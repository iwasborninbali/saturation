"""e_structure.py — third solver: E(p) = (1/8)·#collinear patterns of P_{-1} decomposed into spacing-pattern families (t1,t2,e) with QR switches.
E(p) structure check: collinear point-triples of P_{-1} (three distinct classes, compatible bits) grouped by spacing pattern
(0,t1,t2) along a primitive direction and by the sign pattern e=(e1,e2,e3) (which hyperbola xy≡e_i each point lies on);
prediction: family (t1,t2,e) is present iff Delta = b^2 - 4 w e1 is a QR mod p, where w = uv (mod p) and b = xv+uy are determined by
f(t) = e1 + b t + w t^2 interpolating f(0)=e1, f(t1)=e2, f(t2)=e3 (rationals). Also 4-point lines: pattern (0,t1,t2,t1+t2) needs t1^2+t2^2 QR."""
import sys
from math import gcd
from fractions import Fraction as F
from itertools import combinations
from collections import defaultdict, Counter
def legendre(x, p):
    x %= p
    if x == 0: return 0
    return 1 if pow(x, (p-1)//2, p) == 1 else -1
def run(p):
    h=(p-1)//2
    X=lambda u: (u%p) if (u%p)<=h else (u%p)-p
    inv=lambda a: pow(a,-1,p)
    pts=[]
    for a in range(1,p):
        xa=X(a)+h; y1=inv(a)%p; y2=(-inv(a))%p
        for r in (0,1):
            pts.append((xa+r*p, y1, a, r, 1)); pts.append((xa+r*p, y1+p, a, r, 1))
            pts.append((xa+(1-r)*p, y2, a, r, -1)); pts.append((xa+(1-r)*p, y2+p, a, r, -1))
    n=len(pts); lines=defaultdict(set)
    for i in range(n):
        x1,y1=pts[i][0],pts[i][1]
        for j in range(i+1,n):
            x2,y2=pts[j][0],pts[j][1]; dx,dy=x2-x1,y2-y1; g=gcd(abs(dx),abs(dy)); dx//=g; dy//=g
            if dx<0 or (dx==0 and dy<0): dx,dy=-dx,-dy
            lines[(dx,dy,dx*y1-dy*x1)].update((i,j))
    fam=Counter(); fam4=Counter(); bad=0
    for (dx,dy,c),mem in lines.items():
        m=len(mem)
        if m<3: continue
        mem=sorted(mem, key=lambda i:(pts[i][0],pts[i][1]))
        # parameter t along the line: use x if dx!=0 else y
        def tpar(i): return (pts[i][0]-pts[mem[0]][0])//dx if dx else (pts[i][1]-pts[mem[0]][1])//dy
        for tri in combinations(mem,3):
            req={}; ok=True
            for i in tri:
                a,b=pts[i][2],pts[i][3]
                if a in req and req[a]!=b: ok=False; break
                req[a]=b
            if not ok: continue
            t=[tpar(i) for i in tri]; t0=t[0]; t=[x-t0 for x in t]; e=[pts[i][4] for i in tri]
            # normalise orientation: also the reversed pattern (t2-t) is the same family; take lexicographically smaller
            alt=([0,t[2]-t[1],t[2]],[e[2],e[1],e[0]])
            key=min((tuple(t),tuple(e)),(tuple(alt[0]),tuple(alt[1])))
            fam[key]+=1
        if m>=4:
            for quad in combinations(mem,4):
                t=[tpar(i) for i in quad]; t0=t[0]; t=tuple(x-t0 for x in t); e=tuple(pts[i][4] for i in quad)
                fam4[(t,e)]+=1
    # check predictions
    res=[]
    for (t,e),cnt in sorted(fam.items(), key=lambda kv:-kv[1])[:40]:
        t1,t2=t[1],t[2]; e1,e2,e3=e
        # solve e1 + b t1 + w t1^2 = e2, e1 + b t2 + w t2^2 = e3
        # w = ((e3-e1)/t2 - (e2-e1)/t1)/(t2-t1); b = (e2-e1)/t1 - w t1
        w=(F(e3-e1,t2)-F(e2-e1,t1))/(t2-t1); b=F(e2-e1,t1)-w*t1
        if w==0: pred='degenerate'
        else:
            D=b*b-4*w*e1
            Dp=(D.numerator*pow(D.denominator,-1,p))%p
            pred=legendre(Dp,p)
        res.append((t,e,cnt,str(w),str(D) if w!=0 else '-',pred))
    return fam,fam4,res
if __name__=="__main__":
    for p in map(int,sys.argv[1:]):
        fam,fam4,res=run(p)
        print(f"p={p}: families(t,e) present: {len(fam)}; total patterns {sum(fam.values())}")
        for r in res[:24]: print("   ",r)
        # absent check: for small t1<t2<=6 and all e, count present vs predicted
        agree=dis=0; ex=[]
        for t2 in range(2,9):
            for t1 in range(1,t2):
                for e in [(a,b,c) for a in (1,-1) for b in (1,-1) for c in (1,-1)]:
                    key=min(((0,t1,t2),e),((0,t2-t1,t2),(e[2],e[1],e[0])))
                    present=fam.get(key,0)>0
                    w=(F(e[2]-e[0],t2)-F(e[1]-e[0],t1))/(t2-t1); b=F(e[1]-e[0],t1)-w*t1
                    if w==0: pred=False
                    else:
                        D=b*b-4*w*e[0]; Dp=(D.numerator*pow(D.denominator,-1,p))%p; pred=(legendre(Dp,p)>=0)
                    if present==pred: agree+=1
                    else: dis+=1; ex.append((key,present,pred))
        print("   3-pt families t2<=8: agree",agree,"disagree",dis, ex[:6])
        q4=Counter()
        for (t,e),c in fam4.items(): q4[(t,e)]+=c
        print("   4-point line patterns:", sorted(q4.items(), key=lambda kv:-kv[1])[:8])
