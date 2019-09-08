# 建立一台用于测试的服务器
## 使用 Vagrant 来创建测试服务器
使用 Vagrant 之前，需要确保你的机器上已经安装来 VitualBox。VitualBox 可以在[这里](https://www.virtualbox.org/wiki/Downloads)下载，而 Vagrant 则可以在[这里](https://www.vagrantup.com/downloads.html)下载。

创建一个 *playbooks* 目录用于存储 Ansible playbook 和相关文件。运行下列命令将创建一个64位的CentOS7虚拟机镜像对应的Vagrant配置文件(Vagrantfile)，并启动该虚拟机。
```bash
$ mkdir playbooks
$ cd playbooks
$ vagrant init centos/7
$ vagrant up
```

如果一切正常，将会有如下输出：
```
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Importing base box 'centos/7'...
==> default: Matching MAC address for NAT networking...
==> default: Setting the name of the VM: playbooks_default_1567906793079_51174
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
==> default: Forwarding ports...
    default: 22 (guest) => 2222 (host) (adapter 1)
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: private key
    default: 
    default: Vagrant insecure key detected. Vagrant will automatically replace
    default: this with a newly generated keypair for better security.
    default: 
    default: Inserting generated public key within guest...
    default: Removing insecure key from the guest if it's present...
    default: Key inserted! Disconnecting and reconnecting using new SSH key...
==> default: Machine booted and ready!
==> default: Checking for guest additions in VM...
    default: No guest additions were detected on the base box for this VM! Guest
    default: additions are required for forwarded ports, shared folders, host only
    default: networking, and more. If SSH fails on this machine, please install
    default: the guest additions and repackage the box to continue.
    default: 
    default: This is not an error message; everything may continue to work properly,
    default: in which case you may ignore this message.
==> default: Rsyncing folder: /Users/devops/Desktop/ansiblebook/ch01/playbooks/ => /vagrant
```

还可以使用如下命令使用 SSH 登陆到 CentOS7 虚拟机中：
```bash
$ vagrant ssh
```

这种方式虽然方便让我们直接和 shell 交互，但 Ansible 使用标准 SSH 客户端连接到虚拟机，而不是使用 vagrant ssh 命令。如下操作告诉  Vagrant 输出 SSH 连接的详细信息：
```bash
$ vagrant ssh-config
```
在我的机器上，输出信息如下：
```
Host default
  HostName 127.0.0.1
  User vagrant
  Port 2222
  UserKnownHostsFile /dev/null
  StrictHostKeyChecking no
  PasswordAuthentication no
  IdentityFile /Users/devops/Desktop/ansiblebook/ch01/playbooks/.vagrant/machines/default/virtualbox/private_key
  IdentitiesOnly yes
  LogLevel FATAL
  ForwardAgent yes
```

基于这些信息，你可以在命令行上发起对虚拟机的 SSH 会话：
```bash
$ ssh vagrant@127.0.0.1 -p 2222 -i .vagrant/machines/default/virtualbox/private_key
```

你应该能看到如下输出，代表这是正确的。输入 exit 可以退出会话：
```
The authenticity of host '[127.0.0.1]:2222 ([127.0.0.1]:2222)' can't be established.
ECDSA key fingerprint is SHA256:prA1eiec99ZBP1hM1ny5A+P1rroGzY+8hMjB7FhiUVI.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '[127.0.0.1]:2222' (ECDSA) to the list of known hosts.
Last login: Sun Sep  8 01:42:25 2019 from 10.0.2.2
[vagrant@localhost ~]$ exit
logout
Connection to 127.0.0.1 closed.
```

## 将测试服务器的信息配置在 Ansible 中
在  *playbooks* 目录下创建一个文件 *hosts*。这个文件将充当 inventory 文件。
```
web ansible_host=127.0.0.1 ansible_port=2222
```

## 使用 ansible.cfg 文件来简化配置
在 *playbooks* 目录下创建一个文件 *ansible.cfg*。
```
[defaults]
inventory = hosts
remote_user = vagrant
private_key_file = .vagrant/machines/default/virtualbox/private_key
host_key_checking = False
```

## 测试是否能够通过 Ansible 连接上服务器
使用 Ansible 的 ping 模块进行连通性测试。
```bash
$ ansible web -m ping
```

如果正常的话，此时会输出以下内容：
```
web | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
```

## 一些常见命令
使用 Ansible 的 command 模块执行主机命令。
```bash
$ ansible web -m command -a uptime
web | CHANGED | rc=0 >>
 01:58:21 up 18 min,  1 user,  load average: 0.00, 0.01, 0.02
```

由于 command 模块非常常用，可以简化执行：
```bash
$ ansible web -a "tail /var/log/dmesg"
```

使用 Ansible 执行一些需要 sudo 权限的命令。
```bash
$ ansible web -b -a "cat /etc/shadow"
web | CHANGED | rc=0 >>
root:$1$QDyPlph/$oaAX/xNRf3aiW3l27NIUA/::0:99999:7:::
bin:*:17834:0:99999:7:::
daemon:*:17834:0:99999:7:::
adm:*:17834:0:99999:7:::
lp:*:17834:0:99999:7:::
sync:*:17834:0:99999:7:::
shutdown:*:17834:0:99999:7:::
halt:*:17834:0:99999:7:::
mail:*:17834:0:99999:7:::
operator:*:17834:0:99999:7:::
games:*:17834:0:99999:7:::
ftp:*:17834:0:99999:7:::
nobody:*:17834:0:99999:7:::
systemd-network:!!:18048::::::
dbus:!!:18048::::::
polkitd:!!:18048::::::
rpc:!!:18048:0:99999:7:::
rpcuser:!!:18048::::::
nfsnobody:!!:18048::::::
sshd:!!:18048::::::
postfix:!!:18048::::::
chrony:!!:18048::::::
vagrant:$1$C93uBBDg$pqzqtS3a9llsERlv..YKs1::0:99999:7:::
```