#!/usr/bin/env python

import sys
import json
import argparse
import subprocess

import paramiko

def parse_args():
    parser = argparse.ArgumentParser(description="Vagrant inventory script")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true', help="list vagrant hostnames")
    group.add_argument('--host', help="show vagrant host details")
    return parser.parse_args()

def list_running_hosts():
    cmd = "vagrant status --machine-readable"
    status = subprocess.check_output(cmd.split()).decode().rstrip()
    hosts = []
    for line in status.split('\n'):
        _, host, key, value = line.split(',')[:4]
        if key == 'state' and value == 'running':
            hosts.append(host)
    return hosts

def get_host_details(host):
    cmd = f"vagrant ssh-config {host}"
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    ssh = paramiko.SSHConfig()
    ssh.parse(p.stdout)
    config = ssh.lookup(host)
    return {
        'ansible_host': config['hostname'],
        'ansible_port': config['port'],
        'ansible_user': config['user'],
        'ansible_private_key_file': config['identityfile'][0],
    }

def main():
    args = parse_args()
    if args.list:
        hosts = list_running_hosts()
        details = {'vagrant': hosts}
    else:
        details = get_host_details(args.host)
    json.dump(details, sys.stdout)

if __name__ == "__main__":
    main()