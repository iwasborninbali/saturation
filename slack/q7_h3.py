"""H3 stability test, ONE hyperbola: how far can a lawful set of size 3(p-1)-t be from ALL maximum sets?
d(S) = min over maxima M of |S \ M|.  We compute max_S d(S) for |S| = 3(p-1)-t."""
import math,sys,time
from collections import defaultdict
from itertools import combinations
from satmax import build, rich, solve, cnf_atleast
import subprocess
def atmost_sub(idx, U, nv):
    """Sinz at-most-U over the literals x_i, i in idx (positive lits)."""
    cl=[]; n=len(idx)
    if U>=n: return [],nv
    if U==0:
        return [[-i] for i in idx], nv
    s={}
    for i in range(1,n+1):
        for j in range(1,U+1):
            nv+=1; s[(i,j)]=nv
    L=[idx[i-1] for i in range(1,n+1)]
    cl.append([-L[0], s[(1,1)]])
    for j in range(2,U+1): cl.append([-s[(1,j)]])
    for i in range(2,n+1):
        cl.append([-L[i-1], s[(i,1)]]); cl.append([-s[(i-1,1)], s[(i,1)]])
        for j in range(2,U+1):
            cl.append([-L[i-1], -s[(i-1,j-1)], s[(i,j)]]); cl.append([-s[(i-1,j)], s[(i,j)]])
        cl.append([-L[i-1], -s[(i-1,U)]])
    return cl,nv
def run(p):
    pts=build(p,(1,)); n=len(pts); R=rich(pts)
    base=[]
    for L in R:
        for t3 in combinations(L,3): base.append([-(t3[0]+1),-(t3[1]+1),-(t3[2]+1)])
    A=3*(p-1)
    # enumerate maxima
    maxima=[]; blocking=[]
    while True:
        m=solve(n,base,A,blocking,tmp=f"/tmp/h{p}.cnf")
        if m is None: break
        maxima.append(set(m)); blocking.append([-v for v in m])
    print(f"p={p}: |V|={n}, alpha={A}, #maxima={len(maxima)}",flush=True)
    for t in range(0,6):
        K=A-t
        best=0
        for d in range(1,K+1):
            card,nv=cnf_atleast(n,K,n)
            cls=list(base)+card
            ok=True
            for M in maxima:
                idx=sorted(M)
                c2,nv=atmost_sub(idx,K-d,nv)
                if c2 is None: ok=False;break
                cls+=c2
            with open(f"/tmp/h{p}d.cnf","w") as f:
                f.write(f"p cnf {nv} {len(cls)}\n")
                for c in cls: f.write(" ".join(map(str,c))+" 0\n")
            r=subprocess.run(["kissat","-q",f"/tmp/h{p}d.cnf"],capture_output=True,text=True)
            if "s SATISFIABLE" in r.stdout: best=d
            else: break
        print(f"   t={t}: |S|={K}, max_S min_M |S\\M| = {best}   (t itself = {t})",flush=True)
for p in [11,13,17,19]:
    run(p)
