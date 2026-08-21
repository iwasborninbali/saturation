"""Независимая проверка свидетеля. Ничего не импортирует из искавшего кода.
Три разных способа поймать одно и то же нарушение — они должны согласиться."""
import sys, itertools
from fractions import Fraction

path = sys.argv[1]; n = int(sys.argv[2])
pts = []
for ln in open(path):
    ln = ln.split('#')[0].strip()
    if not ln: continue
    x, y, z = map(int, ln.split())
    pts.append((x, y, z))

print(f"файл {path}: точек {len(pts)}")
assert len(set(pts)) == len(pts), "ЕСТЬ ПОВТОРЫ"
for p in pts:
    assert all(0 <= c < n for c in p), f"ВНЕ СЕТКИ {p}"
print(f"  различны и внутри [0,{n})^3: да")

# способ 1: определитель разностей по ВСЕМ четвёркам
bad4 = 0
for a, b, c, d in itertools.combinations(pts, 4):
    u = [b[i]-a[i] for i in range(3)]; v = [c[i]-a[i] for i in range(3)]; w = [d[i]-a[i] for i in range(3)]
    det = (u[0]*(v[1]*w[2]-v[2]*w[1]) - u[1]*(v[0]*w[2]-v[2]*w[0]) + u[2]*(v[0]*w[1]-v[1]*w[0]))
    if det == 0: bad4 += 1
print(f"  способ 1, определитель по всем C({len(pts)},4)={len(list(itertools.combinations(range(len(pts)),4)))} четвёркам: компланарных {bad4}")

# способ 2: векторное произведение по ВСЕМ тройкам
bad3 = 0
for a, b, c in itertools.combinations(pts, 3):
    u = [b[i]-a[i] for i in range(3)]; v = [c[i]-a[i] for i in range(3)]
    cr = (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
    if cr == (0, 0, 0): bad3 += 1
print(f"  способ 2, векторное произведение по всем тройкам: коллинеарных {bad3}")

# способ 3: у каждой тройки строим уравнение плоскости и ищем четвёртую точку в ней
viol = 0
for a, b, c in itertools.combinations(pts, 3):
    u = [b[i]-a[i] for i in range(3)]; v = [c[i]-a[i] for i in range(3)]
    nx = u[1]*v[2]-u[2]*v[1]; ny = u[2]*v[0]-u[0]*v[2]; nz = u[0]*v[1]-u[1]*v[0]
    if (nx, ny, nz) == (0, 0, 0): viol += 1; continue
    d = nx*a[0]+ny*a[1]+nz*a[2]
    for p in pts:
        if p in (a, b, c): continue
        if nx*p[0]+ny*p[1]+nz*p[2] == d: viol += 1; break
print(f"  способ 3, плоскость каждой тройки не несёт четвёртой: нарушений {viol}")

# структура: инвариантность под циклом, суммы координат
S = set(pts)
inv = all(((y, z, x) in S) for (x, y, z) in pts)
sums = {}
for (x, y, z) in pts: sums.setdefault(x+y+z, []).append((x, y, z))
diag = [p for p in pts if p[0] == p[1] == p[2]]
print(f"  инвариантна под (x,y,z)->(y,z,x): {inv}; неподвижных на диагонали: {len(diag)} {diag}")
print(f"  различных сумм координат: {len(sums)} из {len(pts)} точек; размеры классов {sorted(len(v) for v in sums.values())}")

ok = (bad4 == 0 and bad3 == 0 and viol == 0)
print("ВЕРДИКТ:", "СВИДЕТЕЛЬ ЧИСТ" if ok else "БРАК")
sys.exit(0 if ok else 1)
