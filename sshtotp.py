#/usr/bin/python
import pyotp
import getpass
import json
import os
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

def saveOTPKey(key):
    user = getpass.getuser()
    keyfile = file(os.getenv("HOME")+"/.totpKey", "w")
    str_key = json.dumps({"key": key})
    keyfile.write(str_key)
    keyfile.close()
    return True

def verifyCode(code):
    global totp
    return totp.verify(code)

def setup():
    global totp
    key = readOTPKey()
    if key is None:
        keyNew = pyotp.random_base32()
        saveOTPKey(keyNew)
        totp = pyotp.TOTP(keyNew)
    else:
        totp = pyotp.TOTP(key)

if __name__ == "__main__":
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