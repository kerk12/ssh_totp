#!/usr/bin/env bash

python /usr/bin/sshtotp.py

if [ "$?" -eq "1" ]
then
    pkill -9 -t pts/0 
fi
