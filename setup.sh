#!/usr/bin/env bash

if [ "$EUID" -eq 0 ]
then
 	cp sshtotp.py /usr/bin
 	cp sshtotp.sh /usr/bin
 	echo 'ForceCommand /usr/bin/sshtotp.sh' >> /etc/ssh/sshd_config
fi