"""КРИВАЯ СМЕРТИ: сколько клеток куба остаётся ЖИВЫМИ после каждого рождения.

Формулировка без точек в заключении. Любые три элемента конфигурации задают плоскость,
и с этого мгновения плоскость МЕРТВА — четвёртому в ней не быть. Любые два задают прямую,
и третьему на ней не быть. После k рождений мертво ровно C(k,3) плоскостей и C(k,2) прямых
(ровно, а не «не более»: плоскость несёт <=3 элементов, значит каждая мертва от одной тройки).

Клетка ЖИВА, если через неё не проходит ни одна мёртвая плоскость и ни одна мёртвая прямая.
Вопрос «сколько точек влезет» превращается в «когда кончается место для рождения».

Меряем на известном свидетеле a(7)>=18: если после 18 рождений живых НОЛЬ — это ровно то,
что должно быть при a(7)=18, и видно, КАК быстро место кончается.
"""
import sys, re
from itertools import combinations
n=7
txt=open(sys.argv[1]).read()
pts=[tuple(int(t) for t in m.groups()) for m in re.finditer(r'\((\d+),(\d+),(\d+)\)', txt)]
print(f"свидетель: {len(pts)} точек")
assert len(set(pts))==len(pts)
cube=[(x,y,z) for x in range(n) for y in range(n) for z in range(n)]
def det3(a,b,c,d):
    u=[b[i]-a[i] for i in range(3)]; v=[c[i]-a[i] for i in range(3)]; w=[d[i]-a[i] for i in range(3)]
    return (u[0]*(v[1]*w[2]-v[2]*w[1])-u[1]*(v[0]*w[2]-v[2]*w[0])+u[2]*(v[0]*w[1]-v[1]*w[0]))
def collinear(a,b,c):
    u=[b[i]-a[i] for i in range(3)]; v=[c[i]-a[i] for i in range(3)]
    return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])==(0,0,0)
print()
print(" k | мёртвых плоскостей | мёртвых прямых | ЖИВЫХ клеток | доля живых")
S=[]
for k,p in enumerate(pts, 1):
    S.append(p)
    alive=0
    for q in cube:
        if q in S: continue
        ok=True
        for a,b in combinations(S,2):
            if collinear(a,b,q): ok=False; break
        if ok:
            for a,b,c in combinations(S,3):
                if det3(a,b,c,q)==0: ok=False; break
        if ok: alive+=1
    from math import comb
    print(f"{k:2d} | {comb(k,3):18d} | {comb(k,2):14d} | {alive:12d} | {100*alive/343:6.2f}%")
