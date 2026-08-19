"""type_determinism.py — is the component saving determined by its TYPE SIGNATURE (sequence of group profiles along the chain)?
Component = maximal chain of residues x = d^2 under x ~ x+4 with G_d nonempty.  Signature = tuple of line-size profiles of the groups
(canonical: min of the sequence and its reverse).  For each component we compute IP(U) (exact) and record signature -> set of savings."""
import sys
from collections import defaultdict
import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds

def run(p, agg, capn=520):
    h=(p-1)//2
    pts=[(x,y) for x in range(-h,3*h+2) for y in range(0,2*p) if (x*y)%p in (1,p-1)]
    byres=defaultdict(set); plus=defaultdict(lambda: defaultdict(int))
    for q in pts:
        byres[('p',(q[0]-q[1])%p)].add(q); byres[('m',(q[0]+q[1])%p)].add(q)
        plus[(q[0]-q[1])%p][q[0]-q[1]]+=1
    prof={d:tuple(sorted(plus[d].values(),reverse=True)) for d in plus}
    orb={}
    for d in range(1,(p+1)//2):
        O=byres[('p',d)]|byres[('p',(-d)%p)]|byres[('m',d)]|byres[('m',(-d)%p)]
        if O: orb[(d*d)%p]=(O,min(d,p-d))
    seen=set(); comps=[]
    for x in orb:
        if x in seen: continue
        y=x
        while (y-4)%p in orb and (y-4)%p!=x: y=(y-4)%p
        C=[]; z=y
        while z in orb and z not in seen:
            seen.add(z); C.append(z); z=(z+4)%p
        comps.append(C)
    for C in comps:
        sig=tuple(prof.get(orb[x][1],()) for x in C)
        sig=min(sig,sig[::-1])
        U=sorted(set().union(*[orb[x][0] for x in C]))
        if len(U)>capn:
            agg[('TOOBIG',len(C))].append(None); continue
        idx={q:i for i,q in enumerate(U)}; lines=defaultdict(list)
        for (x,y) in U:
            lines[('r',y)].append(idx[(x,y)]); lines[('c',x)].append(idx[(x,y)])
            lines[('d',x-y)].append(idx[(x,y)]); lines[('a',x+y)].append(idx[(x,y)])
        L=[m for m in lines.values() if len(m)>=3]
        A=np.zeros((len(L),len(U)))
        for i,m in enumerate(L):
            for j in m: A[i,j]=1
        r=milp(c=-np.ones(len(U)),constraints=LinearConstraint(A,-np.inf,2*np.ones(len(L))),bounds=Bounds(0,1),integrality=np.ones(len(U)))
        v=-r.fun if r.success else None
        agg[sig].append(None if v is None else round(len(U)/2-v,4))

agg=defaultdict(list)
for p in map(int,sys.argv[1:]): run(p,agg)
ambiguous=0; tot=0; sav_tot=0.0
for sig in sorted(agg,key=lambda s:(len(s),str(s))):
    v=[a for a in agg[sig] if a is not None]; tot+=len(agg[sig]); sav_tot+=sum(v)
    if not v: print(f"  {sig}: n={len(agg[sig])} (skipped)"); continue
    s=sorted(set(v)); amb = len(s)>1
    ambiguous+= (1 if amb else 0)
    if amb or len(sig)<=2:
        print(f"  n={len(v):4d} saving={s}  sig={sig}")
print(f"\ncomponents={tot} distinct signatures={len(agg)} AMBIGUOUS signatures={ambiguous}")
