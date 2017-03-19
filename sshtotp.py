#!/usr/bin/env python
import pyotp
import getpass
import json
import os
import argparse
totp = None
path = os.getenv("HOME") + "/.totpKey"

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

if __name__ == "__main__":

    # Get the command line arguments.
    # --enable: Enables TOTP authentication for the current user
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--enable', help='Enable totp for the current user.', action="store_true")
    parser.add_argument('-d', '--disable', help="Disable TOTP authentication for the current user.", action="store_true")
    parser.add_argument('-v', "--view", help="View the Secret key set", action="store_true")
    args = parser.parse_args()

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
    # TODO implement config
    while True:
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