#!/usr/bin/env python3
"""rigid_kappa_dist.py — распределение κ³ пустых клеток у случайных максимальных конфигураций A280537 (жадный рост) и на каких клетках
реализуется нежёсткость. usage: python3 rigid_kappa_dist.py n runs seed"""
import sys, random, itertools, collections
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from rigid_a280537 import grow, coplanar
n, runs, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); rnd = random.Random(seed)
hist = collections.Counter(); low_frac = []; medians = []; revive_kappa = collections.Counter(); nonrigid = 0
for r in range(runs):
    S, kap = grow(n, rnd); Sset = set(S)
    cells = [c for c in ((x, y, z) for x in range(n) for y in range(n) for z in range(n)) if c not in Sset]
    ks = sorted(kap[c] for c in cells); hist.update(ks); low_frac.append(sum(1 for k in ks if k <= 2) / len(ks)); medians.append(ks[len(ks) // 2])
    found = False
    for p in S:
        rest = [s for s in S if s != p]
        for c in cells:
            thru = sum(1 for a, b in itertools.combinations(rest, 2) if coplanar(c, p, a, b))
            if kap[c] - thru == 0:
                revive_kappa[kap[c]] += 1; found = True
    nonrigid += found
tot = sum(hist.values())
print(f"n={n}, {runs} случайных максимальных: доля пустых клеток с κ³ ≤ 2 = {sum(hist[k] for k in (0,1,2))/tot:.3f} (среднее по конфигурациям {sum(low_frac)/len(low_frac):.3f}), медиана κ³ по конфигурациям: {sorted(medians)[len(medians)//2]}; распределение κ³: {dict(sorted(hist.items())[:10])}")
print(f"  нежёстких {nonrigid}/{runs}; κ³ оживающих клеток (до удаления): {dict(sorted(revive_kappa.items()))}")
