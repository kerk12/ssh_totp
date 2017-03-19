#!/usr/bin/env bash

python /usr/bin/sshtotp

if [ "$?" -eq "0" ]
then
    /bin/bash
fi
# No need to terminate the session. ForceCommand handles that.