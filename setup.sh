#!/usr/bin/env bash

if [ "$EUID" -ne 0 ]
then
    echo 'The script needs to be run as root.'
fi

chmod 555 *
cp sshtotp.py /usr/bin/sshtotp
cp sshtotp.sh /usr/bin
cp enable_totp /usr/bin
echo 'ForceCommand /usr/bin/sshtotp.sh && exit' >> /etc/ssh/sshd_config
echo 'SSH OTP has been installed successfully. You can enable TOTP authentication for a user by issuing the command'
echo 'sshtotp --enable'