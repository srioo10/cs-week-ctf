# Lone Knight

Misc · 200 points · 6 solves

Flag: `CLUB{kn1ght_m0v3s_sp34k}`

> A lone knight wandered the board, and the board remembers every square it stood on. Read what it saw.

There are two files.

`game.pgn` is a chess game that starts from a custom position, given as a FEN: `7k/8/8/8/5N2/8/8/K7 w`. That's a white knight on f4, a white king on a1 and a black king on h8, followed by a list of moves.

`board.txt` is an 8×8 grid of characters:

```
N v 1 m y s e f
g _ j _ v q a X
b s 0 z 2 U 3 K
r 3 t k Z L t L
p n y h 4 C B a
J m 3 h { U X i
1 a d D Z k l R
9 A g } h i p T
```

The grid is a chessboard with one character on each square. The knight's route across the board spells the flag.

## Solving it

The kings are noise. The white king never moves, and the black king only shuffles between g8 and h8. One of the hints says it directly: "Ignore the king. Only the knight matters."

Write down every square the knight stands on, including the one it starts on. The starting square comes from the FEN, not from the move list, and the second hint is there for that ("The knight's starting square counts too"):

```
f4 h5 f6 g4 e3 d5 b4 a2 c1 d3 c5 b7 d8 c6 e7 g6 f8 d7 b6 a4 c3 e4 f2 d1
```

That's 24 squares, the same as the number of characters in the flag.

Read `board.txt` the way a board looks from White's side. The first line is rank 8 and the last line is rank 1. Columns go a to h from left to right. So a8 is the top-left `N` and h1 is the bottom-right `T`.

Looking up each square in order:

```
f4 C   h5 L   f6 U   g4 B   e3 {   d5 k   b4 n   a2 1
c1 g   d3 h   c5 t   b7 _   d8 m   c6 0   e7 v   g6 3
f8 s   d7 _   b6 s   a4 p   c3 3   e4 4   f2 k   d1 }
```

Together: `CLUB{kn1ght_m0v3s_sp34k}`.

`solve/lone_knight.py` does the same thing and reads the start square from the FEN.

## Where people went wrong

Skipping f4 drops the first letter, so the result starts `LUB{`. Reading the grid with rank 1 at the top gives nonsense. Including the king's squares adds extra characters.
