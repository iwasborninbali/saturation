#!/usr/bin/env python3
"""kappa_general.py — граница леммы о κ (ателье лемм, нужда 1).

Лемма (прямые). Пусть S — множество точек решётки без k+1 на одной прямой, q — пустая клетка, κ_k(q) — число k-подмножеств S,
лежащих с q на одной прямой («убийцы» q). Тогда удаление любой точки p уменьшает κ_k(q) не больше чем на 1.
Доказательство: убийца q, содержащий p, — это k-подмножество прямой pq; на прямой pq лежит ≤ k−1 точек S кроме p (иначе k+1 на прямой),
значит такое k-подмножество не больше одного. ∎  Следствия те же, что при k=2: жёсткость ⟺ min κ ≥ 2, радиус обмена ≥ min κ.

Граница (плоскости). Для запрета «4 в плоскости» (A280537) убийцы q — тройки S, компланарные с q; тройки через p лежат в плоскостях пучка
через прямую pq, каждая плоскость несёт ≤ 2 точек S кроме p, но плоскостей много ⇒ Δ_p κ³(q) может быть ≥ 2, и лемма ложна.

usage: python3 kappa_general.py plane k n runs seed   — проверка Δκ ≤ 1 на жадных максимальных конфигурациях без k+1 на прямой
       python3 kappa_general.py cube4 ФАЙЛ [ФАЙЛ …]   — max Δ_p κ³(q) на свидетелях A280537 (формат: строки «x y z» или «x,y,z;…»)
"""
import sys, math, random, itertools, collections

def collinear(pts):
    a = pts[0]
    for b in pts[1:]:
        pass
    # все точки на одной прямой ⟺ все векторы от a параллельны первому ненулевому
    d = None
    for b in pts[1:]:
        v = tuple(b[i] - a[i] for i in range(len(a)))
        if all(x == 0 for x in v): return True
        if d is None: d = v; continue
        # параллельность через векторные произведения (2D/3D)
        if len(a) == 2:
            if d[0] * v[1] - d[1] * v[0] != 0: return False
        else:
            if (d[1]*v[2]-d[2]*v[1], d[2]*v[0]-d[0]*v[2], d[0]*v[1]-d[1]*v[0]) != (0, 0, 0): return False
    return True

def coplanar(p, a, b, c):
    u = [a[i]-p[i] for i in range(3)]; v = [b[i]-p[i] for i in range(3)]; w = [c[i]-p[i] for i in range(3)]
    return u[0]*(v[1]*w[2]-v[2]*w[1]) - u[1]*(v[0]*w[2]-v[2]*w[0]) + u[2]*(v[0]*w[1]-v[1]*w[0]) == 0

# ---------- плоскость: нет k+1 на прямой ----------
def kappa_k_map(S, n, k):
    """κ_k(q) для всех клеток q: число k-подмножеств S, коллинеарных с q (перебор k-подмножеств, малые n)."""
    kap = collections.Counter()
    for sub in itertools.combinations(S, k):
        if k >= 2 and not collinear(list(sub)): continue
        # прямая через sub: все клетки решётки на ней
        a, b = sub[0], sub[1]; dx, dy = b[0]-a[0], b[1]-a[1]; g = math.gcd(abs(dx), abs(dy)); dx //= g; dy //= g
        for sgn in (1, -1):
            t = 1 if sgn == 1 else -1
            while True:
                c = (a[0] + t*dx, a[1] + t*dy)
                if not (0 <= c[0] < n and 0 <= c[1] < n): break
                if c not in sub: kap[c] += 1
                t += sgn
        # клетки между/за пределами включены; сама прямая через a и b покрыта обеими ветками, кроме точек sub
    return kap

def greedy_no_kplus1(n, k, rnd):
    """жадный рост: добавляем случайную клетку, не создающую k+1 на прямой (клетка допустима ⟺ κ_k(q) = 0)."""
    S = []
    cells = [(x, y) for x in range(n) for y in range(n)]
    while True:
        kap = kappa_k_map(S, n, k) if len(S) >= k else collections.Counter()
        alive = [c for c in cells if c not in S and kap[c] == 0]
        if not alive: return S
        S.append(rnd.choice(alive))

def plane(k, n, runs, seed):
    rnd = random.Random(seed); worst = 0; checked = 0
    for r in range(runs):
        S = greedy_no_kplus1(n, k, rnd)
        kap = kappa_k_map(S, n, k)
        for p in S:
            T = [s for s in S if s != p]; kapT = kappa_k_map(T, n, k)
            for q in [(x, y) for x in range(n) for y in range(n) if (x, y) not in S]:
                d = kap[q] - kapT[q]; checked += 1
                if d > worst: worst = d
                if d > 1: print(f"КОНТРПРИМЕР: n={n}, k={k}, |S|={len(S)}, p={p}, q={q}, Δκ={d}")
    print(f"плоскость, нет {k+1} на прямой, n={n}, {runs} максимальных конфигураций, проверено пар (p,q): {checked}; max Δκ = {worst}  ({'лемма держится' if worst <= 1 else 'ЛЕММА ЛОЖНА'})")

# ---------- куб: нет 4 компланарных (A280537) ----------
def read_pts(path):
    txt = open(path).read()
    import re
    par = re.findall(r'\((-?\d+),(-?\d+),(-?\d+)\)', "\n".join(l for l in txt.splitlines() if not l.strip().startswith('#')))
    if par: return [tuple(int(x) for x in m) for m in par]
    out = []
    for l in txt.splitlines():
        l = l.strip()
        if not l or l.startswith('#'): continue
        if ';' in l or ',' in l:
            for t in l.strip(';').split(';'):
                if t: out.append(tuple(int(x) for x in t.split(',')))
            break
        else:
            parts = l.split()
            if len(parts) == 3 and all(x.lstrip('-').isdigit() for x in parts): out.append(tuple(int(x) for x in parts))
    return out

def kappa3_map(S, n):
    """κ³(q) = число троек S, компланарных с пустой клеткой q (перебор троек × клеток; n ≤ 10 — секунды)."""
    kap = collections.Counter(); Sset = set(S)
    cells = [(x, y, z) for x in range(n) for y in range(n) for z in range(n) if (x, y, z) not in Sset]
    for a, b, c in itertools.combinations(S, 3):
        for q in cells:
            if coplanar(q, a, b, c): kap[q] += 1
    return kap

def cube4(paths):
    for path in paths:
        S = read_pts(path); n = max(max(p) for p in S) + 1
        kap = kappa3_map(S, n); Sset = set(S)
        cells = [c for c in itertools.product(range(n), repeat=3) if c not in Sset]
        worst = 0; ex = None; hist = collections.Counter(); revived = 0; big = 0; big_collinear = 0
        for p in S:
            T = [s for s in S if s != p]; kapT = kappa3_map(T, n)
            for q in cells:
                d = kap[q] - kapT[q]; hist[d] += 1
                if kapT[q] == 0: revived += 1
                if d == len(S) - 2:
                    big += 1
                    if any(collinear([q, p, s]) for s in T): big_collinear += 1
                if d > worst: worst = d; ex = (p, q, kap[q], kapT[q])
        print(f"{path.rsplit('/',1)[-1]}: n={n}, |S|={len(S)}, min κ³ по пустым = {min(kap[c] for c in cells)}, max Δ_p κ³(q) = {worst}, пример (p, q, κ до, κ после) = {ex}; "
              f"оживлений (κ после = 0) среди пар (p, q): {revived}; пар с Δ = |S|−2: {big}, из них q коллинеарна с p и ещё одной точкой: {big_collinear}; распределение Δκ: {dict(sorted(hist.items()))}")

if __name__ == "__main__":
    if sys.argv[1] == "plane": plane(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
    else: cube4(sys.argv[2:])
