# Empty File

Forensics · 50 points · 3 solves

Flag: `CLUB{wh1t3sp4c3_1s_4_l4ngu4g3}`

> An Empty file ???

`empty.txt` looks blank in any editor, but `ls -l` says it's 444 bytes.

`cat -A empty.txt` shows the invisible characters, with `^I` for a tab and `$` for the end of a line. The file is nothing but spaces, tabs and newlines, arranged in regular repeating chunks. Each chunk ends with a newline, followed by a line that is just a tab and a newline.

A file made only of those three characters is a program in Whitespace, an esoteric language that ignores every other character. Paste it into an online Whitespace interpreter, or run it with one locally, and it prints the flag.

## Reading it by hand

This program uses only two Whitespace instructions:

| Characters | Instruction |
|---|---|
| space, space, then a number | push the number onto the stack |
| tab, newline, space, space | print the top of the stack as a character |

A number is a sign character followed by binary digits, with space for 0 and tab for 1, and it ends with a newline.

The first line is `space space space tab space space space space tab tab newline`. The first two spaces mean push. The third space is the sign (positive). The rest, `tab space space space space tab tab`, is binary `1000011`, which is 67, the ASCII code for `C`. The next line, `tab newline space space`, prints it. The rest of the file repeats this pattern for each character of `CLUB{...}`.

`solve/whitespace_decode.py` is a small interpreter for just these two instructions.

## Notes

A file that looks empty but has a non-zero size is worth a `cat -A` or a hex dump. Other ways of hiding text in "nothing" include trailing spaces and zero-width Unicode characters.
