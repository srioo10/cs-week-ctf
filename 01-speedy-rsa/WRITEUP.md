# Speedy RSA

Crypto · 250 points · 2 solves

Flag: `CLUB{Weiner_Attack26}`

> An admin generated an RSA key and tweaked it so decryption would be as fast as possible. The flag is encrypted with it. Can you decrypt the message?

`output.txt` gives three numbers: the modulus `n`, the public exponent `e`, and the ciphertext `c`.

## What gives it away

`n` is 1024 bits, and so is `e`, almost. In normal RSA, `e` is small (usually 65537) and the private exponent `d` is about as large as `n`. When `e` is that big, the key was probably built the other way round: someone picked a small `d` first and calculated `e` from it.

The challenge text says why. Decryption is `c^d mod n`, so a smaller `d` means fewer multiplications and faster decryption. That's the mistake this challenge is built on.

## Wiener's attack

Michael Wiener showed in 1990 that if `d` is less than about a quarter of the bit length of `n`, then `e/n` is very close to `k/d` for some small integer `k`. The continued fraction expansion of `e/n` produces a sequence of approximations called convergents, and one of them will be exactly `k/d`.

Testing each convergent works like this:

1. Take the convergent `k/d`. If `k` is 0, skip it.
2. If `d` is the real private exponent, then `(e·d − 1) / k` is a whole number, and that number is `φ(n)`.
3. From `φ(n)` you get `p + q = n − φ(n) + 1`, and you already know `p · q = n`. Those two give a quadratic whose roots are `p` and `q`. If the roots come out as integers, `n` is factored and the candidate is correct.
4. Decrypt with `m = c^d mod n` and convert `m` to bytes.

`solve/wiener.py` does this. The `d` it recovers is 253 bits, right around the limit for a 1024-bit modulus:

```
d bits : 253 | n bits: 1024
CLUB{Weiner_Attack26}
```

The flag spells it "Weiner", not "Wiener", so copy it exactly.

## Notes

RSA libraries choose a small `e` and let `d` fall where it falls, which keeps `d` large. A public exponent close to the size of the modulus is the signal to try Wiener's attack.

Two teams solved it. The in-game hints pointed first at comparing the size of `e` to `n`, then at continued fractions.
