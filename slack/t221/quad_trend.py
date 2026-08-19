"""quad_trend.py (second solver) — independent check of the 'quadruple of hyperbolae' claim.
For m hyperbolae H(c), c in C, inside the HJSW box: exact maximum lawful subset (CP-SAT), and the gain over 3(p-1).
The point at issue: is max = 3(p-1) + O(1) (so ratio -> 1.5 N) or does the gain grow linearly in p?"""
import sys
from collections import defaultdict
from ortools.sat.python import cp_model
def solve(p, cs, tl=900):
    h=(p-1)//2
    pts=[(x,y) for x in range(-h,3*h+2) for y in range(0,2*p) if (x*y)%p in {c%p for c in cs}]
    idx={q:i for i,q in enumerate(pts)}
    lines=defaultdict(list)
    for i,(x1,y1) in enumerate(pts):
        for j in range(i+1,len(pts)):
            x2,y2=pts[j]; dx,dy=x2-x1,y2-y1
            from math import gcd
            g=gcd(abs(dx),abs(dy)) or 1; dx,dy=dx//g,dy//g
            if dx<0 or (dx==0 and dy<0): dx,dy=-dx,-dy
            lines[(dx,dy,dy*x1-dx*y1)].append((i,j))
    mdl=cp_model.CpModel()
    v=[mdl.NewBoolVar(f"x{i}") for i in range(len(pts))]
    nl=0
    for k,prs in lines.items():
        mem=sorted({i for pr in prs for i in pr})
        if len(mem)>=3: mdl.Add(sum(v[i] for i in mem)<=2); nl+=1
    mdl.Maximize(sum(v))
    s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=tl; s.parameters.num_search_workers=8
    st=s.Solve(mdl)
    val=int(s.ObjectiveValue()); bound=int(s.BestObjectiveBound())
    return len(pts), nl, val, bound, s.StatusName(st)
CS={'pair':[1,-1],'quad':[1,-1,2,-2]}
for p in map(int,sys.argv[1:]):
    for name,cs in CS.items():
        n,nl,val,bnd,st=solve(p,cs)
        print(f"p={p:3d} {name:5s}: |P|={n:4d} lines={nl:5d} max={val} bound={bnd} [{st}]  ratio={val/(2*p):.3f}N  gain over 3(p-1)={val-3*(p-1):+d}", flush=True)
