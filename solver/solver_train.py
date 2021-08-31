from pwn import *
import struct
import hashlib

#conn = process("./runaway_train_server")
conn = remote("3.19.107.33", 31337)

train_labels = ["X", "A", "B", "C"]

def setDirection(train, direction):
    conn.sendlineafter(">> ", "2")
    conn.sendlineafter(">> ", str(train_labels.index(train)))
    conn.sendlineafter(">> ", "1")
    conn.sendlineafter(">> ", str(direction))
    conn.sendlineafter(">> ", "5")

def splitFuel(from_train, to_train, trans_fuel):
    conn.sendlineafter(">> ", "2")
    conn.sendlineafter(">> ", str(train_labels.index(from_train)))
    conn.sendlineafter(">> ", "2")
    conn.sendlineafter(">> ", str(train_labels.index(to_train)))
    conn.sendlineafter(">> ", str(trans_fuel))
    conn.sendlineafter(">> ", "5")

def Filling(train):
    conn.sendlineafter(">> ", "2")
    conn.sendlineafter(">> ", str(train_labels.index(train)))
    conn.sendlineafter(">> ", "3")
    conn.sendlineafter(">> ", "5")

def spendTime(time):
    conn.sendlineafter(">> ", "3")
    conn.sendlineafter(">> ", str(time))

def pow_hash(challenge, solution):
    return hashlib.sha256(challenge.encode('ascii') + struct.pack('<Q', solution)).hexdigest()

def check_pow(challenge, n, solution):
    h = pow_hash(challenge, solution)
    return (int(h, 16) % (2**n)) == 0

def solve_pow(challenge, n):
    candidate = 0
    while True:
        if check_pow(challenge, n, candidate):
            return candidate
        candidate += 1

conn.recvuntil('Solving challenge: "')
challenge = conn.recvuntil('"')[:-1].decode()
n = int(conn.recvline()[5:].decode())
log.progress(f'Solving challenge: "{challenge}", n: {n}')
solution = solve_pow(challenge, n)
log.info(f'solution: {solution}')
conn.sendline(str(solution))

setDirection("A", 1)
setDirection("B", 1)
setDirection("C", 1)
spendTime(16)

setDirection("C", 2)
splitFuel("C", "A", 16)
splitFuel("C", "B", 16)
spendTime(16)

Filling("C")
setDirection("B", 2)
splitFuel("B", "A", 16)
spendTime(32)

Filling("B")
setDirection("C", 2)
spendTime(32)

setDirection("B", 2)
setDirection("C", 1)
splitFuel("C", "A", 16)
spendTime(16)

setDirection("B", 1)
splitFuel("B", "A", 16)
splitFuel("B", "C", 16)
spendTime(16)

conn.recvuntil("   o       | ")
data = conn.recvline()
flag = b""
for i in range(0, len(data), 8):
    flag += bytes([data[i]])

log.info("flag : " + flag.decode())

conn.close()