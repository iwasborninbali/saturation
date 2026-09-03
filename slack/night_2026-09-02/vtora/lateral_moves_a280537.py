#!/usr/bin/env python3
"""lateral_moves_a280537.py — боковые и улучшающие 2-обмены у конфигураций A280537: для каждой пары удаляемых точек R считаем допустимые
относительно S∖R клетки (нет тройки S∖R, компланарной с клеткой), затем ищем максимальное совместимое подмножество допустимых клеток
(попарно и вместе с S∖R без четырёх компланарных; перебор, клеток мало). Боковая 2-замена ⟺ ≥ 2 совместимых; улучшение ⟺ ≥ 3.
Также 1-обмены (жёсткость) для полноты. usage: python3 lateral_moves_a280537.py ФАЙЛ …"""
import sys, itertools, re
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from kappa_general import read_pts, coplanar

def admissible(T, cells):
    trip = list(itertools.combinations(T, 3))
    return [q for q in cells if not any(coplanar(q, *t) for t in trip)]

def max_compatible(T, A):
    """наибольшее k ≤ 3, при котором найдутся k допустимых клеток, добавляемых к T совместно без четырёх компланарных."""
    best = 0
    for k in (1, 2, 3):
        for sub in itertools.combinations(A, k):
            U = list(T) + list(sub); ok = True
            for i in range(len(T), len(U)):
                for a, b, c in itertools.combinations(U[:i] + U[i+1:], 3):
                    if coplanar(U[i], a, b, c): ok = False; break
                if not ok: break
            if ok: best = k; break
        if best < k: break
    return best

for path in sys.argv[1:]:
    S = read_pts(path); hdr = re.search(r'\bn=(\d+)', open(path).readline()); n = int(hdr.group(1)) if hdr else max(max(p) for p in S) + 1
    cells = [c for c in itertools.product(range(n), repeat=3) if c not in set(S)]
    one = 0
    for p in S:
        T = [s for s in S if s != p]
        if admissible(T, cells): one += 1
    lateral = 0; improve = 0; maxadm = 0; maxcomp = 0
    for R in itertools.combinations(S, 2):
        T = [s for s in S if s not in R]; A = admissible(T, cells); maxadm = max(maxadm, len(A))
        if len(A) >= 2:
            k = max_compatible(T, A); maxcomp = max(maxcomp, k)
            if k >= 2: lateral += 1
            if k >= 3: improve += 1
    print(f"{path.rsplit('/',1)[-1]}: n={n} |S|={len(S)} | 1-обмен: точек с оживающей чужой клеткой {one}/{len(S)} ({'ЖЁСТКО' if one == 0 else 'нежёстко'}) | "
          f"2-обмен: пар {len(S)*(len(S)-1)//2}, max допустимых клеток после удаления пары {maxadm}, max совместимых {maxcomp}, "
          f"пар с боковой 2-заменой {lateral}, с улучшением {improve}", flush=True)
