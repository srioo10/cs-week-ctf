# Lights Out 7x7 - solve the toggle puzzle as a linear system over GF(2)
N = 7
board = [l.strip() for l in open("../files/board.txt") if l.strip()]
lit = [1 if ch == "#" else 0 for row in board for ch in row]      # 49 unknowns / equations

# column j of A = effect of pressing cell j (itself + up/down/left/right, no wrapping)
rows = [[0] * (N * N) for _ in range(N * N)]
for r in range(N):
    for c in range(N):
        j = r * N + c
        for dr, dc in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
            rr, cc = r + dr, c + dc
            if 0 <= rr < N and 0 <= cc < N:
                rows[rr * N + cc][j] = 1                           # pressing j flips cell (rr,cc)

# Gaussian elimination on [A | lit]
M = [rows[i] + [lit[i]] for i in range(N * N)]
piv_row = 0
pivots = []
for col in range(N * N):
    sel = next((r for r in range(piv_row, N * N) if M[r][col]), None)
    if sel is None:
        continue
    M[piv_row], M[sel] = M[sel], M[piv_row]
    for r in range(N * N):
        if r != piv_row and M[r][col]:
            M[r] = [a ^ b for a, b in zip(M[r], M[piv_row])]
    pivots.append(col)
    piv_row += 1

print("rank:", len(pivots), "of", N * N, "(49 = exactly one solution)")
x = [0] * (N * N)
for r, col in enumerate(pivots):
    x[col] = M[r][-1]

bits = "".join(map(str, x))
for i in range(N):
    print(bits[i * N:(i + 1) * N])
print("CLUB{" + bits + "}")

# sanity check: replay the presses on the board
state = lit[:]
for j, p in enumerate(x):
    if p:
        r, c = divmod(j, N)
        for dr, dc in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
            rr, cc = r + dr, c + dc
            if 0 <= rr < N and 0 <= cc < N:
                state[rr * N + cc] ^= 1
print("all lights off after pressing:", not any(state))
