#!/usr/bin/env python
import pyotp
import getpass
import json
import os
import argparse
import yaml
from time import sleep
totp = None
path = os.getenv("HOME") + "/.totpKey"
config = None

"""
    All TOTP keys are in JSON form, the config is in YAML to allow comments.
"""

def readOTPKey():
    """ Read the TOTP secret key from the user's home directory. If it doesn't exist, the user hasn't enabled TOTP authentication."""
    user = getpass.getuser()
    try:
        keyfile = file(path, "r")
        jsonKey = json.loads(keyfile.read())
        keyfile.close()
        return jsonKey["key"]
    except IOError:
        return None

def saveOTPKey():
    """ Save a random TOTP secret key to the executing user's home directory. """
    keyNew = pyotp.random_base32()
    keyfile = file(path, "w")
    str_key = json.dumps({"key": keyNew})
    keyfile.write(str_key)
    keyfile.close()
    # Change the file's permissions to be read & written (needed for disabling TOTP) from the current executing user only
    os.chmod(path, 0600)
    return keyNew

def verifyCode(code):
    """ Verifies a 6-digit TOTP code. """
    global totp
    return totp.verify(code)

def setup():
    """ Initializes the script """
    global totp
    key = readOTPKey()
    if key is None:
        exit(0)
    else:
        totp = pyotp.TOTP(key)
        return key

def readConfig():
    """ Read the config file and parse it """
    config_file = open("/etc/sshtotp/config.yml", "r")
    config = yaml.load(config_file)
    config_file.close()
    return config

if __name__ == "__main__":

    # Get the command line arguments.
    # --enable: Enables TOTP authentication for the current user
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--enable', help='Enable totp for the current user.', action="store_true")
    parser.add_argument('-d', '--disable', help="Disable TOTP authentication for the current user.", action="store_true")
    parser.add_argument('-v', "--view", help="View the Secret key set", action="store_true")
    parser.add_argument("-c", "--copyright", help="Show Copyright", action="store_true")
    args = parser.parse_args()

    config = readConfig()

    if args.copyright:
        print """SSH TOTP Authentication Script \nCopyright (C) 2017 Kyriakos Giannakis <kerk12gr@gmail.com>\nReleased under the GNU GPL v3.0 Licence"""
        exit(0)
    if args.enable:
        key = saveOTPKey()
        print "TOTP Authentication enabled. Your secret key is: " + key
        print "You can add the above key to your authenticator app. \nWe recommend using Google Authenticator or FreeOTP."
        exit(0)
    elif args.disable:
        if readOTPKey() is not None:
            os.remove(path)
            print "TOTP Authentication has been disabled successfully for SSH logins."
            exit(0)
        else:
            print "TOTP Authentication hasn't been enabled for this user."
            exit(1)
    elif args.view:
        key = readOTPKey()
        if key is not None:
            print "Your secret key is:" + key
        else:
            print "TOTP authentication hasn't been activated."
        exit(0)

    setup()
    if "max_tries" in config:
        max_tries = config["max_tries"]
    else:
        max_tries = 0

    if "delay" in config:
        delay = config["delay"]
    else:
        delay = 0

    count = 0

    while True:
        if max_tries > 0:
            if count == max_tries:
                print "You have exceeded the allowed number of tries. You have been logged out."
                exit(1)
        try:
            code = raw_input("Please input your OTP: ")
            if len(code) != 6:
                raise ValueError
            if verifyCode(int(code)):
                exit(0)
            else:
                print "Invalid code supplied"
        except KeyboardInterrupt:
            exit(1)
        except ValueError:
            # A ValueError exception gets raised whenever the code string cannot be converted to an integer, or when it isn't of the required length.
            print "Please enter a valid 6-digit OTP code"
        finally:
            if max_tries > 0:
                count += 1
            if delay > 0:
                sleep(delay)