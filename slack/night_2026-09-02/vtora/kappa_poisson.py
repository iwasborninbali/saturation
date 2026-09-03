#!/usr/bin/env python3
"""kappa_poisson.py — механизм закона need-006: доля пустых клеток с κ³ ≤ 2 против пуассоновского хвоста при среднем κ³ конфигурации.
Для случайных максимальных (жадный рост) и заданных файлов: λ = среднее κ³ по пустым клеткам, p_obs = доля клеток с κ³ ≤ 2,
p_pois = e^{−λ}(1 + λ + λ²/2); пул по размеру. usage: python3 kappa_poisson.py n runs seed [ФАЙЛ …]"""
import sys, math, random, itertools, collections, re
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from rigid_a280537 import grow, coplanar
from kappa_general import read_pts
def kappa_stats(S, n):
    Sset = set(S); cells = [c for c in itertools.product(range(n), repeat=3) if c not in Sset]
    trip = list(itertools.combinations(S, 3)); kap = [sum(1 for t in trip if coplanar(q, *t)) for q in cells]
    lam = sum(kap) / len(kap); low = sum(1 for k in kap if k <= 2)
    return lam, low, len(cells)
def pois2(lam): return math.exp(-lam) * (1 + lam + lam * lam / 2)
n, runs, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); rnd = random.Random(seed)
pool = collections.defaultdict(list)
for r in range(runs):
    out = grow(n, rnd); S = out[0] if isinstance(out, tuple) else out
    pool[len(S)].append(kappa_stats(S, n))
print(f"n={n}, {runs} случайных максимальных (seed {seed}): |S| | конф. | среднее λ | доля κ³≤2 наблюдаемая | пуассоновская при среднем λ | отношение")
for m in sorted(pool):
    v = pool[m]; lam = sum(x[0] for x in v) / len(v); pobs = sum(x[1] for x in v) / sum(x[2] for x in v); pp = pois2(lam)
    print(f"|S|={m:2d} | {len(v):3d} | {lam:6.2f} | {pobs:.4f} | {pp:.4f} | {pobs/pp if pp else float('nan'):.2f}", flush=True)
for path in sys.argv[4:]:
    S = read_pts(path); hdr = re.search(r'\bn=(\d+)', open(path).readline()); nn = int(hdr.group(1)) if hdr else max(max(p) for p in S) + 1
    lam, low, N = kappa_stats(S, nn)
    print(f"{path.rsplit('/',1)[-1]}: n={nn} |S|={len(S)} λ={lam:.2f} клеток с κ³≤2: {low} (пуассоновское ожидание {N*pois2(lam):.3f} из {N})", flush=True)
