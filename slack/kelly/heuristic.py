from math import gcd, comb, log, exp, pi, sqrt
from collections import defaultdict

def lines_of(n):
    """размеры всех прямых сетки n x n, несущих >=2 точки"""
    sizes=[]
    for a in range(0,n):
        for b in range(-(n-1),n):
            if a==0 and b<=0: continue
            if gcd(abs(a),abs(b))!=1: continue
            g=defaultdict(int)
            for x in range(n):
                for y in range(n):
                    g[b*x-a*y]+=1
            sizes += [v for v in g.values() if v>=2]
    return sizes

def triples(sizes): return sum(comb(k,3) for k in sizes)

def pred_poisson(n,m,T):
    N=n*n
    lam = T*comb(m,3)/comb(N,3)
    return log(comb(N,m)) - lam

def pred_lines(n,m,sizes):
    """каждая прямая независимо: P(|S∩l|<=2); гипергеометрически точно"""
    N=n*n; s=log(comb(N,m))
    for k in sizes:
        if k<3: continue
        p=sum(comb(k,j)*comb(N-k,m-j) for j in range(0,3) if 0<=m-j<=N-k)/comb(N,m)
        if p<=0: return float('-inf')
        s+=log(p)
    return s

A755={2:1,3:2,4:11,5:32,6:50,7:132,8:380,9:368,10:1135,11:1120,12:4348,
      13:3622,14:10568,15:30634,16:46304,17:55576,18:152210,19:258176,20:941580}

print("  n     точных    ln(точн)   ln(пуассон)  ln(прямые)   отн.пуассон  отн.прямые")
rp=[];rl=[]
for n in range(4,21):
    sz=lines_of(n); T=triples(sz); m=2*n
    a=log(A755[n]); p=pred_poisson(n,m,T); l=pred_lines(n,m,sz)
    rp.append((n,p-a)); rl.append((n,l-a))
    print(f"{n:3d} {A755[n]:10d}  {a:9.3f}   {p:9.3f}   {l:9.3f}   {p-a:+9.3f}  {l-a:+9.3f}")

print("\nДРЕЙФ ошибки (разность соседних):")
for name,r in (("пуассон",rp),("прямые",rl)):
    d=[f"{r[i+1][1]-r[i][1]:+.2f}" for i in range(len(r)-1)]
    print(f"  {name:8s}: {' '.join(d)}")
