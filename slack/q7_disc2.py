"""How far is the rich-line structure from the PG(2,q) 'partition through a point' regularity?"""
import math
from collections import Counter, defaultdict
from itertools import combinations
def build(p, ks):
    h=(p-1)//2; X=lambda a: a if a<=h else a-p; pts=[]
    for c in ks:
        c%=p
        for a in range(1,p):
            b=(c*pow(a,-1,p))%p
            for r in (0,1):
                for s in (0,1):
                    x,y=X(a)+r*p, b+s*p
                    if -h<=x<=(3*p-1)//2 and 0<=y<=2*p-1: pts.append((x,y,c))
    return pts
def rich(pts):
    L=defaultdict(set)
    for i in range(len(pts)):
        for j in range(i+1,len(pts)):
            x1,y1,_=pts[i]; x2,y2,_=pts[j]; dx,dy=x2-x1,y2-y1
            g=math.gcd(abs(dx),abs(dy)); dx//=g; dy//=g
            if dx<0 or (dx==0 and dy<0): dx,dy=-dx,-dy
            L[(dx,dy,dy*x1-dx*y1)].add(i); L[(dx,dy,dy*x1-dx*y1)].add(j)
    return {k:v for k,v in L.items() if len(v)>=3}
print("system            p   |V|   #rich  incid/|V|  pairs-on-rich/all-pairs   Bose-cover: mean |union of rich lines thru v|/(|V|-1)")
for ks,name in [((1,),"ONE hyperbola  "),((1,-1),"TWO hyperbolae ")]:
    for p in [11,13,17,19,23,29]:
        pts=build(p,ks); R=rich(pts); n=len(pts)
        inc=sum(len(v) for v in R.values())
        pairs=sum(len(v)*(len(v)-1)//2 for v in R.values())
        thru=defaultdict(set)
        for v in R.values():
            for i in v: thru[i]|= (v-{i})
        cov=sum(len(thru[i]) for i in range(n))/n/(n-1)
        z=sum(1 for i in range(n) if i not in thru)
        print(f"{name} {p:3d} {n:5d} {len(R):6d}   {inc/n:6.3f}    {pairs}/{n*(n-1)//2} = {pairs/(n*(n-1)/2):.3f}      {cov:.3f}   (pts on no rich line: {z})")
