# Shifting Sands

Crypto · 100 points · 5 solves

Flag: `CLUB{vigenere_is_not_unbreakable}`

> We intercepted a message from an old-school spy. Every letter was shifted, but not all by the same amount. Can you read it?

`cipher.txt`:

```
Kvmt wcef, izseu. Ghi sswds kim vwgimk hybb xjvsg msoujhcb diezj vvufvbstpcf. Ghii smpoie ql QCVJ{owxfvxfv_ja_gck_vvufvbstpcf}
```

A Caesar cipher shifts every letter by the same amount. "Not all by the same amount" points to Vigenère, where a keyword supplies a repeating sequence of shifts. With the key `ORBIT`, the first letter is shifted by O (14), the second by R (17), the third by B (1), and so on, starting over after the fifth letter.

## Using the flag format as a crib

Every flag starts with `CLUB{`, and the ciphertext has `QCVJ{` near the end. Lining them up gives four shifts:

| Plain | Cipher | Shift | Key letter |
|---|---|---|---|
| C | Q | 14 | O |
| L | C | 17 | R |
| U | V | 1 | B |
| B | J | 8 | I |

That's what the in-game hint meant by "You already know how the flag starts."

A four-letter key `ORBI` turns the rest of the message into gibberish, so the key is longer. Trying lengths of 5 and up, with the known letters in place and the unknown ones brute-forced, the candidate that produces English is `ORBIT`.

One detail matters when you decrypt: the key only advances on letters. Spaces, commas and underscores are passed through and don't use up a key letter.

The full plaintext:

> Well done, agent. You broke the cipher that every textbook calls unbreakable. Your reward is CLUB{vigenere_is_not_unbreakable}

`solve/vigenere.py` does the crib step, brute-forces the remaining key letters and scores each candidate for how much it looks like English.

## Other approaches

Without a crib, the Kasiski examination or index of coincidence gives the key length. Each column can then be solved as its own Caesar cipher with frequency analysis. That needs more ciphertext than this message has, but it's the general attack. dCode.fr has a solver that automates it.

Vigenère was once called "le chiffre indéchiffrable". Friedrich Kasiski published a general method for breaking it in 1863.
