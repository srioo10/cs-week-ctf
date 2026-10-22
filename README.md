# CS Week CTF: challenges and writeups

A jeopardy-style CTF I designed and ran for **CS Week at IIITDM Kancheepuram**, with the campus Cybersecurity Club.
I wrote every challenge, set up the CTFd platform, and ran the event. 19 participants, 300+ flag submissions.

This repo has the player files, a writeup, and a solve script for each challenge, written so someone new to CTFs can follow along.

```
NN-challenge-name/
├── WRITEUP.md   ← what it is, how to crack it, what to take away
├── files/       ← exactly what players downloaded from CTFd
└── solve/       ← a short script that solves it (or reproduces the key steps)
```

## Challenges

| # | Challenge | Category | Points | Solves | Technique |
|---|-----------|----------|-------:|-------:|-----------|
| 01 | [Speedy RSA](01-speedy-rsa/WRITEUP.md) | Crypto | 250 | 2 | Wiener's attack on a small private exponent |
| 02 | [Replay](02-replay/WRITEUP.md) | Misc | 50 | 14 | Reading a plaintext Telnet session from a pcap |
| 03 | [Lights Out](03-lights-out/WRITEUP.md) | Misc | 100 | 5 | Solving the puzzle as linear algebra over GF(2) |
| 04 | [Lone Knight](04-lone-knight/WRITEUP.md) | Misc | 200 | 6 | Following a knight's tour that spells the flag |
| 05 | [Empty File](05-empty-file/WRITEUP.md) | Forensics | 50 | 3 | A program in the Whitespace esolang |
| 06 | [Shifting Sands](06-shifting-sands/WRITEUP.md) | Crypto | 100 | 5 | Breaking Vigenère without the key |
| 07 | [Twice as safe](07-twice-as-safe/WRITEUP.md) | Crypto | 150 | 0 | Meet-in-the-middle on double encryption |
| 08 | [Dvorak Typist](08-dvorak-typist/WRITEUP.md) | Forensics | 400 | 0 | USB HID keystroke capture, Dvorak layout, backspaces |
| 09 | [Deleted Scenes](09-deleted-scenes/WRITEUP.md) | Forensics | 250 | 0 | Recovering deleted files from an ext4 image |
| 10 | [Lost Original](10-lost-original/WRITEUP.md) | OSINT | 250 | 7 | Reverse image search on a disguised photo |
| 11 | [Paper Trail](11-paper-trail/WRITEUP.md) | OSINT | 300 | 5 | Recovering an earlier PDF revision |

Two web challenges, **Guest Pass** and **Forged Pass**, were also in the event. Their writeups are coming.

Flags are in each writeup, so if you want to try a challenge cold, open only its `files/` folder first.

Solve counts are from the CTFd stats at the end of the event. Four challenges (Replay, Deleted Scenes, Dvorak Typist, Paper Trail) have decoy flags on purpose; the writeups explain how to tell them apart.

## Running the solve scripts

Plain Python 3 plus a couple of standard tools. Run each script from inside its own `solve/` folder.

```bash
pip install pycryptodome scapy
sudo apt install e2fsprogs poppler-utils     # debugfs, pdftotext/pdfinfo
# sudo dnf install e2fsprogs poppler-utils   # Fedora
```

## License

Code (solve scripts) is MIT. Writeups and challenge files are free to reuse for teaching or your own CTF, just credit the source. The photo in *Lost Original* belongs to its Wikimedia Commons author; see that writeup.
