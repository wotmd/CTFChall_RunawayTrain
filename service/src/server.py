#!/usr/bin/env python3
import subprocess
import random
import hashlib
import struct
import string

def check_pow():
    characters = string.ascii_letters + string.digits
    challenge = ''.join(random.choice(characters) for _ in range(10))
    n = 22
    print('Solving challenge: "{}", n: {}'.format(challenge, n))
    solution = int(input("solution: "))

    h = pow_hash(challenge, solution)
    return (int(h, 16) % (2**n)) == 0

def pow_hash(challenge, solution):
    return hashlib.sha256(challenge.encode('ascii') + struct.pack('<Q', solution)).hexdigest()

def random_string(length = 10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

if __name__ == "__main__":
    try:
        if not check_pow():
            exit(0)
    except:
        print("pow fail")
        exit(0)
    subprocess.run(["./runtrain"], shell=True)
    

