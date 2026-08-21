import re,sys,glob
from math import gcd,comb,log,sqrt
def T(n):
    t=0
    for dx in range(0,n):
        for dy in range(-(n-1),n):
            if dx==0 and dy<=0: continue
            t+=(n-dx)*(n-abs(dy))*(gcd(dx,abs(dy))-1)
    return t
_T={}
def lnpred(n,m):
    if n not in _T: _T[n]=T(n)
    N=n*n; return log(comb(N,m))-_T[n]*comb(m,3)/comb(N,3)
data={}
for f in glob.glob('/tmp/kelly/*.txt'):
    for l in open(f,errors='replace'):
        g=re.match(r'n=(\d+) m=(\d+) спусков=(\d+): оценка ([0-9.e+]+), отн\.ошибка ([0-9.]+)%, дошло (\d+)',l)
        if not g: continue
        n,m,d,v,er,h=int(g[1]),int(g[2]),int(g[3]),float(g[4]),float(g[5]),int(g[6])
        if v<=0 or h==0: continue
        data.setdefault((n,m),[]).append((v,d,h))
EXACT={(5,8):8242,(6,10):98950,(7,12):471860,(8,14):3892476,(10,18):92734158,(5,9):840}
print("ПОВЕРХНОСТЬ ПРОМАХА  E(n,r) = ln(предсказано) - ln(истинно)")
print("  n   m    r      семян  дошло%   оценка        E        источник")
S={}
for (n,m),vs in sorted(data.items()):
    r=m/(2*n)
    if abs(r*20-round(r*20))>1e-9: continue          # только точные доли, кратные 0.05
    if (n,m) in EXACT:
        val=float(EXACT[(n,m)]); tag="ТОЧНОЕ"; sem=0.0; k=0; hp=100.0
    else:
        v=[x[0] for x in vs]; k=len(v); val=sum(v)/k
        sd=sqrt(sum((x-val)**2 for x in v)/k)/val if k>1 else 0.0
        sem=sd/sqrt(k) if k>1 else 0.0
        hp=100.0*sum(x[2] for x in vs)/sum(x[1] for x in vs)
        tag=f"оценка ±{100*sem:.0f}%" if k>1 else "оценка, ОДНО семя"
    E=lnpred(n,m)-log(val); S[(n,round(r,2))]=E
    print(f" {n:3d} {m:3d}  {r:.2f}  {k:5d}  {hp:6.2f}  {val:11.4e}  {E:+7.3f}   {tag}")
print("\nПО СТОЛБЦАМ (фиксированная доля, растущее n) — вот где ответ:")
for r in (0.70,0.75,0.80,0.85,0.90):
    pts=sorted((n,e) for (n,rr),e in S.items() if abs(rr-r)<1e-9)
    if len(pts)<2: continue
    line=" ".join(f"n={n}:{e:+.2f}" for n,e in pts)
    d=" ".join(f"{(pts[i+1][1]-pts[i][1])/(pts[i+1][0]-pts[i][0]):+.3f}" for i in range(len(pts)-1))
    print(f"  r={r:.2f}: {line}")
    print(f"          прирост на единицу n: {d}")
