"""Quick check (second solver): k=-1 groups, types, Klein-orbits, overlaps between used orbits, cover accounting.
P = {(x,y) in [-h,3h+1]x[0,2p-1] : xy = ±1 mod p}.  +1 group G_d = points on lines x-y=c, c=d mod p; -1 group G'_e: x+y=c, c=e mod p.
Klein orbit of the +1 group at d: Omega_d = G_d u G_{-d} u G'_d u G'_{-d}.  Type = sorted line profile."""
import sys
from collections import defaultdict
def run(p):
    h=(p-1)//2
    pts=[(x,y) for x in range(-h,3*h+2) for y in range(0,2*p) if (x*y)%p in (1,p-1)]
    S=set(pts)
    plus=defaultdict(lambda: defaultdict(list)); minus=defaultdict(lambda: defaultdict(list))
    for (x,y) in pts:
        plus[(x-y)%p][x-y].append((x,y)); minus[(x+y)%p][x+y].append((x,y))
    def prof(g): return tuple(sorted((len(v) for v in g.values()),reverse=True))
    ptype={d:prof(plus[d]) for d in plus}; mtype={e:prof(minus[e]) for e in minus}
    # sanity: R'(G_d) = G'_d, R(G_d)=G'_{-d}
    for d in list(plus)[:5]:
        assert ptype[d]==mtype[d]==mtype[(-d)%p]==ptype[(-d)%p], (d,ptype[d],mtype[d])
    def orbit(d):
        pts_=set()
        for g in (plus[d],plus[(-d)%p],minus[d],minus[(-d)%p]):
            for v in g.values(): pts_.update(v)
        return frozenset(pts_)
    used={}  # orbit rep -> (type, saving)
    for d in plus:
        t=ptype[d]
        if t in ((8,4,4),(7,5,3,1)):
            rep=min(d,(-d)%p)
            if rep in used: continue
            used[rep]=(t,orbit(d))
    n8=sum(1 for r in used if used[r][0]==(8,4,4)); n7=len(used)-n8
    # rows closure & sizes
    for r,(t,O) in used.items():
        assert len(O)==64,(p,r,t,len(O))
        rows=defaultdict(int)
        for (x,y) in O: rows[y]+=1
        assert all(v==4 for v in rows.values()), (p,r,'not row closed')
    # overlaps
    mult=defaultdict(int)
    for r,(t,O) in used.items():
        for q in O: mult[q]+=1
    Ov=sum(m-1 for m in mult.values())
    U=len(mult)
    # pairwise overlaps by type
    reps=list(used); pairs=defaultdict(int); pairs_pts=defaultdict(int)
    for i in range(len(reps)):
        for j in range(i+1,len(reps)):
            a=used[reps[i]][1]&used[reps[j]][1]
            if a:
                key=tuple(sorted((used[reps[i]][0][0],used[reps[j]][0][0])))
                pairs[key]+=1; pairs_pts[key]+=len(a)
    # cover accounting: value = 2*#lines(all lines of used groups) + #singletons(1-lines not covered otherwise) + 2*(rows outside U)
    lines=[]; covered=set()
    for r,(t,O) in used.items():
        d=r
        for g in (plus[d],plus[(-d)%p],minus[d],minus[(-d)%p]):
            for c,v in g.items():
                if len(v)>=2: lines.append(v); covered.update(v)
    singles=[q for q in mult if q not in covered]
    nrows_out=2*(p-1)-U//4
    value=2*len(lines)+len(singles)+2*nrows_out
    naive=4*(p-1)-8*n8-4*n7
    print(f"p={p}: 8-orbits={n8} 7-orbits={n7} |U|={U} Ov={Ov} value={value} = 4(p-1)-{4*(p-1)-value}  naive(disjoint)=4(p-1)-{4*(p-1)-naive}  overlaps by type pairs:{dict(pairs)} pts:{dict(pairs_pts)}")
    # cover accounting for 7-orbits only, and 8 only
    return
for p in map(int,sys.argv[1:]): run(p)
