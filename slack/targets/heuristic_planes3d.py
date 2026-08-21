"""heuristic_planes3d.py — какая эвристика ближе к истине: по ЧЕТВЁРКАМ или по ПЛОСКОСТЯМ.

Предсказание второго солвера: в исходной эвристике две ошибки разного знака гасят друг друга —
независимость МЕЖДУ объектами завышает, пересчёт ВНУТРИ объекта занижает. Замена четвёрок на
плоскости чинит только вторую и оставляет первую голой, значит должна быть ХУЖЕ, а не лучше.
В двумерии он это измерил на прямых. Здесь — трёхмерие, на полном перечислении максимумов.

    по четвёркам:  C(N,M)*exp(-C(M,4)*p),   p — доля компланарных четвёрок
    по плоскостям: C(N,M)*ПРОИЗВЕДЕНИЕ по богатым плоскостям P(выбрано не более 3 из k узлов),
                   вероятность ТОЧНАЯ гипергеометрическая
"""
import itertools, math
from math import comb, log10

def planes(n):
    cells = [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]
    seen = {}
    for a, b, c in itertools.combinations(cells, 3):
        u = [b[i] - a[i] for i in range(3)]
        v = [c[i] - a[i] for i in range(3)]
        nx = u[1]*v[2] - u[2]*v[1]; ny = u[2]*v[0] - u[0]*v[2]; nz = u[0]*v[1] - u[1]*v[0]
        if (nx, ny, nz) == (0, 0, 0):
            continue
        d = nx*a[0] + ny*a[1] + nz*a[2]
        g = math.gcd(math.gcd(abs(nx), abs(ny)), math.gcd(abs(nz), abs(d)))
        if g:
            nx, ny, nz, d = nx//g, ny//g, nz//g, d//g
        for t in (nx, ny, nz):
            if t:
                if t < 0:
                    nx, ny, nz, d = -nx, -ny, -nz, -d
                break
        seen[(nx, ny, nz, d)] = 0
    for key in seen:
        nx, ny, nz, d = key
        seen[key] = sum(1 for (x, y, z) in cells if nx*x + ny*y + nz*z == d)
    return len(cells), seen

def quad_frac(n):
    cells = [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]
    tot = comb(len(cells), 4); bad = 0
    for a, b, c, d in itertools.combinations(cells, 4):
        u = [b[i]-a[i] for i in range(3)]; v = [c[i]-a[i] for i in range(3)]; w = [d[i]-a[i] for i in range(3)]
        if u[0]*(v[1]*w[2]-v[2]*w[1]) - u[1]*(v[0]*w[2]-v[2]*w[0]) + u[2]*(v[0]*w[1]-v[1]*w[0]) == 0:
            bad += 1
    return bad / tot

for n, M, truth in [(3, 8, 16), (4, 10, 10960)]:
    N, pl = planes(n); p = quad_frac(n)
    lq = log10(comb(N, M)) - comb(M, 4)*p*math.log10(math.e)
    lp = log10(comb(N, M)); rich = 0
    for key, k in pl.items():
        if k < 4:
            continue
        rich += 1
        s = sum(comb(k, j)*comb(N-k, M-j) for j in range(4) if M-j >= 0 and N-k >= M-j)
        lp += log10(s) - log10(comb(N, M))
    dq = log10(truth) - lq; dp = log10(truth) - lp
    print(f"n={n} M={M}: истина {truth}, богатых плоскостей {rich}")
    print(f"   по четвёркам  10^{lq:6.2f}   промах {dq:+.3f}")
    print(f"   по плоскостям 10^{lp:6.2f}   промах {dp:+.3f}   -> плоскости "
          f"{'ХУЖЕ' if abs(dp) > abs(dq) else 'ЛУЧШЕ'} в {10**abs(abs(dp)-abs(dq)):.1f} раз")
