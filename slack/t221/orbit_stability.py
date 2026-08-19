"""orbit_stability.py — H3 for ONE hyperbola, reduced to a single V-orbit (16 or 8 points, no rich line leaves the orbit).
For every orbit type: (a) the optimum, (b) the number of optimal patterns, (c) the stability constant
   c(d) = max over lawful subsets of size opt-d of min over optimal patterns M of |S \\ M|.
Then: S lawful with |S| = 3(p-1) - t is within sum over deficient orbits of c(d) of a maximum set."""
import sys
from itertools import combinations
from collections import defaultdict
def analyse(p, verbose=True):
    h=(p-1)//2; X=lambda u: u if u<=h else u-p; inv=lambda a: pow(a,p-2,p)
    base={a:(X(a),inv(a)) for a in range(1,p)}
    orbmap={}
    for a in range(1,p): orbmap[a]=frozenset({a,(p-inv(a))%p,inv(a),(p-a)%p})
    orbits=sorted({o for o in orbmap.values()}, key=lambda o: sorted(o))
    res=defaultdict(list)
    for O in orbits:
        P=[(base[a][0]+r*p, base[a][1]+s*p) for a in sorted(O) for r in (0,1) for s in (0,1)]
        n=len(P)
        def lawful(S):
            r=defaultdict(int)
            for (x,y) in S:
                for k in (('r',y),('c',x),('d',x-y),('a',x+y)):
                    r[k]+=1
                    if r[k]>2: return False
            return True
        best=0; opt=[]
        for m in range(n,0,-1):
            found=[S for S in combinations(P,m) if lawful(S)]
            if found: best=m; opt=[frozenset(S) for S in found]; break
        cs={}
        for d in (1,2,3):
            m=best-d
            if m<0: break
            worst=0
            for S in combinations(P,m):
                if not lawful(S): continue
                dist=min(len(set(S)-M) for M in opt)
                worst=max(worst,dist)
            cs[d]=worst
        res[(len(O),n)].append((best,len(opt),cs))
    for key,v in res.items():
        bests={x[0] for x in v}; nopts={x[1] for x in v}; cs={tuple(sorted(x[2].items())) for x in v}
        print(f"p={p} orbit type (classes={key[0]}, points={key[1]}): count={len(v)} opt={bests} #optimal patterns={nopts} stability c(d)={cs}")
for p in map(int,sys.argv[1:]): analyse(p)
