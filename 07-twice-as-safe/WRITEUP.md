# Twice as safe

Crypto · 150 points · 0 solves

Flag: `CLUB{m33t_1n_th3_m1ddl3}`

> We encrypted the flag twice with two different keys, so it must be twice as hard to break. Right? Both keys are numbers below 1,048,576. The script and its output are attached.

You get two files:

- `encrypt.py`: the encryption script, with the real keys replaced by placeholders so it still runs
- `output.txt`: three hex strings: a known plaintext (`434c55425f4b4e4f574e5f424c4f434b`, which is `CLUB_KNOWN_BLOCK`), its ciphertext, and the encrypted flag

The script encrypts with AES-ECB under key `K1`, then encrypts the result again under `K2`. Each key is a number below 2²⁰, padded out to a 16-byte AES key.

## Why two keys don't help much

Trying every pair of keys means 2²⁰ × 2²⁰ = 2⁴⁰ combinations, about a trillion. That's too slow in Python.

Having a known plaintext/ciphertext pair changes things. Encryption under `K1` takes the plaintext to some middle value, and encryption under `K2` takes that middle value to the ciphertext:

```
known plaintext  --K1-->  middle  --K2-->  known ciphertext
```

So you can work from both ends:

1. For every `K1` from 0 to 1,048,575, encrypt the known plaintext and store the result in a table mapping it back to `K1`.
2. For every `K2`, decrypt the known ciphertext and look the result up in the table.
3. A match gives both keys.

That's about 2²⁰ + 2²⁰, roughly two million AES operations, plus a table with a million 16-byte entries. Any laptop can do that.

Here the match is `K1 = 480948` and `K2 = 935002`. Decrypting the flag with `K2` first and then `K1`, and removing the padding, gives:

```
CLUB{m33t_1n_th3_m1ddl3}
```

`solve/mitm.py` does this in plain Python with `pycryptodome` and finishes in under a minute.

## Notes

With two independent `n`-bit keys, meet-in-the-middle brings the cost down to about `2^(n+1)` instead of `2^(2n)`, at the price of memory for the table. This is the attack that ruled out Double DES and is the reason Triple DES uses three stages.

Nobody solved it during the event. The two hints were "Is there a way to test the two keys separately?" and "Work from both ends and look for a match in the middle."
