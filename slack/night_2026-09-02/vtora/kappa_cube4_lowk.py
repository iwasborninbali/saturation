#!/usr/bin/env python3
"""kappa_cube4_lowk.py — для свидетелей A280537: (1) лемма 3 границы lem-001: нет двух убийц (троек, компланарных с q) с общей ПАРОЙ у
неколлинеарной q — счёт пар убийц с |K₁ ∩ K₂| = 2; (2) распределение κ³ по пустым клеткам (k ≤ 6 и всё), (3) для хрупких клеток (κ³ ≤ 5)
и для всех клеток — максимальная доля убийц через одну точку. Полный вывод, без обрезки. usage: python3 kappa_cube4_lowk.py ФАЙЛ …"""
import sys, itertools, collections, re
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from kappa_general import read_pts, coplanar, collinear
for path in sys.argv[1:]:
    S = read_pts(path); Sset = set(S)
    hdr = re.search(r'\bn=(\d+)', open(path).readline()); n = int(hdr.group(1)) if hdr else max(max(p) for p in S) + 1
    cells = [c for c in itertools.product(range(n), repeat=3) if c not in Sset]
    triples = list(itertools.combinations(S, 3))
    K = {q: [frozenset(t) for t in triples if coplanar(q, *t)] for q in cells}
    dist = collections.Counter(len(K[q]) for q in cells)
    pairs_checked = shared_pair = 0; shared_pair_collinear = 0
    for q in cells:
        col = any(collinear([q, a, b]) for a, b in itertools.combinations(S, 2))
        for A, B in itertools.combinations(K[q], 2):
            pairs_checked += 1
            if len(A & B) == 2:
                shared_pair += 1
                if col: shared_pair_collinear += 1
    share = {}
    for q in cells:
        cnt = collections.Counter(p for t in K[q] for p in t)
        share[q] = max(cnt.values()) / len(K[q]) if K[q] else 0.0
    low = [q for q in cells if 1 <= len(K[q]) <= 5]
    print(f"{path.rsplit('/',1)[-1]}: n={n} |S|={len(S)} пустых клеток {len(cells)}; min κ³={min(dist)}; распределение κ³ (k ≤ 6): { {k: dist[k] for k in sorted(dist) if k <= 6} }; полное: {dict(sorted(dist.items()))}")
    print(f"  лемма 3: пар убийц проверено {pairs_checked}, с общей парой точек {shared_pair}, из них у клеток, коллинеарных с парой точек S: {shared_pair_collinear}; у неколлинеарных клеток: {shared_pair - shared_pair_collinear}")
    print(f"  хрупких клеток (1 ≤ κ³ ≤ 5): {len(low)}; max по хрупким доли убийц через одну точку: {max((share[q] for q in low), default=0):.3f}; max по всем клеткам: {max(share.values()):.3f}; клеток с долей 1.0 (оживают удалением точки): {sum(1 for q in cells if share[q] == 1.0)}")
