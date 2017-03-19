#!/usr/bin/env bash

python /usr/bin/sshtotp

if [ "$?" -eq "0" ]
then
    /bin/bash
fi
