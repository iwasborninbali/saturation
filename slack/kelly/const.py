from math import gcd, comb, log, pi, sqrt, lgamma
def T(n):
    t=0
    for dx in range(0,n):
        for dy in range(-(n-1),n):
            if dx==0 and dy<=0: continue
            t+=(n-dx)*(n-abs(dy))*(gcd(dx,abs(dy))-1)
    return t
def lnC(N,m): return lgamma(N+1)-lgamma(m+1)-lgamma(N-m+1)
def lnpred(n,m,t):
    N=n*n
    return lnC(N,m)-t*(m*(m-1.0)*(m-2.0))/(N*(N-1.0)*(N-2.0))
print("ПОРОГ ПЕРВОГО МОМЕНТА m*(n)/n  — к чему сходится?")
print(f"  ориентиры: пи/кор3 = {pi/sqrt(3):.6f}   (2пи^2/3)^(1/3) = {(2*pi*pi/3)**(1/3):.6f}")
for n in (50,100,200,400,800,1600,3200,6400,12800):
    t=T(n); lo,hi=1.0*n,3.0*n
    while hi-lo>0.5:
        mid=(lo+hi)/2
        if lnpred(n,int(mid),t)>0: lo=mid
        else: hi=mid
    print(f"  n={n:6d}:  m*={lo:9.1f}   m*/n = {lo/n:.6f}")
print("\nТ(n)/n^4 (асимптотика числа коллинеарных троек):")
for n in (100,400,1600,6400): print(f"  n={n:5d}: {T(n)/n**4:.6f}")
