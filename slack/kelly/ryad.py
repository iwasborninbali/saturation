import re,sys
from math import gcd, comb, log, sqrt, lgamma
def T(n):
    t=0
    for dx in range(0,n):
        for dy in range(-(n-1),n):
            if dx==0 and dy<=0: continue
            t+=(n-dx)*(n-abs(dy))*(gcd(dx,abs(dy))-1)
    return t
def lnC(N,m): return lgamma(N+1)-lgamma(m+1)-lgamma(N-m+1)
def lnpred(n,m):
    N=float(n*n)
    return lnC(N,m)-T(n)*(m*(m-1.0)*(m-2.0))/(N*(N-1)*(N-2))
EX={(5,8):8242}                      # точное, полный профиль
rows=[]
for l in open(sys.argv[1]):
    g=re.match(r'n=(\d+) m=(\d+) спусков=(\d+): оценка ([0-9.e+]+), отн\.ошибка ([0-9.]+)%, дошло (\d+)',l)
    if not g: continue
    n,m,_,v,relerr,hits=int(g[1]),int(g[2]),int(g[3]),float(g[4]),float(g[5]),int(g[6])
    if hits==0 or v<=0: rows.append((n,m,None,None,None,hits)); continue
    e=lnpred(n,m)-log(v)
    rows.append((n,m,v,e,relerr,hits))
print("РЯД ПРИ ДОЛЕ r = m/2n = 0.80")
print("  n   m        оценка   попаданий  промах ln(пред/оценка)  ±")
for n,m,v,e,relerr,hits in rows:
    if v is None: print(f" {n:3d} {m:3d}   НЕТ ПОПАДАНИЙ — точка не берётся"); continue
    if (n,m) in EX:
        ex=EX[(n,m)]; print(f" {n:3d} {m:3d} {v:13.4e} {hits:9d}  {lnpred(n,m)-log(ex):8.3f}   (ТОЧНОЕ {ex}, оценка промахнулась на {100*(v/ex-1):+.2f}%)")
    else:
        print(f" {n:3d} {m:3d} {v:13.4e} {hits:9d}  {e:8.3f}   ±{relerr/100:.3f}")
ok=[(n,e) for n,m,v,e,r,h in rows if v is not None]
if len(ok)>=3:
    print("\n  прирост промаха на единицу n:")
    for i in range(len(ok)-1):
        (n0,e0),(n1,e1)=ok[i],ok[i+1]
        print(f"    n={n0}->{n1}: {(e1-e0)/(n1-n0):+.4f} на единицу")
    print("\n  Если прирост ЗАТУХАЕТ — множитель ограничен, показатель эвристики верен,")
    print("  и константа pi/sqrt3 устояла на этой форме. Если ПОСТОЯНЕН — показатель неверен.")
