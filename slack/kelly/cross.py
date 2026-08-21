from math import gcd, comb, log, sqrt
def T(n):
    t=0
    for dx in range(0,n):
        for dy in range(-(n-1),n):
            if dx==0 and dy<=0: continue
            t+=(n-dx)*(n-abs(dy))*(gcd(dx,abs(dy))-1)
    return t
def lnpred(n,m):
    N=n*n; return log(comb(N,m))-T(n)*comb(m,3)/comb(N,3)
V={n:lnpred(n,2*n) for n in range(5,601)}
print("ln(предсказано) при m=2n — НЕ монотонна, растёт потом падает:")
for n in (5,20,100,200,300,400,450,480,490,492,493,494,500,550,600):
    print(f"   n={n:3d}: {V[n]:9.3f}")
mx=max(V,key=V.get); print(f"\n  максимум при n={mx}")
cr=[n for n in sorted(V) if V[n]<0 and V[n-1]>=0]
print(f"  переходы через ноль: {cr}")
print(f"  => последнее n с положительным предсказанием = {cr[0]-1}")
print(f"  Прелльберг / обзор: эвристика применима при n>=493 — совпадение по целому: {cr[0]==493}")
A={4:11,5:32,6:50,7:132,8:380,9:368,10:1135,11:1120,12:4348,13:3622,14:10568,
   15:30634,16:46304,17:55576,18:152210,19:258176,20:941580}
E={n:lnpred(n,2*n)-log(A[n]) for n in A}
def lsq(xs,ys):
    k=len(xs);sx=sum(xs);sy=sum(ys);sxx=sum(x*x for x in xs);sxy=sum(x*y for x,y in zip(xs,ys))
    d=k*sxx-sx*sx;c=(k*sxy-sx*sy)/d;a=(sy-c*sx)/k
    return a,c,sqrt(sum((y-(a+c*x))**2 for x,y in zip(xs,ys))/k)
MOD={"ln n":log,"sqrt n":sqrt,"n^0.75":lambda n:n**0.75,"n/ln n":lambda n:n/log(n),"n":lambda n:n}
ns=[n for n in sorted(A) if n>=12]
print("\nС КАЛИБРОВКОЙ (сканированием, без двоичного поиска):")
for name,f in MOD.items():
    a,c,r=lsq([f(n) for n in ns],[E[n] for n in ns])
    s=[n for n in range(21,3000) if lnpred(n,2*n)-(a+c*f(n))<0]
    print(f"   {name:8s} невязка {r:.3f}: последнее n = {s[0]-1 if s else '>3000'}")
