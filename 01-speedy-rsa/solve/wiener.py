# Speedy RSA - Wiener's attack (small private exponent d)
import re
from math import isqrt

txt = open("../files/output.txt").read()
n, e, c = (int(re.search(rf"{v} = (\d+)", txt).group(1)) for v in "nec")

def cont_frac(a, b):
    while b:
        q = a // b
        yield q
        a, b = b, a - q * b

def convergents(cf):
    h0, h1, k0, k1 = 0, 1, 1, 0
    for q in cf:
        h0, h1 = h1, q * h1 + h0
        k0, k1 = k1, q * k1 + k0
        yield h1, k1          # (k, d) candidates

for k, d in convergents(cont_frac(e, n)):
    if k == 0 or (e * d - 1) % k:
        continue
    phi = (e * d - 1) // k
    s = n - phi + 1                       # p + q
    disc = s * s - 4 * n
    if disc >= 0 and isqrt(disc) ** 2 == disc:
        p = (s + isqrt(disc)) // 2
        q = (s - isqrt(disc)) // 2
        if p * q == n:
            print("d bits :", d.bit_length(), "| n bits:", n.bit_length())
            print("p =", p)
            print("q =", q)
            m = pow(c, d, n)
            print(m.to_bytes((m.bit_length() + 7) // 8, "big").decode())
            break
