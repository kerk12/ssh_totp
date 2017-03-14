#!/usr/bin/env bash

if [ "$EUID" -eq 0 ]
then
 	cp sshtotp.py /usr/bin
 	cp sshtotp.sh /usr/bin
fi