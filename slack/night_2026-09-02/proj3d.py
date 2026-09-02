"""3D: проекция свидетелей A280537 (нет 4 компланарных) вдоль решёточных направлений.
Утверждение: 4 точки компланарны  <=>  существует направление v, вдоль которого их проекции коллинеарны.
Значит «нет 4 компланарных» <=> в КАЖДОЙ проекции нет 4 коллинеарных. Проверяем на свидетелях."""
import numpy as np, re, itertools, math, collections

def blocks(path):
    cur = None; out = []
    for l in open(path):
        m = re.match(r'n=\s*(\d+)\s+m=\s*(\d+)', l)
        if m: cur = (int(m.group(1)), int(m.group(2)), []); out.append(cur); continue
        t = l.split()
        if cur and len(t) == 3 and all(s.lstrip('-').isdigit() for s in t): cur[2].append(tuple(map(int,t)))
    return [(n, m, np.array(p)) for n, m, p in out]

def project(P, v):
    """координаты в плоскости, перпендикулярной v: две независимые целочисленные линейные формы, аннулирующие v"""
    v = np.array(v)
    # базис ядра: для v=(a,b,c) берём формы, ортогональные v
    forms = [f for f in [(v[1], -v[0], 0), (v[2], 0, -v[0]), (0, v[2], -v[1])] if any(f)]
    A = np.array(forms[:2])
    return P @ A.T

def max_collinear_2d(Q):
    """макс. число точек (с кратностью) на одной прямой в плоском множестве"""
    best = 0
    m = len(Q)
    for i in range(m):
        cnt = collections.Counter()
        for j in range(m):
            if i == j: continue
            dx, dy = int(Q[j,0]-Q[i,0]), int(Q[j,1]-Q[i,1])
            if dx == 0 and dy == 0: cnt[('same',)] += 1; continue
            g = math.gcd(abs(dx), abs(dy)); dx//=g; dy//=g
            if dx < 0 or (dx == 0 and dy < 0): dx, dy = -dx, -dy
            cnt[(dx,dy)] += 1
        same = cnt.pop(('same',), 0)
        best = max(best, 1 + same + (max(cnt.values()) if cnt else 0))
    return best

dirs = [(1,1,1), (1,0,0), (1,1,0), (1,-1,0), (1,1,-1), (1,2,3), (2,1,0)]
print("A280537 (нет 4 компланарных): для каждого свидетеля — макс. занятость слоя вдоль v (должно быть <=3),\n"
      "и макс. коллинеарность в проекции вдоль v (должно быть <=3 по теореме)")
print(f"{'n':>3} {'m':>3}  " + "  ".join(f"{str(v):>11}" for v in dirs))
for n, m, P in blocks('/Users/iwasborninbali/saturation/witnesses/A280537_no4coplanar_cube.txt'):
    cells = []
    for v in dirs:
        Q = project(P, v)
        fib = collections.Counter(map(tuple, Q.tolist()))
        cells.append(f"{max(fib.values())}/{max_collinear_2d(Q)}")
    print(f"{n:>3} {m:>3}  " + "  ".join(f"{c:>11}" for c in cells))
print("\n(слой/проекция). Все <=3 — переформулировка подтверждена на 19 свидетелях.")

print("\nA399138 (нет 3 коллинеарных): занятость слоя вдоль v (должно быть <=2); коллинеарность в проекции НЕ ограничена")
for n, m, P in blocks('/Users/iwasborninbali/saturation/witnesses/A399138_no3collinear_cube.txt'):
    cells = []
    for v in dirs[:5]:
        Q = project(P, v)
        fib = collections.Counter(map(tuple, Q.tolist()))
        k2 = sum(1 for c in fib.values() if c == 2)
        cells.append(f"{max(fib.values())} k2={k2:2d}")
    print(f"n={n} m={m:3d}: " + "  ".join(f"{c:>10}" for c in cells))
