"""crosstriples.py — Computation B: for the union of hyperbola lifts H(1,p) and H(1,q) in the N x N window (HJSW x-shift for
each modulus), count collinear-over-Z triples: within p, within q, and cross (points from both).  Growth of the cross count
with N decides whether the two-prime union can beat 3/2 (Theta(N^2) kills it; o(N^2) leaves room).
usage: crosstriples.py p q N [p q N ...]"""
import sys
from itertools import combinations
def cands(p, N):
    out = []
    for x in range(N):
        xp = ((x - (p - 1) // 2) % p + p) % p
        if xp == 0: continue
        for y in range(N):
            if y % p and (xp * y - 1) % p == 0: out.append((x, y))
    return out
def collinear(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]) == 0
args = list(map(int, sys.argv[1:]))
print("p q N |Hp| |Hq| |union| triples: within_p within_q cross | cross/N^2 cross/N | HJSW-like 3(max-1)")
for i in range(0, len(args), 3):
    p, q, N = args[i:i+3]
    Hp, Hq = cands(p, N), cands(q, N)
    sp, sq = set(Hp), set(Hq)
    U = sorted(sp | sq)
    wp = wq = cross = 0
    for a, b, c in combinations(U, 3):
        if not collinear(a, b, c): continue
        inp = sum(1 for t in (a, b, c) if t in sp); inq = sum(1 for t in (a, b, c) if t in sq)
        if inp == 3 and inq < 3: wp += 1
        elif inq == 3 and inp < 3: wq += 1
        else: cross += 1
    print(f"{p:3d} {q:3d} {N:3d} {len(Hp):4d} {len(Hq):4d} {len(U):5d}   {wp:6d} {wq:6d} {cross:6d} | {cross/N**2:.3f} {cross/N:.2f} | {3*(max(p,q)-1)}")
