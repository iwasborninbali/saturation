"""block_bound_all.py — sharper block bound: for each block B (run of consecutive QRs) compute the exact maximum
lawful subset of B with respect to ALL lines contained in B (mixed 2+1 lines included — they are valid inside B).
Sum over blocks is a valid upper bound for alpha(P_{-1}) and is <= the +-1-only version."""
import sys
from collections import defaultdict
from math import gcd
from ortools.sat.python import cp_model

def blocks(p):
    h=(p-1)//2
    pts=[(x,y) for x in range(-h,3*h+2) for y in range(0,2*p) if (x*y)%p in (1,p-1)]
    byres=defaultdict(set)
    for q in pts:
        byres[('p',(q[0]-q[1])%p)].add(q); byres[('m',(q[0]+q[1])%p)].add(q)
    orb={}
    for d in range(0,(p+1)//2):
        O=byres[('p',d%p)]|byres[('p',(-d)%p)]|byres[('m',d%p)]|byres[('m',(-d)%p)]
        if O: orb[(d*d)%p]=O
    seen=set(); out=[]
    for x in orb:
        if x in seen: continue
        y=x
        while (y-4)%p in orb and (y-4)%p!=x: y=(y-4)%p
        C=[]; z=y
        while z in orb and z not in seen: seen.add(z); C.append(z); z=(z+4)%p
        out.append(sorted(set().union(*[orb[t] for t in C])))
    return pts,out

def beta_all(B, tl=600):
    idx={q:i for i,q in enumerate(B)}; lines=defaultdict(set)
    for i in range(len(B)):
        for j in range(i+1,len(B)):
            (x1,y1),(x2,y2)=B[i],B[j]; dx,dy=x2-x1,y2-y1
            g=gcd(abs(dx),abs(dy)) or 1; dx,dy=dx//g,dy//g
            if dx<0 or (dx==0 and dy<0): dx,dy=-dx,-dy
            lines[(dx,dy,dy*x1-dx*y1)]|={i,j}
    L=[sorted(m) for m in lines.values() if len(m)>=3]
    m=cp_model.CpModel(); v=[m.NewBoolVar(f"x{i}") for i in range(len(B))]
    for mem in L: m.Add(sum(v[i] for i in mem)<=2)
    m.Maximize(sum(v))
    s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=tl; s.parameters.num_search_workers=8
    st=s.Solve(m)
    return int(s.ObjectiveValue()), int(s.BestObjectiveBound()), s.StatusName(st), len(L)

p=int(sys.argv[1]); tl=float(sys.argv[2]) if len(sys.argv)>2 else 600
pts,Bs=blocks(p)
tot=0
for B in sorted(Bs,key=len,reverse=True):
    val,bnd,st,nl=beta_all(B,tl)
    print(f"  block |B|={len(B):4d} lines={nl:5d}  max={val} bound={bnd} [{st}]", flush=True)
    tot+=bnd
print(f"p={p}: |P|={len(pts)} blocks={len(Bs)}  SUM of block bounds = {tot}  ({tot/(p-1):.4f}(p-1))   [conjecture: alpha <= {3*(p-1)+6}]")
