# Lone Knight - read the letter on every square the knight stood on
import re

grid = [l.split() for l in open("../files/board.txt") if l.strip()]   # grid[0] is rank 8 (White's view)
pgn = open("../files/game.pgn").read()
fen = re.search(r'\[FEN "([^"]+)"', pgn).group(1)

# knight's start square from the FEN: find the 'N'
ranks = fen.split()[0].split("/")
sq = None
for ri, row in enumerate(ranks):
    f = 0
    for ch in row:
        if ch.isdigit(): f += int(ch)
        else:
            if ch == "N": sq = "abcdefgh"[f] + str(8 - ri)
            f += 1
squares = [sq]

# every white move is a knight move: take the destination square
moves = re.sub(r"\{.*?\}|\[.*?\]", "", pgn)
for m in re.findall(r"\d+\.\s*(\S+)", moves):
    squares.append(re.sub(r"[+#x]", "", m)[-2:])

def letter(square):
    file_, rank = "abcdefgh".index(square[0]), int(square[1])
    return grid[8 - rank][file_]

print("squares:", " ".join(squares))
print("letters:", "".join(letter(s) for s in squares))
