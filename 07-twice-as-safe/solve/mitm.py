# Twice as safe - meet-in-the-middle on double AES-ECB with two 20-bit keys
import re, time
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

txt = open("../files/output.txt").read()
known_p = bytes.fromhex(re.search(r"known plaintext\s*:\s*(\w+)", txt).group(1))
known_c = bytes.fromhex(re.search(r"its ciphertext\s*:\s*(\w+)", txt).group(1))
flag_c  = bytes.fromhex(re.search(r"encrypted flag\s*:\s*(\w+)", txt).group(1))

def key(k): return k.to_bytes(16, "big")

t = time.time()
# forward half: P --K1--> middle  (store every possible middle value)
table = {}
for k1 in range(1 << 20):
    table[AES.new(key(k1), AES.MODE_ECB).encrypt(known_p)] = k1
print(f"built {len(table):,} entries in {time.time()-t:.1f}s")

# backward half: C --K2^-1--> middle, look for a match
for k2 in range(1 << 20):
    mid = AES.new(key(k2), AES.MODE_ECB).decrypt(known_c)
    if mid in table:
        k1 = table[mid]
        print("K1 =", k1, " K2 =", k2)
        pt = AES.new(key(k1), AES.MODE_ECB).decrypt(AES.new(key(k2), AES.MODE_ECB).decrypt(flag_c))
        print(unpad(pt, 16).decode())
        break
