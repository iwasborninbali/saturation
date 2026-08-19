"""Discriminator statistics for P_k = (H(1) u H(k)) cap G(p): regularity of the line hypergraph."""
import sys, math
from collections import Counter, defaultdict
from itertools import combinations

def build(p, k=-1):
    h=(p-1)//2
    X=lambda a: a if a<=h else a-p
    pts=[]
    for c in (1, k%p):
        for a in range(1,p):
            b=(c*pow(a,-1,p))%p
            x0,y0=X(a), b
            for r in (0,1):
                for s in (0,1):
                    pts.append((x0+r*p, y0+s*p, c))
    # restrict to box G(p) = [-h, 3p-1-h] x [0,2p-1] ... actually HJSW window: x in [-(p-1)/2, (3p-1)/2], y in [0,2p-1]
    box=[(x,y,c) for (x,y,c) in pts if -h<=x<= (3*p-1)//2 and 0<=y<=2*p-1]
    return box

def lines(pts):
    """group points into maximal collinear families"""
    n=len(pts); L=defaultdict(set)
    for i in range(n):
        for j in range(i+1,n):
            x1,y1,_=pts[i]; x2,y2,_=pts[j]
            dx,dy=x2-x1,y2-y1
            g=math.gcd(abs(dx),abs(dy)); dx//=g; dy//=g
            if dx<0 or (dx==0 and dy<0): dx,dy=-dx,-dy
            # canonical line id: direction + signed offset  (dy*x - dx*y = const)
            c=dy*x1-dx*y1
            L[(dx,dy,c)].add(i); L[(dx,dy,c)].add(j)
    return L

for p in [11,13,17,19,23]:
    pts=build(p,-1)
    L=lines(pts)
    sizes=Counter(len(v) for v in L.values())
    rich={kk:v for kk,v in L.items() if len(v)>=3}
    deg=Counter()
    for v in rich.values():
        for i in v: deg[i]+=1
    codeg=Counter()
    for v in rich.values():
        for a,b in combinations(sorted(v),2): codeg[(a,b)]+=1
    triples_only=sum(1 for v in rich.values() if len(v)==3)
    print(f"p={p} |V|={len(pts)} (expect {8*(p-1)}) lines>=3: {len(rich)}  sizes>=3: {sorted((s,c) for s,c in sizes.items() if s>=3)}")
    print(f"   3-pt lines: {triples_only} ({triples_only/len(rich):.3f} of rich); deg: min {min(deg.values())} mean {sum(deg.values())/len(pts):.2f} max {max(deg.values())}")
    print(f"   codegree (pairs in >=1 rich line): {len(codeg)}; max codeg {max(codeg.values())}; codeg dist {Counter(codeg.values())}")
