from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


K1 = 123456        # a number below 2**20
K2 = 654321        # a number below 2**20
FLAG = b"CLUB{this_is_not_the_real_flag}"

def enc(k, data):
    key = k.to_bytes(16, "big")      
    return AES.new(key, AES.MODE_ECB).encrypt(data)

def double_enc(data):
    return enc(K2, enc(K1, data))     # encrypted twice, with two different keys

KNOWN = b"CLUB_KNOWN_BLOCK"           

print("known plaintext :", KNOWN.hex())
print("its ciphertext  :", double_enc(KNOWN).hex())
print("encrypted flag  :", double_enc(pad(FLAG, 16)).hex())
