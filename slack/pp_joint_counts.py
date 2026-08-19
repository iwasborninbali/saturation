import sys, math
from collections import Counter
def counts(p, k):
    plus = Counter(); minus = Counter()
    for t in range(p):
        plus[(pow(t,k,p) - t) % p] += 1; minus[(pow(t,k,p) + t) % p] += 1
    J = Counter(); Mp = Counter(); Mm = Counter(); n=0
    for x in range(1, (p+1)//2):   # one representative per pair {x,-x}
        a = plus[(pow(x,k,p) - x) % p]; b = minus[(pow(x,k,p) + x) % p]
        J[(a,b)] += 1; Mp[a] += 1; Mm[b] += 1; n+=1
    return J, Mp, Mm, n
for (p,k) in [(10007,7),(10009,7),(20011,7),(20011,5),(30011,7)]:
    if math.gcd(k, p-1) != 1: print("skip", p, k); continue
    J, Mp, Mm, n = counts(p,k)
    chi = 0; cells=0
    for (a,b), c in J.items():
        e = Mp[a]*Mm[b]/n
        if e >= 5: chi += (c-e)**2/e; cells+=1
    print(f"p={p} k={k}: n={n} chi2={chi:.1f} over {cells} cells (df≈{(len(Mp)-1)*(len(Mm)-1)})  marg+ {dict(sorted(Mp.items()))}")
