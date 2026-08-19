"""orbit_decomp_one.py — ONE hyperbola: do the rich lines decompose over the V-orbits {kappa, sigma kappa, tau kappa, nu kappa}?
If yes, the maximum 3(p-1) and the classification 9^s are orbit-wise, and stability (H3) is immediate with an explicit constant."""
import sys
from collections import defaultdict
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
def run(p):
    h=(p-1)//2; X=lambda u: u if u<=h else u-p
    inv=lambda a: pow(a,p-2,p)
    cls={}
    for a in range(1,p):
        b=inv(a); cls[a]=(X(a), b)          # base copy (x in [-h,h], y in [1,p-1])
    pts=[]; owner={}
    for a,(x0,y0) in cls.items():
        for r in (0,1):
            for s in (0,1):
                q=(x0+r*p, y0+s*p); pts.append(q); owner[q]=a
    # V-orbits: a -> {a, -1/a (sigma), 1/a (tau), -a (nu)}
    orb={}
    for a in range(1,p):
        o=frozenset({a,(p-inv(a))%p,inv(a),(p-a)%p}); orb[a]=o
    orbits={}
    for a in range(1,p): orbits.setdefault(orb[a],set()).add(a)
    # lines with >=3 points; check each stays inside one orbit
    lines=defaultdict(list)
    for q in pts:
        x,y=q
        lines[('r',y)].append(q); lines[('c',x)].append(q); lines[('d',x-y)].append(q); lines[('a',x+y)].append(q)
    rich=[m for m in lines.values() if len(m)>=3]
    bad=sum(1 for m in rich if len({orb[owner[q]] for q in m})>1)
    # also all other slopes: any 3 collinear points?
    n=len(pts); allbad=0
    idx={q:i for i,q in enumerate(pts)}
    trip=defaultdict(list)
    for i in range(n):
        for j in range(i+1,n):
            (x1,y1),(x2,y2)=pts[i],pts[j]
            dx,dy=x2-x1,y2-y1
            g=np.gcd(abs(dx),abs(dy)) or 1
            dx,dy=dx//g,dy//g
            if dx<0 or (dx==0 and dy<0): dx,dy=-dx,-dy
            c=dy*x1-dx*y1
            trip[(dx,dy,c)].append((pts[i],pts[j]))
    rich_all=[k for k,v in trip.items() if len(v)>=3]
    crossing=0
    for k in rich_all:
        qs={q for pair in trip[k] for q in pair}
        if len({orb[owner[q]] for q in qs})>1: crossing+=1
    # orbit-wise maximum
    tot=0; per=[]
    for O,mem in orbits.items():
        P=[q for q in pts if owner[q] in mem]
        ii={q:i for i,q in enumerate(P)}; L=defaultdict(list)
        for (x,y) in P:
            L[('r',y)].append(ii[(x,y)]); L[('c',x)].append(ii[(x,y)]); L[('d',x-y)].append(ii[(x,y)]); L[('a',x+y)].append(ii[(x,y)])
        LL=[m for m in L.values() if len(m)>=3]
        A=np.zeros((len(LL),len(P)))
        for i,m in enumerate(LL):
            for j in m: A[i,j]=1
        r=milp(c=-np.ones(len(P)),constraints=LinearConstraint(A,-np.inf,2*np.ones(len(LL))),bounds=Bounds(0,1),integrality=np.ones(len(P)))
        v=-r.fun; tot+=v; per.append((len(mem),len(P),int(round(v))))
    from collections import Counter
    print(f"p={p}: orbits={len(orbits)} profile(classes,points,opt)={sorted(Counter(per).items())}")
    print(f"   rich lines (rows/cols/±1) crossing orbits: {bad};  ALL-slope rich lines crossing orbits: {crossing} of {len(rich_all)}")
    print(f"   sum of orbit optima = {int(round(tot))}   vs 3(p-1) = {3*(p-1)}")
for p in map(int,sys.argv[1:]): run(p)
