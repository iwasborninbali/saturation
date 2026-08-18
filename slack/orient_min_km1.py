"""vertical-pair model for k=-1: for each a in F_p^*, class kappa_a=(a,1/a) takes both lifts in column X_a + r_a p, class R'(kappa_a)=(a,-1/a)
takes both lifts in column X_a + (1-r_a) p.  V(r) = number of collinear triples of S(r).  Brute force over all r (2^{p-1})."""
import sys, itertools, time
import numpy as np
from math import gcd
p=int(sys.argv[1]); h=(p-1)//2; N=2*p
X=lambda u: (u%p) if (u%p)<=h else (u%p)-p   # least absolute residue
def Y(u): v=u%p; return v                       # rep in [1,p-1] (y coordinate base)
inv=lambda a: pow(a,-1,p)
As=list(range(1,p))
# per class a: the two possible column choices (r=0: X_a, r=1: X_a+p) in grid coords x = X + h; rows y: Y(1/a) and Y(1/a)+p for kappa; Y(-1/a), +p for R'(kappa)
def pts_for(a, r):
    xa=X(a)+h
    yk=Y(inv(a)); ym=Y(-inv(a))
    col_k = xa + r*p; col_m = xa + (1-r)*p
    return [(col_k,yk),(col_k,yk+p),(col_m,ym),(col_m,ym+p)]
# enumerate all candidate points and index them
allpts={}
for a in As:
    for r in (0,1):
        for q in pts_for(a,r): allpts.setdefault(q,len(allpts))
n=len(allpts); idx=allpts
# collinear triples among all candidate points (each point belongs to exactly one class a and one r? a point (col_k, yk): col_k determines a and r)
# find lines with >=3 candidates
from collections import defaultdict
lines=defaultdict(list); P=list(allpts.keys())
for i in range(n):
    x1,y1=P[i]
    for j in range(i+1,n):
        x2,y2=P[j]; dx,dy=x2-x1,y2-y1; g=gcd(abs(dx),abs(dy)); dx//=g; dy//=g
        if dx<0 or (dx==0 and dy<0): dx,dy=-dx,-dy
        lines[(dx,dy,dx*y1-dy*x1)]
for i in range(n):
    x,y=P[i]
    for (dx,dy,c) in list(lines.keys()):
        pass
# faster: group points by line key over all pairs
lines=defaultdict(set)
for i in range(n):
    x1,y1=P[i]
    for j in range(i+1,n):
        x2,y2=P[j]; dx,dy=x2-x1,y2-y1; g=gcd(abs(dx),abs(dy)); dx//=g; dy//=g
        if dx<0 or (dx==0 and dy<0): dx,dy=-dx,-dy
        lines[(dx,dy,dx*y1-dy*x1)].update((i,j))
rich=[sorted(m) for m in lines.values() if len(m)>=3]
# each point -> (class index, r): point (x,y): a from column: X = x-h mod p (as least residue) -> a ; r = 1 if x-h > h else 0 for kappa; but a point may belong to kappa_a with r or R'(kappa_a) with 1-r
owner={}
for ai,a in enumerate(As):
    for r in (0,1):
        q=pts_for(a,r)
        owner[q[0]]=(ai,r); owner[q[1]]=(ai,r); owner[q[2]]=(ai,r); owner[q[3]]=(ai,r)   # all four points present iff r_a = r
# assignments: r in {0,1}^{p-1}; S(r) = union over a of pts_for(a, r_a). A point q is in S iff r_{owner a} == owner r.
M=len(As); nass=1<<M
# build for each point the (a, rbit); point present iff bit a of assignment == rbit
pt_a=np.array([owner[q][0] for q in P]); pt_r=np.array([owner[q][1] for q in P])
ass=np.arange(nass,dtype=np.int64)
present=((ass[:,None]>>pt_a[None,:])&1)==pt_r[None,:]     # nass x n boolean
# triples: for each rich line, count C(k,3) where k = number of present points on it
V=np.zeros(nass,dtype=np.int64)
for mem in rich:
    k=present[:,mem].sum(axis=1)
    V+= k*(k-1)*(k-2)//6
print(f"p={p}: candidates {n}, rich lines {len(rich)}, assignments {nass}: min V = {V.min()}, mean {V.mean():.1f}, max {V.max()}; #assignments attaining min: {(V==V.min()).sum()}; quantiles: {np.percentile(V,[1,10,50])}")
