from math import gcd, comb, log, sqrt, pi
def T(n):
    t=0
    for dx in range(0,n):
        for dy in range(-(n-1),n):
            if dx==0 and dy<=0: continue
            t+=(n-dx)*(n-abs(dy))*(gcd(dx,abs(dy))-1)
    return t
A={4:11,5:32,6:50,7:132,8:380,9:368,10:1135,11:1120,12:4348,13:3622,14:10568,
   15:30634,16:46304,17:55576,18:152210,19:258176,20:941580}
def lnpred(n,m):
    N=n*n; return log(comb(N,m))-T(n)*comb(m,3)/comb(N,3)
E={n:lnpred(n,2*n)-log(A[n]) for n in A}
def lsq(xs,ys):
    k=len(xs); sx=sum(xs); sy=sum(ys); sxx=sum(x*x for x in xs); sxy=sum(x*y for x,y in zip(xs,ys))
    d=k*sxx-sx*sx; c=(k*sxy-sx*sy)/d; a=(sy-c*sx)/k
    return a,c,sqrt(sum((y-(a+c*x))**2 for x,y in zip(xs,ys))/k)
MOD={"n":lambda n:n,"n/ln n":lambda n:n/log(n),"sqrt n":lambda n:sqrt(n),
     "ln n":lambda n:log(n),"n^0.75":lambda n:n**0.75}
for lo in (8,12):
    ns=[n for n in sorted(A) if n>=lo]; ys=[E[n] for n in ns]
    print(f"\nМОДЕЛИ ПРОМАХА по n>={lo} ({len(ns)} точек) — среднеквадратичная невязка:")
    fits={}
    for name,f in MOD.items():
        a,c,r=lsq([f(n) for n in ns],ys); fits[name]=(a,c,r)
        print(f"   промах = {a:+7.2f} {c:+8.4f}*{name:8s}   невязка {r:.3f}")
    if lo==12:
        print("\n  ГДЕ УМИРАЕТ 2n по каждой модели:")
        for name,(a,c,r) in sorted(fits.items(),key=lambda kv:kv[1][2]):
            f=MOD[name]; ans=None
            for n in range(21,4000):
                if lnpred(n,2*n)-(a+c*f(n))<0: ans=n-1; break
            print(f"   {name:8s} (невязка {r:.3f}): последнее n = {ans}")
