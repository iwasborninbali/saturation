"""vp_traces.py — vertical-pair model for k=-1 (see pair_bound_notes §20): T(eps) = E + eps^T C eps.  Fast construction of C_p from
the collinear point-triples of P_{-1} (all slopes; lines found by pair hashing), then diagnostics: E, lambda_min/max, spectral bound,
row l1/l2 norms, and normalised traces tr(C^{2k})/(p-1) for k=1,2,3 (trace-method diagnostics).  Validated against slack/vp_quadratic.py.
usage: python3 slack/vp_traces.py p1 p2 ...     (third solver, task T2.10)"""
import sys
import numpy as np
from math import gcd
from itertools import combinations
from collections import defaultdict
def build(p):
    h=(p-1)//2
    X=lambda u: (u%p) if (u%p)<=h else (u%p)-p
    Y=lambda u: (u%p) if (u%p) else p          # rep in [1,p]?? note: y-range is [0,2p-1]; class y in [1,p-1] (never 0)
    inv=lambda a: pow(a,-1,p)
    # candidate points of P_{-1} with (variable a, required bit, position)
    pts=[]   # (x, y, a, bit)
    for a in range(1,p):
        xa=X(a)+h; y1=inv(a)%p; y2=(-inv(a))%p
        for r in (0,1):
            # kappa_a copies with r_a = r: column xa + r p, rows y1, y1+p
            pts.append((xa+r*p, y1, a, r)); pts.append((xa+r*p, y1+p, a, r))
            # R'(kappa_a) = (a, -1/a) copies present iff r_a = 1-r' where its column is xa + r' p; so with r' = 1-r: column xa+(1-r)p, bit r
            pts.append((xa+(1-r)*p, y2, a, r)); pts.append((xa+(1-r)*p, y2+p, a, r))
    n=len(pts); assert n==8*(p-1)
    lines=defaultdict(set)
    for i in range(n):
        x1,y1=pts[i][0],pts[i][1]
        for j in range(i+1,n):
            x2,y2=pts[j][0],pts[j][1]; dx,dy=x2-x1,y2-y1; g=gcd(abs(dx),abs(dy)); dx//=g; dy//=g
            if dx<0 or (dx==0 and dy<0): dx,dy=-dx,-dy
            lines[(dx,dy,dx*y1-dy*x1)].update((i,j))
    E=0.0; C=np.zeros((p-1,p-1)); ntrip=0
    for mem in lines.values():
        if len(mem)<3: continue
        for tri in combinations(sorted(mem),3):
            req={}
            ok=True
            for i in tri:
                a,b=pts[i][2],pts[i][3]
                if a in req and req[a]!=b: ok=False; break
                req[a]=b
            if not ok: continue          # incompatible requirements: triple never present
            ntrip+=1
            vars_=sorted(req); m=len(vars_)
            # indicator = prod (1 + s_a eps_a)/2 with s_a = +1 if bit 0 (eps=+1 <-> r=0) else -1
            s={a:(1 if req[a]==0 else -1) for a in vars_}
            E+=1.0/(1<<m)
            for a,b in combinations(vars_,2):
                C[a-1,b-1]+=s[a]*s[b]/(1<<m)/2; C[b-1,a-1]+=s[a]*s[b]/(1<<m)/2
    return E,C,ntrip
if __name__=="__main__":
    print(" p     E    E/(p-1)  lam_min  lam_max  spec_bound/(p-1)  max_row_l1  max_row_l2  tr(C^2)/(p-1)  tr(C^4)/(p-1)  tr(C^6)/(p-1)  #triples")
    for a in sys.argv[1:]:
        p=int(a); E,C,nt=build(p); n=p-1
        lam=np.linalg.eigvalsh(C); l1=np.abs(C).sum(axis=1).max(); l2=np.sqrt((C**2).sum(axis=1)).max()
        t2=(lam**2).sum()/n; t4=(lam**4).sum()/n; t6=(lam**6).sum()/n
        print(f"{p:3d} {E:8.1f} {E/n:7.3f} {lam[0]:8.3f} {lam[-1]:8.3f} {(E+n*lam[0])/n:10.3f} {l1:11.2f} {l2:11.2f} {t2:13.3f} {t4:13.2f} {t6:13.1f} {nt:8d}", flush=True)
