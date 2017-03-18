#/usr/bin/python2.7
import pyotp
import getpass
import json
import os
import argparse
totp = None

"""
    All TOTP keys are in JSON form, the config is in YAML to allow comments.
"""

def readOTPKey():
    """ Read the TOTP secret key from the user's home directory. If it doesn't exist, the user hasn't enabled TOTP authentication."""
    user = getpass.getuser()
    try:
        keyfile = file(os.getenv("HOME")+"/.totpKey", "r")
        jsonKey = json.loads(keyfile.read())
        keyfile.close()
        return jsonKey["key"]
    except IOError:
        return None

def saveOTPKey():
    """ Save a random TOTP secret key to the executing user's home directory. """
    keyNew = pyotp.random_base32()
    user = getpass.getuser()
    keyfile = file(os.getenv("HOME")+"/.totpKey", "w")
    str_key = json.dumps({"key": keyNew})
    keyfile.write(str_key)
    keyfile.close()
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
    # TODO --disable
    # TODO --view-key
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--enable', help='Enable totp for the current user.', action="store_true")
    args = parser.parse_args()
    if args.enable:
        key = saveOTPKey()
        print "TOTP Authentication enabled. Your secret key is: " + key
        print "You can add the above key to your authenticator app. \nWe recommend using Google Authenticator or FreeOTP."
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
            """ A ValueError exception gets raised whenever the code string cannot be converted to an integer, or when it isn't of the required length. """
            print "Please enter a valid 6-digit OTP code"