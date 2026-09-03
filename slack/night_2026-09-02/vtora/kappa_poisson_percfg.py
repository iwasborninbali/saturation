#!/usr/bin/env python3
"""kappa_poisson_percfg.py — conj-007 (need-007): поконфигурационная проверка L ≤ 2·N·e^{−λ}(1 + λ + λ²/2), где L — число пустых клеток с κ³ ≤ 2,
N — число пустых клеток, λ — средняя κ³ конфигурации. usage: python3 kappa_poisson_percfg.py n runs seed [ФАЙЛ …]"""
import sys, math, random, itertools, re
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from rigid_a280537 import grow, coplanar
from kappa_general import read_pts
def stats(S, n):
    Sset = set(S); cells = [c for c in itertools.product(range(n), repeat=3) if c not in Sset]
    trip = list(itertools.combinations(S, 3)); kap = [sum(1 for t in trip if coplanar(q, *t)) for q in cells]
    lam = sum(kap) / len(kap); L = sum(1 for k in kap if k <= 2); return lam, L, len(cells)
def bound(lam, N): return 2 * N * math.exp(-lam) * (1 + lam + lam * lam / 2)
n, runs, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); rnd = random.Random(seed)
viol = 0; worst = 0.0; rows = []
for r in range(runs):
    out = grow(n, rnd); S = out[0] if isinstance(out, tuple) else out
    lam, L, N = stats(S, n); b = bound(lam, N); ratio = L / b if b > 0 else float('inf'); worst = max(worst, ratio)
    if L > b: viol += 1
    rows.append((len(S), round(lam, 2), L, round(b, 1)))
print(f"n={n}, {runs} случайных максимальных (seed {seed}): нарушений L > 2·N·Pois(≤2; λ): {viol} ({viol/runs:.1%}); max L/граница = {worst:.2f}")
print("  примеры (|S|, λ, L, граница):", rows[:6])
for path in sys.argv[4:]:
    S = read_pts(path); hdr = re.search(r'\bn=(\d+)', open(path).readline()); nn = int(hdr.group(1)) if hdr else max(max(p) for p in S) + 1
    lam, L, N = stats(S, nn); print(f"{path.rsplit('/',1)[-1]}: n={nn} |S|={len(S)} λ={lam:.2f} L={L} граница={bound(lam, N):.3f} — {'держится' if L <= bound(lam, N) else 'НАРУШЕНО'}")
