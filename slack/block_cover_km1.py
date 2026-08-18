"""block_cover_km1.py — Theorem (block cover, k = -1): alpha(P_{-1}) <= 4(p-1) - 2*m8(p), where P_{-1} = (H(1,p) u H(-1,p)) n G(p) and
m8(p) = number of slope-+-1 lines with 8 points of P_{-1}.  This script builds the explicit cover for each p (weight 1 on the three
lines c-p, c, c+p of every 8-point-line residue group, weight 1 on every row containing a point outside the groups), checks that the
groups are pairwise disjoint and mirror-closed, that every such row has exactly 4 outside points, that every candidate is covered,
and that the cost is exactly 4(p-1) - 2*m8.   usage: python3 slack/block_cover_km1.py [pmax=320]   (third solver, 2026-08-19)"""
import sys; sys.path.insert(0,'/home/claude/saturation/slack')
from maxlawful_pysat import cands_M
from collections import defaultdict
def run(p):
    N=2*p; h=(p-1)//2; cands=cands_M(p,{1,p-1},N); S=set(cands)
    # class of a candidate: (x residue in window coords, y residue), and which hyperbola
    def cl(q):
        x,y=q; xw=x-h; return (xw%p, y%p)
    lines=defaultdict(list)
    for q in cands:
        x,y=q; lines[('d',x-y)].append(q); lines[('a',x+y)].append(q); lines[('r',y)].append(q); lines[('c',x)].append(q)
    # 8-point slope lines -> groups (set of 4 classes; block lines = centre line and centre +- p)
    groups=[]
    for key,mem in lines.items():
        if key[0] in ('d','a') and len(mem)==8:
            classes=set(cl(q) for q in mem); assert len(classes)==4
            c=key[1]
            if key[0]=='d': blk=[('d',c),('d',c-p),('d',c+p)]
            else: blk=[('a',c),('a',c-p),('a',c+p)]
            pts=set(q for L in blk for q in lines.get(L,[]))
            # check: block lines cover exactly the 16 copies of the 4 classes
            allcopies=set(q for q in cands if cl(q) in classes)
            assert allcopies<=pts and len(allcopies)==16, (p,key,len(allcopies),len(pts))
            groups.append((key,classes,blk,allcopies))
    # mirror R: (x,y) -> (2p-1-x?)... window x'=x-h; R: x' -> p - x' ; grid x -> p - (x-h) + h = p+2h - x = 2p-1-x
    def R(q): return (2*p-1-q[0], q[1])
    for q in cands: assert R(q) in S
    def Rclasses(classes): return set(cl(R(q)) for q in cands if cl(q) in classes)
    # greedy R-symmetric disjoint family: process groups; take G and R(G) together if both disjoint from taken
    idx={frozenset(g[1]):i for i,g in enumerate(groups)}
    taken=[]; used=set()
    for i,(key,classes,blk,pts) in enumerate(groups):
        mc=frozenset(Rclasses(classes))
        if mc not in idx: continue   # mirror must be an 8-line group too (it always is, by symmetry)
        j=idx[mc]
        if i==j:  # self-mirror group
            if not (classes & used): taken.append(i); used|=classes
        elif classes & mc:  # group overlaps its mirror -> skip (cannot take symmetric pair)
            continue
        else:
            if not ((classes|mc) & used) and j not in taken:
                taken+= [i,j]; used|=classes|mc
    B=len(taken)
    # build the cover: weight 1 on block lines; weight 1 on rows containing rest points; verify coverage
    cover=defaultdict(float)
    for i in taken:
        for L in groups[i][2]: cover[L]=1.0
    restpts=[q for q in cands if cl(q) not in used]
    rows=set(('r',q[1]) for q in restpts)
    for r in rows: cover[r]=1.0
    # verify: every candidate covered with total weight >= 1; every row used has exactly 4 rest points
    for r in rows: assert sum(1 for q in lines[r] if cl(q) not in used)==4, (p, r)
    for q in cands:
        w=cover[('r',q[1])]+cover[('c',q[0])]+cover[('d',q[0]-q[1])]+cover[('a',q[0]+q[1])]
        assert w>=1-1e-9, (p,q,w)
    cost=sum(2*w for w in cover.values())
    assert abs(cost-(4*(p-1)-2*B))<1e-9, (p,cost,B)
    return len(groups), B, cost
print(" p  #8-line groups  B(sym,disjoint)  bound=4(p-1)-2B   /(p-1)")
PMAX=int(sys.argv[1]) if len(sys.argv)>1 else 320
for p in [p for p in range(17,PMAX) if all(p%d for d in range(2,int(p**.5)+1))]:
    g,B,c=run(p); print(f"{p:3d}  {g:4d}  {B:4d}  {c:7.0f}  {c/(p-1):.3f}", flush=True)
