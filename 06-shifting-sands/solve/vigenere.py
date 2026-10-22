# Shifting Sands - Vigenere solved with a known-plaintext crib (the flag starts with "CLUB{")
import itertools, string

ct = open("../files/cipher.txt").read().strip()
A = string.ascii_uppercase
letters = [c for c in ct if c.isalpha()]

# 1) The flag is written CLUB{...}; in the ciphertext that is QCVJ{...}.
#    Subtracting plaintext from ciphertext letter by letter reveals the key letters used there.
crib_p, crib_c = "CLUB", "QCVJ"
key_start = "".join(A[(A.index(c) - A.index(p)) % 26] for p, c in zip(crib_p, crib_c))
pos = "".join(letters).index(crib_c)             # which letter of the message the crib sits at
print("key letters at the crib:", key_start, "| crib position:", pos)

def decrypt(ct, key):
    out, i = [], 0
    for ch in ct:
        if ch.isalpha():                          # the key only advances on letters
            base = ord("A") if ch.isupper() else ord("a")
            out.append(chr((ord(ch) - base - A.index(key[i % len(key)])) % 26 + base))
            i += 1
        else:
            out.append(ch)
    return "".join(out)

COMMON = ["THE", "AND", "THAT", "WITH", "FROM", "THIS", "YOU", "YOUR", "AGENT", "CIPHER", "REWARD"]
score = lambda t: sum(t.upper().count(w) * len(w) for w in COMMON)

# 2) We know 4 key letters, but not how long the key is. Try lengths 5-8,
#    brute-force the unknown letters, and keep whatever reads like English.
best = []
for L in range(5, 9):
    fixed = {(pos + j) % L: k for j, k in enumerate(key_start)}
    free = [i for i in range(L) if i not in fixed]
    for combo in itertools.product(A, repeat=len(free)):
        key = [fixed.get(i) for i in range(L)]
        for i, k in zip(free, combo):
            key[i] = k
        key = "".join(key)
        text = decrypt(ct, key)
        best.append((score(text), key, text))
best.sort(reverse=True)
s, key, text = best[0]
print("key:", key)
print(text)
