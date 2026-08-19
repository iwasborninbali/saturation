"""lp_spread.py — where does the 0.47 spread of LP(all)/(p-1) live?
Our theorem: LP(1) = sum over blocks (runs of consecutive QRs) of the block LP.  So the fluctuation of LP(1) is
PREDICTED by the run-signature composition of p (an explicit QR statistic).  The mixed 2+1 lines add the rest.
We split:  LP(1)/(p-1)  and  D(p) := (LP(1) - LP(all))/(p-1)   [the linear value of all weak mixed lines]
and report their spreads separately, together with the arithmetic invariants s, p mod 8, m8/p."""
import sys
from collections import defaultdict
from math import gcd
import numpy as np
from scipy.optimize import linprog

def pts_of(p):
    h=(p-1)//2
    return [(x,y) for x in range(-h,3*h+2) for y in range(0,2*p) if (x*y)%p in (1,p-1)]

def lp(pts, all_slopes):
    idx={q:i for i,q in enumerate(pts)}; lines=defaultdict(set)
    if all_slopes:
        for i in range(len(pts)):
            for j in range(i+1,len(pts)):
                (x1,y1),(x2,y2)=pts[i],pts[j]; dx,dy=x2-x1,y2-y1
                g=gcd(abs(dx),abs(dy)) or 1; dx,dy=dx//g,dy//g
                if dx<0 or (dx==0 and dy<0): dx,dy=-dx,-dy
                lines[(dx,dy,dy*x1-dx*y1)]|={i,j}
    else:
        for (x,y) in pts:
            lines[('r',y)].add(idx[(x,y)]); lines[('c',x)].add(idx[(x,y)])
            lines[('d',x-y)].add(idx[(x,y)]); lines[('a',x+y)].add(idx[(x,y)])
    L=[sorted(m) for m in lines.values() if len(m)>=3]
    A=np.zeros((len(L),len(pts)))
    for i,m in enumerate(L):
        for j in m: A[i,j]=1
    r=linprog(-np.ones(len(pts)),A_ub=A,b_ub=2*np.ones(len(L)),bounds=[(0,1)]*len(pts),method='highs')
    return -r.fun

def invariants(p):
    inv=lambda a: pow(a,p-2,p); h=(p-1)//2; X=lambda u: u if u<=h else u-p
    sig=defaultdict(list); tau=defaultdict(list)
    for t in range(1,p):
        sig[(t-inv(t))%p].append(t); tau[(t+inv(t))%p].append(t)
    m8=0
    for d in range(1,p):
        if len(sig[d])==2 and len(tau[d])==2:
            a=sig[d][0]; b=tau[d][0]
            if ((X(a)>0)!=(X(inv(a))>0)) and ((X(b)>0)==(X(inv(b))>0)): m8+=1
    s = 2 if p%4==1 else 1
    # run structure: number of maximal runs of consecutive QRs and the largest
    QR={(x*x)%p for x in range(1,p)}|{0}
    seen=set(); runs=[]
    for t in range(p):
        if t in seen or t not in QR: continue
        z=t
        while (z-1)%p in QR: z=(z-1)%p
        R=[]; y=z
        while y in QR and y not in seen: seen.add(y); R.append(y); y=(y+1)%p
        if len(R)>=2: runs.append(len(R))
    return s, p%8, m8/p, len(runs), max(runs) if runs else 0

def primes(a,b): return [q for q in range(a,b+1) if q>2 and all(q%d for d in range(2,int(q**.5)+1))]
rows=[]
for p in primes(int(sys.argv[1]), int(sys.argv[2])):
    P=pts_of(p); l1=lp(P,False); la=lp(P,True)
    s,p8,m8,nr,mr=invariants(p)
    rows.append((p,l1/(p-1),la/(p-1),(l1-la)/(p-1),s,p8,m8,nr,mr))
    print(f"p={p:4d} LP(1)/(p-1)={l1/(p-1):.4f} LP(all)/(p-1)={la/(p-1):.4f} D={(l1-la)/(p-1):.4f} "
          f"s={s} p%8={p8} m8/p={m8:.4f} runs={nr} maxrun={mr}", flush=True)
a=np.array([[r[1],r[2],r[3]] for r in rows])
print(f"\nspread LP(1)/(p-1): {a[:,0].min():.4f}..{a[:,0].max():.4f}  (range {a[:,0].max()-a[:,0].min():.4f}, sd {a[:,0].std():.4f})")
print(f"spread LP(all)/(p-1): {a[:,1].min():.4f}..{a[:,1].max():.4f}  (range {a[:,1].max()-a[:,1].min():.4f}, sd {a[:,1].std():.4f})")
print(f"spread D (mixed-line value): {a[:,2].min():.4f}..{a[:,2].max():.4f}  (range {a[:,2].max()-a[:,2].min():.4f}, sd {a[:,2].std():.4f}, mean {a[:,2].mean():.4f})")
