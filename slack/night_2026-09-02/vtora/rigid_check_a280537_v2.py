#!/usr/bin/env python3
"""rigid_check_a280537_v2.py — жёсткость свидетеля A280537 с отсечением из lem-001 §граница:
у НЕколлинеарной пустой клетки q убийцы через одну точку образуют паросочетание ⇒ Δ_p κ³(q) ≤ ⌊(|S|−1)/2⌋, поэтому клетки с
κ³(q) > ⌊(|S|−1)/2⌋ оживить одной точкой нельзя — их проверять не нужно; коллинеарные с парой {a,b} клетки оживают удалением a или b
⟺ у них нет убийцы вне пары. Остальные (хрупкие) клетки — прямой счёт. Выход совпадает с rigid_check_a280537.py (проверено на 16/17/18).
usage: python3 rigid_check_a280537_v2.py ФАЙЛ [ФАЙЛ …]"""
import sys, itertools, collections, re
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from kappa_general import read_pts, coplanar, collinear
for path in sys.argv[1:]:
    S = read_pts(path); Sset = set(S); m = len(S)
    hdr = re.search(r'\bn=(\d+)', open(path).readline()); n = int(hdr.group(1)) if hdr else max(max(p) for p in S) + 1
    cells = [c for c in itertools.product(range(n), repeat=3) if c not in Sset]
    triples = list(itertools.combinations(S, 3))
    kap = {c: 0 for c in cells}
    for t in triples:
        for c in cells:
            if coplanar(c, *t): kap[c] += 1
    thr = (m - 1) // 2; alive0 = sum(1 for c in cells if kap[c] == 0)
    fragile = 0; collinear_cells = 0; revive_pts = set(); skipped = 0
    for q in cells:
        if kap[q] == 0: continue
        pairs = [(a, b) for a, b in itertools.combinations(S, 2) if collinear([q, a, b])]
        if pairs:
            collinear_cells += 1
            K = [set(t) for t in triples if coplanar(q, *t)]
            for a, b in pairs:
                if all({a, b} <= t for t in K): revive_pts.add(a); revive_pts.add(b)
            # неколлинеарные убийцы через другие точки: клетка коллинеарна с парой, но оживить её может и третья точка, если все убийцы через неё
            cnt = collections.Counter(p for t in K for p in t)
            for p, c in cnt.items():
                if c == len(K): revive_pts.add(p)
            continue
        if kap[q] > thr: skipped += 1; continue
        fragile += 1
        K = [set(t) for t in triples if coplanar(q, *t)]
        cnt = collections.Counter(p for t in K for p in t)
        for p, c in cnt.items():
            if c == len(K): revive_pts.add(p)
    status = 'НЕ МАКСИМАЛЬНА' if alive0 else ('ЖЁСТКО' if not revive_pts else 'НЕЖЁСТКО')
    print(f"{path.rsplit('/',1)[-1]}: n={n} m={m} min κ³={min(kap.values())} {status} заменяемых {len(revive_pts)}/{m}; клеток: коллинеарных {collinear_cells}, хрупких (κ³ ≤ {thr}) {fragile}, пропущено по отсечению {skipped} из {len(cells)}")
