"""THE money statistic: in PG(2,q) an external point sees ALL q+1 arc points (the q+1 lines through it partition
the plane).  Here: how many of the 3(p-1) points of a maximum M_1 of H(1) does a candidate q in H(-1) 'see'
(i.e. lie in a blocking pair with)?"""
import math
from collections import defaultdict
from itertools import combinations
from satmax import build, rich, solve
def one_max(p):
    pts=build(p,(1,)); n=len(pts); R=rich(pts)
    base=[]
    for L in R:
        for t in combinations(L,3): base.append([-(t[0]+1),-(t[1]+1),-(t[2]+1)])
    m=solve(n,base,3*(p-1),[],tmp=f"/tmp/b{p}.cnf")
    return pts,[pts[i-1] for i in m]
for p in [11,13,17,19,23,29,31,37]:
    ptsall,M1=one_max(p)
    h=(p-1)//2; X=lambda a: a if a<=h else a-p
    P2=[]
    for a in range(1,p):
        b=((-1)*pow(a,-1,p))%p
        for r in (0,1):
            for s in (0,1):
                x,y=X(a)+r*p, b+s*p
                if -h<=x<=(3*p-1)//2 and 0<=y<=2*p-1: P2.append((x,y))
    M=[(x,y) for (x,y,_) in M1]
    stats=[];B=[]
    for q in P2:
        seen=set(); nb=0
        for i in range(len(M)):
            for j in range(i+1,len(M)):
                (x1,y1),(x2,y2)=M[i],M[j]
                if (x2-x1)*(q[1]-y1)==(y2-y1)*(q[0]-x1):
                    nb+=1; seen.add(i); seen.add(j)
        stats.append(len(seen)); B.append(nb)
    n=len(M)
    print(f"p={p}: |M1|={n}=3(p-1), |P2|={len(P2)};  points of M1 SEEN by q: mean {sum(stats)/len(stats):.2f} max {max(stats)} min {min(stats)}  -> fraction of M1 seen: {sum(stats)/len(stats)/n:.4f};  blocking pairs B(q): mean {sum(B)/len(B):.2f} max {max(B)}, #(B=0)={sum(1 for b in B if b==0)}",flush=True)
