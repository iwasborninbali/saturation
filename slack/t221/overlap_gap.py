"""overlap_gap.py (second solver) — the overlap structure of near-optimal lawful sets (hole H2 / local-algorithm barrier).
OGP signature: the distribution of |S ∩ S'| over near-optimal pairs has a forbidden middle band ("clustered"),
which by Gamarnik–Sudan-type arguments blocks every local algorithm of radius o(diameter).
Control: for ONE hyperbola our stability theorem predicts the structure exactly (maxima differ only on exceptional orbits).
Sampling: CP-SAT with random linear perturbation of the objective, size fixed to alpha - d."""
import sys, random
from collections import defaultdict
from math import gcd
from ortools.sat.python import cp_model

def inst(p, cs):
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

def sample(p, cs, target, nsol=60, tl=25, seed=0):
    pts,lines=inst(p,cs); rnd=random.Random(seed); out=[]
    for s in range(nsol):
        m=cp_model.CpModel(); v=[m.NewBoolVar(f"x{i}") for i in range(len(pts))]
        for mem in lines: m.Add(sum(v[i] for i in mem)<=2)
        m.Add(sum(v)==target)
        w=[rnd.randrange(0,1000) for _ in range(len(pts))]
        m.Maximize(sum(w[i]*v[i] for i in range(len(pts))))
        so=cp_model.CpSolver(); so.parameters.max_time_in_seconds=tl; so.parameters.num_search_workers=4
        so.parameters.random_seed=s
        st=so.Solve(m)
        if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            out.append(frozenset(i for i in range(len(pts)) if so.Value(v[i])))
    return pts,out

def report(p, cs, target, label):
    pts,sols=sample(p,cs,target)
    sols=list(dict.fromkeys(sols))
    if len(sols)<2: print(f"p={p} {label} target={target}: solutions found {len(sols)}"); return
    ov=[]
    for i in range(len(sols)):
        for j in range(i+1,len(sols)):
            ov.append(len(sols[i]&sols[j]))
    ov.sort(); n=len(ov)
    hist=defaultdict(int)
    for o in ov: hist[o]+=1
    dens=[f"{k}:{v}" for k,v in sorted(hist.items())]
    print(f"p={p} {label} target={target}: distinct solutions={len(sols)} overlaps min={ov[0]} med={ov[n//2]} max={ov[-1]} "
          f"(normalised {ov[0]/target:.2f}..{ov[-1]/target:.2f})", flush=True)
    print(f"    histogram: {' '.join(dens[:24])}", flush=True)

if __name__=='__main__':
    for p,a in ((11,30),(13,36),(17,48)):
        report(p,(1,),a,"one-hyperbola max")
    for p,a in ((11,32),(13,40),(17,54)):
        for d in (0,1,2):
            report(p,(1,-1),a-d,f"pair (alpha-{d})")
