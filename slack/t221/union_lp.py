"""union_lp.py (second solver, 19.08) — can a seven-orbit be used TOGETHER with its neighbour?
Orbit Omega_d = {q in P : +-d in {r+(q), r-(q)}}, r+ = x-y, r- = x+y mod p.  Neighbours: e^2 = d^2 +- 4 (Lemma neighbours).
For a union U of orbits (closed under rows and columns) the local certificate is
   LP(U) = max sum x_q, x in [0,1]^U, sum_{q in l} x_q <= 2 for every row, column and slope-+-1 line meeting U.
Saving of U = |U|/2 - LP(U)  (the trivial cover by rows gives |U|/2).  Single orbits: good 32-24 = 4, seven 32-28 = 4.
Question: for adjacent pairs (|U| = 96) is the saving 8 (additive) or less?
usage: python3 slack/t221/union_lp.py p [p ...]"""
import sys
from collections import defaultdict
import numpy as np
from scipy.optimize import linprog

def build(p):
    h=(p-1)//2
    pts=[(x,y) for x in range(-h,3*h+2) for y in range(0,2*p) if (x*y)%p in (1,p-1)]
    return pts

def orbit(pts,p,d):
    return [q for q in pts if (q[0]-q[1])%p in (d%p,(-d)%p) or (q[0]+q[1])%p in (d%p,(-d)%p)]

def lp(U):
    idx={q:i for i,q in enumerate(U)}; n=len(U)
    lines=defaultdict(list)
    for (x,y) in U:
        lines[('r',y)].append(idx[(x,y)]); lines[('c',x)].append(idx[(x,y)])
        lines[('d',x-y)].append(idx[(x,y)]); lines[('a',x+y)].append(idx[(x,y)])
    L=[m for m in lines.values() if len(m)>=3]
    A=np.zeros((len(L),n))
    for i,m in enumerate(L):
        for j in m: A[i,j]=1
    r=linprog(-np.ones(n),A_ub=A,b_ub=2*np.ones(len(L)),bounds=[(0,1)]*n,method='highs')
    return -r.fun

def types(p):
    inv=lambda x: pow(x,p-2,p); h=(p-1)//2; X=lambda u: u if u<=h else u-p
    sig=defaultdict(list); tau=defaultdict(list)
    for t in range(1,p):
        sig[(t-inv(t))%p].append(t); tau[(t+inv(t))%p].append(t)
    typ={}
    for d in range(1,p):
        if len(sig[d])==2 and len(tau[d])==2:
            a=sig[d][0]; b=tau[d][0]
            ss=(X(a)>0)!=(X(inv(a))>0); ts=(X(b)>0)==(X(inv(b))>0)
            typ[d]='8' if (ss and ts) else ('7' if (ss or ts) else '6')
    return typ

def run(p):
    pts=build(p); typ=types(p)
    xtyp={}
    for d,t in typ.items(): xtyp[(d*d)%p]=(t,min(d,p-d))
    res=defaultdict(list)
    for x,(t,d) in sorted(xtyp.items()):
        if t not in '78': continue
        O=orbit(pts,p,d); s1=len(O)//2-lp(O); res['single_'+t].append((d,len(O),s1))
        for dx in (4,p-4):
            y=(x+dx)%p
            if y in xtyp and xtyp[y][0] in '78':
                t2,e=xtyp[y]
                if (t,d)>(t2,e): continue
                U=sorted(set(O)|set(orbit(pts,p,e)))
                res['pair_'+''.join(sorted(t+t2))].append((d,e,len(U),len(U)//2-lp(U)))
    for k in sorted(res):
        v=res[k]
        if k.startswith('single'):
            print(f"  p={p} {k}: n={len(v)} sizes={sorted(set(a[1] for a in v))} savings={sorted(set(round(a[2],3) for a in v))}")
        else:
            print(f"  p={p} {k}: n={len(v)} |U|={sorted(set(a[2] for a in v))} savings={sorted(set(round(a[3],3) for a in v))}")
for p in map(int,sys.argv[1:]):
    run(p)
