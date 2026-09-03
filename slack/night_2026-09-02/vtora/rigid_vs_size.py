#!/usr/bin/env python3
"""rigid_vs_size.py — доля заменяемых точек у случайных максимальных конфигураций A280537 как функция размера (need-006, ставка 03.09).
Заменяемая точка p: после удаления p допустима хотя бы одна клетка, кроме p (прямой счёт определителями, независимо от κ).
usage: python3 rigid_vs_size.py n runs seed"""
import sys, random, itertools, collections
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from rigid_a280537 import grow, coplanar
n, runs, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); rnd = random.Random(seed)
cells_all = list(itertools.product(range(n), repeat=3))
by_size = collections.defaultdict(list)
for r in range(runs):
    out = grow(n, rnd); S = out[0] if isinstance(out, tuple) else out
    Sset = set(S); cells = [c for c in cells_all if c not in Sset]
    repl = 0
    for p in S:
        T = [s for s in S if s != p]; trip = list(itertools.combinations(T, 3))
        if any(not any(coplanar(q, *t) for t in trip) for q in cells): repl += 1
    by_size[len(S)].append(repl / len(S))
    if (r + 1) % 25 == 0: print(f"# {r+1} конфигураций", flush=True)
print(f"n={n}, {runs} случайных максимальных (seed {seed}): размер | конфигураций | средняя доля заменяемых | доля жёстких")
for m in sorted(by_size):
    v = by_size[m]; print(f"|S|={m:2d} | {len(v):3d} | {sum(v)/len(v):.3f} | {sum(1 for x in v if x == 0)/len(v):.3f}", flush=True)
