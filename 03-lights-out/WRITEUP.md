# Lights Out

Misc · 100 points · 5 solves

Flag: `CLUB{0100010000011001100101010011100100100110011111011}`

> Pressing a cell toggles it and its four neighbors (up, down, left, right, no wrapping). Turn every light off. Each cell is pressed at most once.
> Write your solution as 49 bits, row by row, with 1 for a pressed cell and 0 for an untouched one.

`board.txt` is a 7×7 grid, with `#` for a lit cell and `.` for an unlit one:

```
###...#
..##..#
..##.#.
.#..###
.##.#.#
..#.#.#
.#.#..#
```

Two properties make this solvable. The order of presses doesn't matter, and pressing a cell twice is the same as not pressing it. So each of the 49 cells is either pressed or not, which is why the answer is 49 bits.

## Light chasing (the in-game hint)

Pick a set of presses for the first row. After that, every other press is forced: the only way left to turn off a lit cell in row 1 is to press the cell directly below it. Do that for row 1, then row 2, and so on down the board. If the bottom row ends up dark, you're done. If not, try a different first row.

There are only 2⁷ = 128 choices for the first row, so a short script can try them all.

## Linear algebra over GF(2)

`solve/lights_out.py` treats the puzzle as a system of equations. Each press flips a fixed set of cells, and flipping twice cancels out, so this is arithmetic mod 2, where 1 + 1 = 0. Addition becomes XOR.

The unknown is a 49-bit vector `x` (which cells to press). Each cell gives one equation: the presses that touch it, added mod 2, must equal its starting state. That's a 49×49 matrix of 0s and 1s, solved with ordinary Gaussian elimination using XOR in place of subtraction.

The matrix has rank 49, so there is exactly one solution:

```
0100010
0000110
0110010
1010011
1001001
0011001
1111011
```

Reading it row by row gives the flag. The script also applies these presses to the original board to confirm that every light goes out.

## Notes

The unique solution is what makes a fixed flag possible here. Some sizes, 5×5 included, have more than one valid solution, and a challenge on those boards would need a checker instead of a single flag.

When a puzzle's moves commute and doing a move twice undoes it, it's usually a linear system over GF(2).
