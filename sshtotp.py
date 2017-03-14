#/usr/bin/python
import pyotp
import getpass
import json
import os
import argparse
totp = None

def readOTPKey():
    user = getpass.getuser()
    try:
        keyfile = file(os.getenv("HOME")+"/.totpKey", "r")
        jsonKey = json.loads(keyfile.read())
        keyfile.close()
        return jsonKey["key"]
    except IOError:
        return None

def saveOTPKey():
    keyNew = pyotp.random_base32()
    user = getpass.getuser()
    keyfile = file(os.getenv("HOME")+"/.totpKey", "w")
    str_key = json.dumps({"key": keyNew})
    keyfile.write(str_key)
    keyfile.close()
    return keyNew

def verifyCode(code):
    global totp
    return totp.verify(code)

def setup():
    global totp
    key = readOTPKey()
    if key is None:
        exit(0)
    else:
        totp = pyotp.TOTP(key)
        print key
        return key

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--enable', help='Enable totp for the current user.', action="store_true")
    args = parser.parse_args()
    if args.enable:
        key = saveOTPKey()
        print "TOTP Authentication enabled. Your secret key is: " + key
        exit(0)

    setup()
    while True:
        try:
            code = int(raw_input("Please input your OTP: "))
            if verifyCode(code):
                exit(0)
            else:
                print "Invalid code supplied"
        except KeyboardInterrupt:
            exit(1)