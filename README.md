### A Python based 2FA Time-based One Time Password script for authenticating in SSH.

Developed by Kyriakos Giannakis

##### Install:
0. ```git clone ...```
1. Install the requirements:
```$ sudo pip install -r requirements.txt```
2. Run the install script as root:
```$ sudo ./setup.sh```
3. Restart the SSH service:
```$ sudo service ssh restart```
4. Now each user needs to enable 2FA on his own account, by issuing: 
```$ sshtotp --enable```. When the command is run, a base32 Secret Key will be generated and saved in HOME/.totpKey.
This needs to be copied onto a 2FA mobile app such as Google Authenticator or FreeOTP. Keep this key secret.

Whenever a user tries to log in, a prompt to enter a One Time Password will appear.

Note: The time on both the server and the mobile device needs to be in sync. We recommend using NTP for syncing the time.

##### Open Source Licences:
[PyOTP](https://github.com/pyotp/pyotp).
Copyright (C) 2011-2016 Mark Percival <m@mdp.im>, Nathan Reynolds <email@nreynolds.co.uk>, and PyOTP contributors.
