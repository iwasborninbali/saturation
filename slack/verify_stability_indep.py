"""independent check of Lemma orbdec / orbopt / Prop stability (first solver's review of v1.13)"""
import sys
from itertools import combinations
from collections import defaultdict
sys.path.insert(0,'/home/pmbot/projects/saturation_peer/slack')
from lp_curve import lines as alllines
def orbits(p):
    h=(p-1)//2; x0,y0=-h,0
    orb={}
    for a in range(1,p):
        ia=pow(a,-1,p); orb[a]=frozenset({a,ia,(p-a)%p,(p-ia)%p})
    seen=set(); out=[]
    for a in range(1,p):
        O=orb[a]
        if O in seen: continue
        seen.add(O)
        pts=[]
        for b in O:
            ib=pow(b,-1,p); bx=x0+((b-x0)%p); by=y0+((ib-y0)%p)
            pts += [(bx+r*p, by+s*p) for r in (0,1) for s in (0,1)]
        out.append((O, sorted(set(pts))))
    return out
def lawful_sets(P):
    L=[frozenset(s) for s in alllines(P,'all')]
    idx={q:i for i,q in enumerate(P)}
    best=0; maxima=[]
    for m in range(len(P),0,-1):
        found=[]
        for S in combinations(range(len(P)), m):
            SS=set(S)
            if all(len(SS & l) <= 2 for l in L): found.append(SS)
        if found: return m, found, L
    return 0, [], L
for p in (11,13,17,19,23):
    prof=defaultdict(int); res=defaultdict(list)
    allpts=set()
    for O,P in orbits(p): allpts |= set(P)
    # (1) do rich lines stay inside an orbit?
    cross=0
    L=alllines(sorted(allpts),'all'); ap=sorted(allpts)
    owner={}
    for i,(O,P) in enumerate(orbits(p)):
        for q in P: owner[q]=i
    for s in L:
        if len({owner[ap[j]] for j in s})>1: cross+=1
    for O,P in orbits(p):
        m, maxima, LL = lawful_sets(P)
        sizes=tuple(sorted((len(l) for l in LL), reverse=True))
        kind = 'generic' if len(P)==16 else 'exceptional'
        res[kind].append((m, len(maxima), sizes))
        # stability: every lawful of size m-d has <= d points outside SOME maximum
        ok=True
        for d in (1,2,3):
            for S in combinations(range(len(P)), m-d):
                SS=set(S)
                if all(len(SS & l) <= 2 for l in LL):
                    if min(len(SS - M) for M in maxima) > d: ok=False; break
            if not ok: break
        res[kind][-1] = res[kind][-1] + (ok,)
    summ = {k: sorted(set(v)) for k,v in res.items()}
    print(f"p={p}: rich lines crossing orbits: {cross}; per kind (alpha, #maxima, line profile, stability_ok): {summ}", flush=True)
