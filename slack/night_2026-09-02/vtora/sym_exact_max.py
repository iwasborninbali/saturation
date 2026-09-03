#!/usr/bin/env python3
"""sym_exact_max.py — точный максимум H-инвариантного множества в [n]³ без четырёх компланарных для подгрупп H ⊂ O_h (нумерация cube_strata.py),
перебором по орбитам (DFS с отсечением по компланарности; годится, когда максимум мал — классы с инверсией или отражением, lem-003).
usage: python3 sym_exact_max.py n c1,c2,… [макс. глубина]   → для каждого класса: |H|, инверсия/отражение, точный максимум (и пример)"""
import sys, itertools; sys.path.insert(0, __file__.rsplit('/', 1)[0] + '/..'); sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cube_strata import all_matrices, subgroup_classes, orbits
from kappa_general import coplanar
INV = (-1,0,0,0,-1,0,0,0,-1)
def det(M): return M[0]*(M[4]*M[8]-M[5]*M[7]) - M[1]*(M[3]*M[8]-M[5]*M[6]) + M[2]*(M[3]*M[7]-M[4]*M[6])
def is_refl(M): return det(M) == -1 and M[0]+M[4]+M[8] == 1
def clean_add(S, new):
    allp = S + new
    for i in range(len(S), len(allp)):
        for a, b, c in itertools.combinations(allp[:i] + allp[i+1:], 3):
            if coplanar(allp[i], a, b, c): return False
    return True
def exact_max(n, H, depth_cap):
    cells, idx, orb_of, orbs = orbits(H, n)
    orbs = [o for o in orbs if clean_add([], o)]          # орбиты, чистые сами по себе
    orbs.sort(key=len, reverse=True)
    best = [0, []]
    def dfs(i, S, k):
        if len(S) > best[0]: best[0], best[1] = len(S), list(S)
        if k >= depth_cap: return
        rest = sum(len(o) for o in orbs[i:])
        if len(S) + rest <= best[0]: return
        for j in range(i, len(orbs)):
            if clean_add(S, orbs[j]): dfs(j + 1, S + orbs[j], k + 1)
    dfs(0, [], 0)
    return best
if __name__ == "__main__":
    n = int(sys.argv[1]); want = [int(x) for x in sys.argv[2].split(',')]; cap = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    cl = subgroup_classes(all_matrices())
    for ci in want:
        H = cl[ci]; m, ex = exact_max(n, H, cap)
        tag = ("inv " if INV in H else "") + ("refl" if any(is_refl(M) for M in H) else "")
        print(f"n={n} c{ci:02d} |H|={len(H):2d} {tag:9s} точный максимум (глубина орбит ≤ {cap}) = {m}  пример: {sorted(ex)}", flush=True)
