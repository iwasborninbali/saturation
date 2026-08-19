"""alpha23_decide.py — decision form of the O(1) premise at p=23 (k=-1).
Published conjecture: alpha(P_k) <= 3(p-1)+6, i.e. alpha(23) <= 72.  Known: 69/70 <= alpha(23) <= 74.
We ask the DECISION questions "is there a lawful set of size >= m?" for m = 73, 72, 71, ... — usually far
easier than optimisation.  INFEASIBLE at 73 => the premise survives at p=23; FEASIBLE => it is refuted."""
import sys
from collections import defaultdict
from math import gcd
from ortools.sat.python import cp_model

def build(p, cs=(1,-1)):
    h=(p-1)//2; S={c%p for c in cs}
    pts=[(x,y) for x in range(-h,3*h+2) for y in range(0,2*p) if (x*y)%p in S]
    lines=defaultdict(set)
    for i in range(len(pts)):
        for j in range(i+1,len(pts)):
            (x1,y1),(x2,y2)=pts[i],pts[j]; dx,dy=x2-x1,y2-y1
            g=gcd(abs(dx),abs(dy)) or 1; dx,dy=dx//g,dy//g
            if dx<0 or (dx==0 and dy<0): dx,dy=-dx,-dy
            lines[(dx,dy,dy*x1-dx*y1)]|={i,j}
    return pts,[sorted(m) for m in lines.values() if len(m)>=3]

def decide(p, m, tl):
    pts,lines=build(p)
    mdl=cp_model.CpModel(); v=[mdl.NewBoolVar(f"x{i}") for i in range(len(pts))]
    for mem in lines: mdl.Add(sum(v[i] for i in mem)<=2)
    mdl.Add(sum(v)>=m)
    s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=tl; s.parameters.num_search_workers=8
    st=s.Solve(mdl); name=s.StatusName(st)
    wit=[pts[i] for i in range(len(pts)) if st in (cp_model.OPTIMAL,cp_model.FEASIBLE) and s.Value(v[i])]
    print(f"p={p} |P|={len(pts)} lines={len(lines)}  ?exists lawful |S|>={m}: {name}  (witness size {len(wit)})", flush=True)
    if wit: print("   witness:", wit, flush=True)
    return name

if __name__=='__main__':
    p=int(sys.argv[1]); tl=float(sys.argv[2]) if len(sys.argv)>2 else 1800
    for m in (73,72,71):
        r=decide(p,m,tl)
        if r=='INFEASIBLE': continue
        break
