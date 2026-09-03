#!/usr/bin/env python3
"""conj006d_check.py — «уязвимые по паре» клетки: пустая q коллинеарна с парой {p,s} ⊂ S и каждая тройка-убийца q содержит {p,s}.
usage: python3 conj006d_check.py ФАЙЛ … | random n runs seed"""
import sys, itertools, random, collections
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from kappa_general import read_pts, coplanar, collinear
from rigid_a280537 import grow
def vulnerable(S, n):
    Sset = set(S); out = []
    cells = [c for c in itertools.product(range(n), repeat=3) if c not in Sset]
    for q in cells:
        pairs = [(a, b) for a, b in itertools.combinations(S, 2) if collinear([q, a, b])]
        if not pairs: continue
        K = [set(t) for t in itertools.combinations(S, 3) if coplanar(q, *t)]
        for a, b in pairs:
            if all({a, b} <= t for t in K): out.append((q, (a, b), len(K))); break
    return out
if __name__ == "__main__":
    if sys.argv[1] == "random":
        n, runs, seed = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); rnd = random.Random(seed); cnt = 0
        for _ in range(runs):
            S, _ = grow(n, rnd)
            if vulnerable(S, n): cnt += 1
        print(f"случайные максимальные n={n}: с уязвимыми по паре клетками {cnt}/{runs} = {cnt/runs:.2f}")
    else:
        for path in sys.argv[1:]:
            S = read_pts(path); import re
            hdr = re.search(r'\bn=(\d+)', open(path).readline()); n = int(hdr.group(1)) if hdr else max(max(p) for p in S) + 1
            v = vulnerable(S, n)
            print(f"{path.rsplit('/',1)[-1]}: n={n} m={len(S)} уязвимых по паре клеток: {len(v)}" + (f"  пример {v[0]}" if v else ""))
