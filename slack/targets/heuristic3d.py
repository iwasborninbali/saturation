"""heuristic3d.py — прямая проверка эвристики независимости в ТРЁХМЕРИИ, по СЧЁТУ, а не по порогу.

Эвристика оценивает число правильных M-множеств как C(N,M)*exp(-C(M,4)*p), где p — доля
компланарных четвёрок среди всех. Истина здесь известна точно: полное перечисление максимумов.

Сравнение по счёту прямее, чем по порогу: порог — это место, где оценка пересекает единицу,
и он наследует всю ошибку оценки, не показывая её величины.
"""
import sys, itertools
from math import comb, exp, log10

def coplanar_fraction(n):
    cells=[(x,y,z) for x in range(n) for y in range(n) for z in range(n)]
    N=len(cells); tot=comb(N,4); bad=0
    for a,b,c,d in itertools.combinations(cells,4):
        ux,uy,uz=b[0]-a[0],b[1]-a[1],b[2]-a[2]
        vx,vy,vz=c[0]-a[0],c[1]-a[1],c[2]-a[2]
        wx,wy,wz=d[0]-a[0],d[1]-a[1],d[2]-a[2]
        if ux*(vy*wz-vz*wy)-uy*(vx*wz-vz*wx)+uz*(vx*wy-vy*wx)==0: bad+=1
    return N,tot,bad

for n,M,truth in [(3,8,16),(4,10,10960)] + ([(5,13,int(sys.argv[1]))] if len(sys.argv)>1 else []):
    N,tot,bad=coplanar_fraction(n)
    p=bad/tot
    logest=(sum(log10(N-i) for i in range(M)) - sum(log10(i+1) for i in range(M))
            - comb(M,4)*p/log(10) if False else 0)
    import math
    logest=math.log10(comb(N,M)) - comb(M,4)*p*math.log10(math.e)
    d=log10(truth)-logest
    print(f"n={n} M={M}: клеток {N}, компланарных четвёрок {bad} из {tot} = {p:.6f}")
    print(f"    истина {truth}  оценка 10^{logest:.2f}   log10(истина/оценка) = {d:+.3f}")
