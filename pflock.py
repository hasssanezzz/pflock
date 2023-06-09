from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import InvalidToken
from getpass import getpass
from glob import glob
from time import perf_counter as pc
import sys
import os
import base64

key = Fernet.generate_key()
coder = Fernet(key)
password = ""
recursive = False

def genKey(password):
    # generate your own.
    salt = b"@\xef\x07k\x14\xe9\x0f^/\xc7\xc2\xe8_\x95\x17\xe4"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def encode_file(path):
    tmr = pc()

    if not os.path.exists(path):
        print("[!] Error: file does exist", path)
        return
    
    try:
        with open(path, "rb") as f:
            sample = f.read()
    except:
        print("[!] Error: couldn't read file", path)
    
    enc = coder.encrypt(sample)
    
    try:
        with open(path, "wb") as f:
            f.write(enc)
        print(f"[+] File encoded in {'{:.4f}'.format(pc() - tmr)} seconds")
    except:
        print("[!] Error: couldn't write file", path)
    


def decode_file(path):

    if not os.path.exists(path):
        print("[!] Error: file does exist", path)
        return

    tmr = pc()
    try:
        with open(path, "rb") as f:
            sample = f.read()
    except:
        print("[!] Error: couldn't read file", path)

    try:
        dec = coder.decrypt(sample)
        with open(path, "wb") as f:
            f.write(dec)
        print(f"[+] File decoded in {'{:.4f}'.format(pc() - tmr)} seconds")
    except:
        print("[!] Error: can not decode file")


def getPasswordConfirmation():
    p1 = getpass("Enter your key: ")
    p2 = getpass("Enter your key again: ")
    while p1 != p2:
        print("[!] Passwords don't match!")
        p1 = getpass("Enter your key: ")
        p2 = getpass("Enter your key again: ")
    print()
    return p1

def myJoin(filenames, org):
    for i in range(0, len(filenames)):
        filenames[i] = os.path.join(org, filenames[i])
    return filenames

def operate(files):
    for filename in files:
        if os.path.isdir(filename):
            if recursive:
                operate(myJoin(os.listdir(filename), filename))
        elif os.path.exists(filename) and filename.find("pflock") == -1:
            print("Processing:", os.path.abspath(filename))
            if cmnd == "decode" or cmnd == "d":
                decode_file(filename)
            elif cmnd == "encode" or cmnd == "e":
                encode_file(filename)


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 3:
        print("[!] Error: missing arguments")
        exit()

    cmnd = args[1]
    if cmnd in ["decode", "encode", "e", "d"]:
        if cmnd == "decode" or cmnd == "d":
            password = getpass("Enter your key: ")
        else:
            password = getPasswordConfirmation()
    else:
        print("[!] Unknow command")
        exit()

    coder = Fernet(genKey(password))

    if "-r" in args:
        recursive = True

    duration = pc()
    for i in range(2, len(args)):
        files = glob(args[i])
        operate(files)

    print(f"\nAll done in {'{:.4f}'.format(pc() - duration)} seconds")
