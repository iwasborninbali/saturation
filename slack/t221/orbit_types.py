"""orbit_types.py — classify V-orbits of ONE hyperbola by their incidence type (which rich lines exist) and check that
optimum / number of maxima / stability constant depend only on that type."""
import sys
from itertools import combinations
from collections import defaultdict
def analyse(p, agg):
    h=(p-1)//2; X=lambda u: u if u<=h else u-p; inv=lambda a: pow(a,p-2,p)
    base={a:(X(a),inv(a)) for a in range(1,p)}
    orbmap={a:frozenset({a,(p-inv(a))%p,inv(a),(p-a)%p}) for a in range(1,p)}
    for O in {o for o in orbmap.values()}:
        P=[(base[a][0]+r*p, base[a][1]+s*p) for a in sorted(O) for r in (0,1) for s in (0,1)]
        n=len(P)
        lines=defaultdict(list)
        for q in P:
            x,y=q
            lines[('r',y)].append(q); lines[('c',x)].append(q); lines[('d',x-y)].append(q); lines[('a',x+y)].append(q)
        prof=tuple(sorted((len(v) for v in lines.values() if len(v)>=3),reverse=True))
        def lawful(S):
            c=defaultdict(int)
            for (x,y) in S:
                for k in (('r',y),('c',x),('d',x-y),('a',x+y)):
                    c[k]+=1
                    if c[k]>2: return False
            return True
        best=0; opt=[]
        for m in range(n,0,-1):
            f=[S for S in combinations(P,m) if lawful(S)]
            if f: best=m; opt=[frozenset(S) for S in f]; break
        cs={}
        for d in (1,2):
            worst=0
            for S in combinations(P,best-d):
                if lawful(S): worst=max(worst,min(len(set(S)-M) for M in opt))
            cs[d]=worst
        agg[(len(O),n,prof)].append((best,len(opt),tuple(sorted(cs.items())),p))
agg=defaultdict(list)
for p in map(int,sys.argv[1:]): analyse(p,agg)
print(f"orbit incidence types found: {len(agg)}")
for k,v in sorted(agg.items(), key=lambda kv:(kv[0][0],kv[0][1])):
    vals={(a,b,c) for a,b,c,_ in v}
    print(f"  classes={k[0]} points={k[1]} richline profile={k[2]}: n={len(v)} (p={sorted({x[3] for x in v})}) -> (opt,#max,c(d))={vals}")
