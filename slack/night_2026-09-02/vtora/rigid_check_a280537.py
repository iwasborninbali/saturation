#!/usr/bin/env python3
"""rigid_check_a280537.py — жёсткость свидетеля A280537 (нет четырёх компланарных) ПРЯМЫМ счётом (лемма о κ здесь не работает):
κ³(q) — число троек S, компланарных с пустой q; после удаления p: κ³_p(q) = κ³(q) − #{пар {a,b} ⊂ S∖p: q,p,a,b компланарны};
клетка оживает ⟺ κ³_p(q) = 0. Печатает: min κ³, число заменяемых точек, число оживающих клеток, и есть ли ДОПУСТИМАЯ клетка без удаления
(немаксимальность). usage: python3 rigid_check_a280537.py ФАЙЛ [ФАЙЛ …]"""
import sys, itertools, collections
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from kappa_general import read_pts, coplanar
for path in sys.argv[1:]:
    S = read_pts(path); Sset = set(S)
    import re
    hdr = re.search(r'\bn=(\d+)', open(path).readline()); n = int(hdr.group(1)) if hdr else max(max(p) for p in S) + 1
    cells = [c for c in itertools.product(range(n), repeat=3) if c not in Sset]
    kap = {c: 0 for c in cells}
    for t in itertools.combinations(S, 3):
        for c in cells:
            if coplanar(c, *t): kap[c] += 1
    alive0 = [c for c in cells if kap[c] == 0]
    swappable = 0; revived = 0
    for p in S:
        rest = [s for s in S if s != p]; got = False
        for c in cells:
            if kap[c] == 0: continue
            thru = sum(1 for a, b in itertools.combinations(rest, 2) if coplanar(c, p, a, b))
            if kap[c] - thru == 0: revived += 1; got = True
        swappable += got
    print(f"{path.rsplit('/',1)[-1]}: n={n} m={len(S)} min κ³={min(kap.values()) if cells else None} "
          f"{'НЕ МАКСИМАЛЬНА: допустимых клеток ' + str(len(alive0)) if alive0 else ('ЖЁСТКО' if swappable == 0 else 'НЕЖЁСТКО')} "
          f"заменяемых {swappable}/{len(S)} оживающих клеток {revived}")
