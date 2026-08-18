"""pair_structure.py — describe a maximum lawful subset of H(1,p) u H(k,p) in the HJSW box: per-hyperbola counts, copies per
class, per column/row occupancy, which classes lose which copies.  Grid coords x y (x = column offset in [0,2p), y row in [0,2p));
the HJSW box is x0=-(p-1)/2 .. so grid x = X + h where X is the actual coordinate.  usage: python3 slack/pair_structure.py p k file"""
import sys
p=int(sys.argv[1]); k=int(sys.argv[2]) % p; f=sys.argv[3]; h=(p-1)//2
pts=[]
for l in open(f):
    l=l.strip()
    if not l or l.startswith('#'): continue
    x,y=map(int,l.split()[:2]); pts.append((x,y))
S=set(pts); n=len(pts)
def actual(x,y): return (x-h, y)          # HJSW box: X in [-h, 3h+1], Y in [0,2p-1]
def hyp(X,Y):
    r=(X*Y)%p
    return 1 if r==1 else (2 if r==k else 0)
c1=sum(1 for (x,y) in pts if hyp(*actual(x,y))==1); c2=sum(1 for (x,y) in pts if hyp(*actual(x,y))==2)
print(f"p={p} k={k}: |S|={n} = {c1} from H(1) + {c2} from H(k);  3(p-1)={3*(p-1)}, 4(p-1)={4*(p-1)}")
# copies per class
from collections import Counter, defaultdict
cls=defaultdict(list)
for (x,y) in pts:
    X,Y=actual(x,y); cls[(hyp(X,Y), X%p, Y%p)].append((X,Y))
mult=Counter(len(v) for v in cls.values())
allcls=[(1,a,pow(a,-1,p)) for a in range(1,p)]+[(2,a,(k*pow(a,-1,p))%p) for a in range(1,p)]
zero=sum(1 for c in allcls if c not in cls)
print("classes by number of copies used:", dict(sorted(mult.items())), "unused classes:", zero, "of", len(allcls))
# columns and rows occupancy
col=Counter(x for (x,y) in pts); row=Counter(y for (x,y) in pts)
print("columns with 2 points:", sum(1 for v in col.values() if v==2), "with 1:", sum(1 for v in col.values() if v==1), "empty (of 2p-2 nonzero):", 2*p-2-len([c for c in col if (c-h)%p]))
print("rows with 2:", sum(1 for v in row.values() if v==2), "with 1:", sum(1 for v in row.values() if v==1))
# which copy pattern per class: (r,s) in {0,1}^2 relative to base copy
pat=Counter()
for key,v in cls.items():
    hy,a,b=key
    xs=sorted(set(X for X,Y in v)); ys=sorted(set(Y for X,Y in v))
    Xmin=min(X for X,Y in v); Ymin=min(Y for X,Y in v)
    # base copy: representative X in [-h,h], Y in [1,p-1]
    Xb = a if a<=h else a-p; Yb = b
    pat[tuple(sorted(((X-Xb)//p,(Y-Yb)//p) for X,Y in v))]+=1
print("copy patterns (r,s) per class:", dict(pat.most_common()))
# lines with exactly 2 points of S by slope, and rich lines status
from math import gcd
lines=defaultdict(set)
P=list(S)
for i in range(len(P)):
    for j in range(i+1,len(P)):
        (x1,y1),(x2,y2)=P[i],P[j]; dx,dy=x2-x1,y2-y1; g=gcd(abs(dx),abs(dy)); dx//=g; dy//=g
        if dx<0 or (dx==0 and dy<0): dx,dy=-dx,-dy
        lines[(dx,dy,dx*y1-dy*x1)].update([P[i],P[j]])
sl=Counter((dx,dy) for (dx,dy,c),v in lines.items())
print("2-point lines of S by direction (top):", sl.most_common(8))
