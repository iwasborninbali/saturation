"""verify_anisotropic.py — независимая проверка обобщённой конструкции: для анизотропной бинарной квадратичной формы Q над F_p
множество {(x, y, Q(x,y) mod p)} из p² точек не содержит трёх коллинеарных (в R³).
Механизм: вдоль прямой с примитивным направлением (a,b) координата z ≡ Q(x0,y0) + t·B((x0,y0),(a,b)) + t²·Q(a,b) (mod p);
коллинеарность в R³ требует аффинности по t, значит Q(a,b) ≡ 0, что для анизотропной Q даёт (a,b) ≡ (0,0) — противоречие.
Проверяет перебором ВСЕХ троек.  usage: verify_anisotropic.py [p ...]"""
import sys
from itertools import combinations
def nonresidue(p):
    for d in range(2, p):
        if pow(d, (p-1)//2, p) == p-1: return d
def collinear_free(p, Q):
    pts = [(x, y, Q(x, y) % p) for x in range(p) for y in range(p)]
    for a, b, c in combinations(pts, 3):
        u = (b[0]-a[0], b[1]-a[1], b[2]-a[2]); v = (c[0]-a[0], c[1]-a[1], c[2]-a[2])
        if (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]) == (0, 0, 0):
            return (a, b, c)
    return None
for p in (map(int, sys.argv[1:]) if len(sys.argv) > 1 else (3, 5, 7, 11, 13)):
    d = nonresidue(p)
    forms = [(f"x^2-{d}y^2 (universal: d nonresidue)", lambda x, y, d=d: x*x - d*y*y),
             ("x^2+y^2 (anisotropic iff p=3 mod 4)", lambda x, y: x*x + y*y),
             ("x^2+xy+y^2 (anisotropic iff p=2 mod 3)", lambda x, y: x*x + x*y + y*y)]
    for name, Q in forms:
        bad = collinear_free(p, Q)
        print(f"p={p:3d} {name:42s}: {'no collinear triple ✓' if bad is None else 'FAILS, e.g. ' + str(bad)}", flush=True)
