from math import gcd, comb, log

def T_lines(n):
    from collections import defaultdict
    t=0
    for a in range(0,n):
        for b in range(-(n-1),n):
            if a==0 and b<=0: continue
            if gcd(abs(a),abs(b))!=1: continue
            g=defaultdict(int)
            for x in range(n):
                for y in range(n): g[b*x-a*y]+=1
            t+=sum(comb(v,3) for v in g.values() if v>=3)
    return t

def T_pairs(n):
    """независимый способ: тройка = пара концов + точка строго между"""
    t=0
    for dx in range(0,n):
        for dy in range(-(n-1),n):
            if dx==0 and dy<=0: continue
            t += (n-dx)*(n-abs(dy))*(gcd(dx,abs(dy))-1)
    return t

print("СВЕРКА двух способов счёта коллинеарных троек:")
for n in range(3,13):
    a,b=T_lines(n),T_pairs(n)
    print(f"  n={n:2d}: по прямым {a:9d}   по парам {b:9d}   {'сходится' if a==b else 'РАСХОЖДЕНИЕ'}")

A={2:1,3:2,4:11,5:32,6:50,7:132,8:380,9:368,10:1135,11:1120,12:4348,13:3622,
   14:10568,15:30634,16:46304,17:55576,18:152210,19:258176,20:941580}
err={}
for n in range(4,21):
    N=n*n; m=2*n; lam=T_pairs(n)*comb(m,3)/comb(N,3)
    err[n]=log(comb(N,m))-lam-log(A[n])

print("\nПРОМАХ ln(предсказано/точно), раздельно по чётности:")
for name,rng in (("чётные",range(4,21,2)),("нечётные",range(5,21,2))):
    v=[(n,err[n]) for n in rng]
    print(f"  {name}: "+" ".join(f"{n}:{e:.2f}" for n,e in v))
    d=[(v[i+1][0],v[i+1][1]-v[i][1]) for i in range(len(v)-1)]
    print(f"    шаг(+2): "+" ".join(f"{n}:{x:+.3f}" for n,x in d))
    print(f"    шаг*n^2: "+" ".join(f"{x*n*n:.0f}" for n,x in d))
