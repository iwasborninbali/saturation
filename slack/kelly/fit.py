from math import gcd, comb, log
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
    res=[y-(a+c*x) for x,y in zip(xs,ys)]
    return a,c,max(abs(r) for r in res)

print("ЛИНЕЙНАЯ КАЛИБРОВКА промаха по разным хвостам данных:")
fits=[]
for lo in (4,8,11,13,15):
    ns=[n for n in sorted(A) if n>=lo]
    a,c,r=lsq(ns,[E[n] for n in ns])
    fits.append((lo,a,c))
    print(f"  по n>={lo:2d} ({len(ns):2d} точек): промах = {a:+.2f} {c:+.4f}*n   макс.невязка {r:.2f}")

print("\nГДЕ УМИРАЕТ 2n по калиброванной эвристике (ln(предсказано) - промах = 0):")
for lo,a,c in fits:
    prev=None
    for n in range(20,600):
        v=lnpred(n,2*n)-(a+c*n)
        if v<0: print(f"  калибровка по n>={lo:2d}: последнее n = {n-1}"); break
    else: print(f"  калибровка по n>={lo:2d}: не умирает до 600")
print(f"\n  без калибровки вовсе: 399")
print("  известно, что 2n достижимо: все нечётные n<=69, все чётные n<=74 (Фламменкамп)")
