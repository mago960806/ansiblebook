#!/bin/bash

# 签发私有的TLS证书(10年)
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -subj /CN=localhost -keyout nginx.key -out nginx.crt