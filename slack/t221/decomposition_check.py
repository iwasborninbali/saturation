"""decomposition_check.py (second solver, 19.08) — DOES LP(1) DECOMPOSE OVER COMPONENTS OF THE NEIGHBOUR GRAPH?
Orbits: for a residue d != 0 with G_d nonempty, Omega_d = {q in P : +-d in {r+(q), r-(q)}} (r+ = x-y, r- = x+y mod p).
Adjacency: d ~ e iff e^2 = d^2 +- 4 (Lemma neighbours).  Claim: the components partition P, every row/column/+-1-line lies inside
one component, hence LP(1) = sum over components of LP(U_C) and IP(1) = sum of IP(U_C).
Checks: (1) partition; (2) lines inside components; (3) LP(1) global vs sum of component LPs; (4) IP per component (exact) -> bound."""
import sys
from collections import defaultdict
import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds

def lines_of(U):
    idx={q:i for i,q in enumerate(U)}; lines=defaultdict(list)
    for (x,y) in U:
        lines[('r',y)].append(idx[(x,y)]); lines[('c',x)].append(idx[(x,y)])
        lines[('d',x-y)].append(idx[(x,y)]); lines[('a',x+y)].append(idx[(x,y)])
    return [m for m in lines.values() if len(m)>=3], len(U)

def solve(U, ip=True, cap=400):
    L,n=lines_of(U)
    A=np.zeros((len(L),n))
    for i,m in enumerate(L):
        for j in m: A[i,j]=1
    r=linprog(-np.ones(n),A_ub=A,b_ub=2*np.ones(len(L)),bounds=[(0,1)]*n,method='highs'); vlp=-r.fun
    vip=None
    if ip and n<=cap:
        m=milp(c=-np.ones(n),constraints=LinearConstraint(A,-np.inf,2*np.ones(len(L))),bounds=Bounds(0,1),integrality=np.ones(n))
        if m.success: vip=-m.fun
    return vlp,vip

def run(p):
    h=(p-1)//2
    pts=[(x,y) for x in range(-h,3*h+2) for y in range(0,2*p) if (x*y)%p in (1,p-1)]
    byres=defaultdict(set)
    for q in pts:
        byres[('p',(q[0]-q[1])%p)].add(q); byres[('m',(q[0]+q[1])%p)].add(q)
    # orbits indexed by x = d^2 (d and -d give the same orbit)
    orb={}
    for d in range(0,(p+1)//2):
        O=byres[('p',d)]|byres[('p',(-d)%p)]|byres[('m',d)]|byres[('m',(-d)%p)]
        if O: orb[(d*d)%p]=O
    # components under x ~ x+4
    seen=set(); comps=[]
    for x in orb:
        if x in seen: continue
        y=x
        while (y-4)%p in orb and (y-4)%p!=x: y=(y-4)%p
        C=[]; z=y
        while z in orb and z not in seen:
            seen.add(z); C.append(z); z=(z+4)%p
        comps.append(C)
    U={i:sorted(set().union(*[orb[x] for x in C])) for i,C in enumerate(comps)}
    # (1) partition?
    tot=sum(len(v) for v in U.values()); allpts=set().union(*U.values())
    part = (tot==len(pts)==len(allpts))
    # (2) every line inside one component
    where={}
    for i,v in U.items():
        for q in v: where[q]=i
    lines=defaultdict(list)
    for (x,y) in pts:
        lines[('r',y)].append((x,y)); lines[('c',x)].append((x,y)); lines[('d',x-y)].append((x,y)); lines[('a',x+y)].append((x,y))
    bad=sum(1 for m in lines.values() if len(m)>=3 and len({where[q] for q in m})>1)
    # (3) global LP(1) vs sum
    vlp_glob,_=solve(pts, ip=False)
    s_lp=0.0; s_ip=0.0; sizes=[]
    for i,v in U.items():
        a,b=solve(v, ip=True)
        s_lp+=a; s_ip+=(b if b is not None else a); sizes.append(len(v))
    print(f"p={p}: |P|={len(pts)} components={len(comps)} maxsize={max(sizes)} partition={part} lines_crossing={bad}")
    print(f"   LP(1) global={vlp_glob:.4f}  sum of component LPs={s_lp:.4f}  diff={vlp_glob-s_lp:+.2e}")
    print(f"   sum of component IPs={s_ip:.4f}   =>  alpha <= {s_ip:.0f} = {s_ip/(p-1):.4f}(p-1)   [LP(1)={vlp_glob/(p-1):.4f}(p-1)]")
    return vlp_glob, s_ip, p
for p in map(int,sys.argv[1:]): run(p)
