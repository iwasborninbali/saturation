#!/usr/bin/env python3
"""rigid_a280537.py — conj-006: жёсткость (нет замены одной точки) у случайных максимальных конфигураций без четырёх компланарных в [n]³.
Жадный рост: добавляем случайную допустимую клетку (κ³ = 0 — ни одна тройка S не компланарна с ней), κ³ ведётся инкрементально;
по достижении максимальности — прямой счёт: для каждой точки p считаем κ после удаления (минус тройки через p) и смотрим, ожила ли
какая-нибудь клетка кроме p. usage: python3 rigid_a280537.py n runs seed"""
import sys, random, itertools, collections
def coplanar(p, a, b, c):
    u = [a[i]-p[i] for i in range(3)]; v = [b[i]-p[i] for i in range(3)]; w = [c[i]-p[i] for i in range(3)]
    return u[0]*(v[1]*w[2]-v[2]*w[1]) - u[1]*(v[0]*w[2]-v[2]*w[0]) + u[2]*(v[0]*w[1]-v[1]*w[0]) == 0
def grow(n, rnd):
    cells = [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]
    S = []; kap = {c: 0 for c in cells}; occ = set()
    while True:
        alive = [c for c in cells if c not in occ and kap[c] == 0]
        if not alive: return S, kap
        q = rnd.choice(alive)
        for a, b in itertools.combinations(S, 2):
            for c in cells:
                if c not in occ and c != q and coplanar(c, q, a, b): kap[c] += 1
        S.append(q); occ.add(q)
def rigid(S, kap, n):
    cells = [c for c in ((x, y, z) for x in range(n) for y in range(n) for z in range(n)) if c not in set(S)]
    revive_pts = 0
    for p in S:
        rest = [s for s in S if s != p]
        for c in cells:
            if kap[c] == 0: continue
            thru = sum(1 for a, b in itertools.combinations(rest, 2) if coplanar(c, p, a, b))
            if kap[c] - thru == 0: revive_pts += 1; break
    return revive_pts == 0
if __name__ == "__main__":
    n, runs, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); rnd = random.Random(seed)
    sizes = collections.Counter(); rig = collections.Counter()
    for r in range(runs):
        S, kap = grow(n, rnd); m = len(S); sizes[m] += 1; rig[(m, rigid(S, kap, n))] += 1
        if (r + 1) % 20 == 0: print(f"  {r+1} конфигураций… размеры {dict(sorted(sizes.items()))}", flush=True)
    tot = sum(sizes.values()); nonrigid = sum(v for (m, rg), v in rig.items() if not rg)
    print(f"n={n}, {runs} максимальных конфигураций: размеры {dict(sorted(sizes.items()))}; нежёстких {nonrigid} = {nonrigid/tot:.3f}")
    for m in sorted(sizes): print(f"  размер {m}: {sizes[m]} шт., жёстких {rig[(m, True)]}, нежёстких {rig[(m, False)]}")
