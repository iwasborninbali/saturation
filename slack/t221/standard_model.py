"""standard_model.py (second solver) — the STANDARD MODEL of a block: the incidence structure of B_rho depends only on the
xi-chain (descent pattern), so it can be built from real positions instead of a prime.
Model: positions v_1..v_k in (0,1/2) (images of X(u_i)/p); edge i carries the H(1) residues A = v_i+v_{i+1}, B = v_{i+1}-v_i (mod 1)
and their negatives; the class of residue a has base copy (X(a), Y(1/a)), X in (-1/2,1/2), Y in (0,1); lifts (X+r, Y+s), r,s in {0,1};
H(-1) classes are the R-images (1-x, y).  Lines: equal x (column), equal y (row), equal x-y, equal x+y.  Exact rational arithmetic.
xi_i = [g(v_i) > g(v_{i+1})], g(x) = min(x, 1/2-x).   usage: python3 standard_model.py [kmax]"""
import sys, json, random
from fractions import Fraction as F
from collections import defaultdict
from itertools import product
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def X(a):            # centred representative in (-1/2, 1/2)
    a = a - int(a) if a>=0 else a - int(a) + 1
    a = a % 1
    return a-1 if a > F(1,2) else a
def Y(a):            # representative in (0,1)
    return a % 1

def block(vs):
    pts=set()
    for i in range(len(vs)-1):
        A=(vs[i]+vs[i+1])%1; B=(vs[i+1]-vs[i])%1
        for a in (A,B,(-A)%1,(-B)%1):
            inv = {A:B, B:A, (-A)%1:(-B)%1, (-B)%1:(-A)%1}[a]
            x0,y0=X(a),Y(inv)
            if x0==0 or y0==0: return None
            for r in (0,1):
                for s in (0,1):
                    pts.add((x0+r,y0+s)); pts.add((1-(x0+r),y0+s))
    return sorted(pts)

def saving(U):
    idx={q:i for i,q in enumerate(U)}; lines=defaultdict(list)
    for (x,y) in U:
        lines[('r',y)].append(idx[(x,y)]); lines[('c',x)].append(idx[(x,y)])
        lines[('d',x-y)].append(idx[(x,y)]); lines[('a',x+y)].append(idx[(x,y)])
    L=[m for m in lines.values() if len(m)>=3]
    A=np.zeros((len(L),len(U)))
    for i,m in enumerate(L):
        for j in m: A[i,j]=1
    r=milp(c=-np.ones(len(U)),constraints=LinearConstraint(A,-np.inf,2*np.ones(len(L))),bounds=Bounds(0,1),integrality=np.ones(len(U)))
    return len(U)/2-(-r.fun), len(U)

def perm_with_descents(k, S, rnd):
    """a permutation of [k] whose descent set is exactly S (standard construction: increasing runs between descents)."""
    blocks=[]; prev=0
    for d in sorted(S)+[k]:
        blocks.append(list(range(prev+1,d+1))); prev=d
    # assign the largest values to the earliest blocks so that each block ends with a descent
    vals=list(range(1,k+1)); out=[]
    for b in reversed(blocks):
        take=sorted(vals[:len(b)]); vals=vals[len(b):]
        out=take+out
    return out

def positions(xi, rnd, D=None):
    """positions v_i realising the descent pattern xi of g(v_i), generically."""
    k=len(xi)+1; S={i+1 for i,b in enumerate(xi) if b==1}
    pi=perm_with_descents(k,S,rnd)
    if any(((pi[i]>pi[i+1]) != (xi[i]==1)) for i in range(k-1)): return None
    M=1000; Dd=(k+2)*M*97
    vs=[]
    for i,r in enumerate(pi):
        g=F(r*M+rnd.randrange(1,M//2), Dd)          # g in (0,1/4), order = pi, generic
        vs.append(g if rnd.random()<0.5 else F(1,2)-g)
    return vs

def run(kmax=8, tries=3, seed=0, kmin=2):
    rnd=random.Random(seed); TAB={}
    for k in range(kmin,kmax+1):
        for xi in product((0,1),repeat=k-1):
            pass
        for xi in product((0,1),repeat=k-1):
            vals=set()
            for _ in range(tries):
                vs=positions(xi,rnd)
                if vs is None: continue
                U=block(vs)
                if U is None: continue
                s,n=saving(U); vals.add((round(s,6),n))
            TAB[''.join(map(str,xi))]=sorted(vals)
        json.dump({k2:sorted({a[0] for a in v}) for k2,v in TAB.items()}, open('slack/t221/standard_model.json','w'), indent=0)
        print(f"  k={k} done ({len(TAB)} patterns)", flush=True)
    return TAB

if __name__=='__main__':
    kmax=int(sys.argv[1]) if len(sys.argv)>1 else 6
    T=run(kmax)
    amb=[k for k,v in T.items() if len({a[0] for a in v})>1]
    print(f"patterns={len(T)} ambiguous(saving depends on positions)={len(amb)}: {amb[:8]}")
    for k in sorted(T,key=lambda s:(len(s),s))[:40]:
        print(f"  xi={k:9s} -> {T[k]}")
    json.dump({k:(sorted({a[0] for a in v})) for k,v in T.items()}, open('slack/t221/standard_model.json','w'), indent=0)
