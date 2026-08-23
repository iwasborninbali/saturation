# -*- coding: utf-8 -*-
# Объединение H(1) u H(-1) в окне HJSW: m8, LP-сертификаты, точные альфа, блоки, 7-точечные.
import subprocess, sys
from math import gcd
from collections import defaultdict

def primes(a,b):
    return [n for n in range(a,b+1) if n>1 and all(n%d for d in range(2,int(n**.5)+1))]
def is_qr(a,p): return pow(a%p,(p-1)//2,p)==1
def union_pts(p):
    pts=[]
    for x in range(-(p-1)//2,(3*p-1)//2+1):
        if x%p==0: continue
        for y in range(0,2*p):
            r=(x*y)%p
            if r==1 or r==p-1: pts.append((x,y))
    return pts
def diag_counts(pts):
    dp=defaultdict(int); dm=defaultdict(int)
    for x,y in pts: dp[x-y]+=1; dm[x+y]+=1
    return dp,dm

print("=== A. m8(p) для простых 19..1500: положительность и доля ===",flush=True)
bad=[]; samples=[]
for p in primes(19,1500):
    pts=union_pts(p); dp,dm=diag_counts(pts)
    m8p=sum(1 for v in dp.values() if v==8); m8m=sum(1 for v in dm.values() if v==8)
    tot=m8p+m8m
    if tot==0: bad.append(p)
    if p in (499,997,1499) or p<=31: samples.append((p,m8p,m8m,tot,round(tot/p,4),round(m8p/p,4)))
print("  нулевых m8 в 19..1500:", len(bad), bad[:10],flush=True)
print("   p   m8(+) m8(-) сумма  сумма/p  (+)/p    [1/12=0.0833]")
for r in samples: print("  ",r,flush=True)

def rich_all(pts):
    lines=defaultdict(set)
    n=len(pts)
    for i in range(n):
        x1,y1=pts[i]
        for j in range(i+1,n):
            x2,y2=pts[j]
            a=y2-y1;b=x1-x2;g=gcd(abs(a),abs(b));a//=g;b//=g
            if a<0 or (a==0 and b<0):a,b=-a,-b
            lines[(a,b,a*x1+b*y1)].update((i,j))
    return {k:v for k,v in lines.items() if len(v)>=3}

print("=== B. LP-сертификат: LP <= 4(p-1)-4*m8 для p=19..101 ===",flush=True)
from scipy.optimize import linprog
for p in primes(19,101):
    pts=union_pts(p); RL=rich_all(pts); N=len(pts)
    dp,dm=diag_counts(pts); m8=sum(1 for v in dp.values() if v==8)+sum(1 for v in dm.values() if v==8)
    A=[[0]*N for _ in RL]
    for r,(k,L) in enumerate(RL.items()):
        for i in L: A[r][i]=1
    res=linprog([-1.0]*N,A_ub=A,b_ub=[2.0]*len(A),bounds=[(0,1)]*N,method='highs')
    lp=-res.fun; bnd=4*(p-1)-4*m8
    c7=sum(1 for v in dp.values() if v==7)+sum(1 for v in dm.values() if v==7)
    print(f"  p={p:3d}: N={N:3d} прямых {len(RL):4d} m8={m8:2d} 7-точечных={c7:2d}  LP={lp:8.3f}  4(p-1)-4m8={bnd:3d}  {'OK' if lp<=bnd+1e-6 else 'НАРУШЕНИЕ'}  LP/(p-1)={lp/(p-1):.4f}",flush=True)

print("=== C. Точная альфа объединения (alpha2), пока влезает ===",flush=True)
for p in (5,7,11,13,17,19,23):
    pts=union_pts(p); RL=rich_all(pts)
    dp,dm=diag_counts(pts); m8=sum(1 for v in dp.values() if v==8)+sum(1 for v in dm.values() if v==8)
    inp=f"{len(pts)} {len(RL)}\n"+"\n".join(f"{len(L)} "+" ".join(map(str,sorted(L))) for L in RL.values())
    try:
        r=subprocess.run(['/tmp/hjfull/alpha2'],input=inp,capture_output=True,text=True,timeout=900)
        a,nodes=r.stdout.split()
        bnd=4*(p-1)-4*m8
        print(f"  p={p:3d}: alpha={a:>4s} узлов {nodes:>12s}  4(p-1)={4*(p-1):3d}  4(p-1)-4m8={bnd:3d}  {'OK' if int(a)<=bnd else 'НАРУШЕНИЕ ГРАНИЦЫ'}  alpha/(p-1)={int(a)/(p-1):.4f}",flush=True)
    except subprocess.TimeoutExpired:
        print(f"  p={p:3d}: ОБОРВАНО по 900с — точная альфа не взята, честно говорю",flush=True)
        break

print("=== D. Блоки: компоненты (строки/столбцы/диагонали) против пробегов вычетов ===",flush=True)
for p in primes(19,311):
    pts=union_pts(p); n=len(pts)
    # компоненты только по строкам, столбцам и наклонам +-1
    parent=list(range(n))
    def find(x):
        while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
        return x
    def uni(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: parent[ra]=rb
    keys=[defaultdict(list) for _ in range(4)]
    for i,(x,y) in enumerate(pts):
        keys[0][x].append(i); keys[1][y].append(i); keys[2][x-y].append(i); keys[3][x+y].append(i)
    for kd in keys:
        for v in kd.values():
            for j in v[1:]: uni(v[0],j)
    comps=defaultdict(int)
    for i in range(n): comps[find(i)]+=1
    ncomp=len(comps)
    # максимальные пробеги подряд идущих квадратичных вычетов в [1,p-1]
    q=[is_qr(a,p) for a in range(1,p)]
    runs=0; inrun=False
    for v in q:
        if v and not inrun: runs+=1; inrun=True
        elif not v: inrun=False
    sizes=sorted(comps.values())
    div8=all(s%8==0 for s in sizes)
    flag='OK' if ncomp==runs else f'РАСХОЖДЕНИЕ comp={ncomp} runs={runs}'
    if p<=61 or ncomp!=runs: print(f"  p={p:3d}: компонент {ncomp:3d}, пробегов вычетов {runs:3d}  {flag}  размеры кратны 8: {div8}",flush=True)
print("ГОТОВО",flush=True)
