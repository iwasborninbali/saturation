"""Check: used Klein-orbits Omega_d, Omega_e overlap iff e^2 = d^2 ± 4 (mod p); then |overlap| = 32 (8 classes). Also P(clean) statistics."""
import sys
from collections import defaultdict
def run(p):
    h=(p-1)//2
    pts=[(x,y) for x in range(-h,3*h+2) for y in range(0,2*p) if (x*y)%p in (1,p-1)]
    plus=defaultdict(lambda: defaultdict(list)); minus=defaultdict(lambda: defaultdict(list))
    for (x,y) in pts:
        plus[(x-y)%p][x-y].append((x,y)); minus[(x+y)%p][x+y].append((x,y))
    def prof(g): return tuple(sorted((len(v) for v in g.values()),reverse=True))
    ptype={d:prof(plus[d]) for d in plus}
    def orbit(d):
        s=set()
        for g in (plus[d],plus[(-d)%p],minus[d],minus[(-d)%p]):
            for v in g.values(): s.update(v)
        return frozenset(s)
    reps={}
    for d in plus:
        r=min(d,(-d)%p)
        if r not in reps: reps[r]=(ptype[d],orbit(d))
    used=[r for r in reps if reps[r][0] in ((8,4,4),(7,5,3,1))]
    sq={ (x*x)%p for x in range(p)}
    bad=0; npairs=0; sizes=defaultdict(int)
    for i in range(len(used)):
        for j in range(i+1,len(used)):
            d,e=used[i],used[j]
            ov=len(reps[d][1]&reps[e][1])
            nb=((e*e-d*d)%p in (4,p-4))
            if (ov>0)!=nb: bad+=1
            if ov>0: npairs+=1; sizes[ov]+=1
    # clean statistics for 7-orbits and the neighbour rule
    n7=0; clean=0; nb_used=defaultdict(int)
    for d in used:
        if reps[d][0]!=(7,5,3,1): continue
        n7+=1
        # neighbours: e with e^2 = d^2+4 and e^2 = d^2-4
        nbs=[]
        for s in (4,p-4):
            t=(d*d+s)%p
            for e in range(p):
                if (e*e)%p==t: nbs.append(min(e,(-e)%p))
        nbs=set(nbs)
        used_nbs=[e for e in nbs if e in reps and reps[e][0] in ((8,4,4),(7,5,3,1))]
        if not used_nbs: clean+=1
        nb_used[len(used_nbs)]+=1
    print(f"p={p}: used orbits={len(used)}, overlapping pairs={npairs}, sizes={dict(sizes)}, rule violations={bad}; 7-orbits={n7} clean={clean} ({clean/max(n7,1):.2f}) #used-neighbours dist={dict(nb_used)}")
for p in map(int,sys.argv[1:]): run(p)
