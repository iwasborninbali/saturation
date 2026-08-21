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
print("ПРОМАХ, ДЕЛЁННЫЙ НА n  — линеен ли он?")
print("  n :  промах   промах/n")
for n in range(4,21):
    e=lnpred(n,2*n)-log(A[n]); print(f"  {n:2d}: {e:7.3f}   {e/n:6.3f}")
print("\nПредсказание эвристики для m=2n дальше (некалиброванное):")
for n in (20,30,40,46,50,60,80,100,120,150):
    print(f"  n={n:4d}: ln(предсказано)={lnpred(n,2*n):10.2f}")
print("\nГде ln(предсказано) переходит через ноль:")
lo,hi=20,400
while hi-lo>1:
    mid=(lo+hi)//2
    if lnpred(mid,2*mid)>0: lo=mid
    else: hi=mid
print(f"  без калибровки: последнее n с положительным предсказанием = {lo}")
