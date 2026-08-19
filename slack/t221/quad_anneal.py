"""quad_anneal.py — fast lower bounds for the union of m hyperbolae by local search (null moves along light rays),
to read off the TREND of the gain over 3(p-1) for larger p than CP-SAT can reach exactly."""
import sys, random
from collections import defaultdict
from math import gcd
def build(p, cs):
    h=(p-1)//2
    S={c%p for c in cs}
    return [(x,y) for x in range(-h,3*h+2) for y in range(0,2*p) if (x*y)%p in S]
def line_key(a,b):
    dx,dy=b[0]-a[0],b[1]-a[1]; g=gcd(abs(dx),abs(dy)) or 1; dx,dy=dx//g,dy//g
    if dx<0 or (dx==0 and dy<0): dx,dy=-dx,-dy
    return (dx,dy,dy*a[0]-dx*a[1])
def greedy_rounds(p, cs, rounds=40, seed=0):
    pts=build(p,cs); rnd=random.Random(seed); best=0; bestS=None
    # precompute for each pair its line key
    n=len(pts)
    idx={q:i for i,q in enumerate(pts)}
    pairline={}
    lines=defaultdict(list)
    for i in range(n):
        for j in range(i+1,n):
            k=line_key(pts[i],pts[j]); lines[k].append((i,j))
    memb=defaultdict(list)
    for k,prs in lines.items():
        mem=sorted({i for pr in prs for i in pr})
        if len(mem)>=3:
            for i in mem: memb[i].append(k)
    linemem={k:sorted({i for pr in prs for i in pr}) for k,prs in lines.items() if len({i for pr in prs for i in pr})>=3}
    for r in range(rounds):
        order=list(range(n)); rnd.shuffle(order)
        cnt=defaultdict(int); S=set()
        for i in order:
            if all(cnt[k]<2 for k in memb[i]):
                S.add(i)
                for k in memb[i]: cnt[k]+=1
        # local improvement: remove 1, add 2
        improved=True
        while improved:
            improved=False
            for i in list(S):
                S.discard(i)
                for k in memb[i]: cnt[k]-=1
                added=0
                for j in order:
                    if j in S: continue
                    if all(cnt[k]<2 for k in memb[j]):
                        S.add(j); added+=1
                        for k in memb[j]: cnt[k]+=1
                        if added==2: break
                if added>=2: improved=True
                elif added==1: pass
                else:
                    S.add(i)
                    for k in memb[i]: cnt[k]+=1
        if len(S)>best: best=len(S); bestS=set(S)
    return len(pts), best
for p in map(int,sys.argv[2:]):
    cs=[1,-1] if sys.argv[1]=='pair' else ([1,-1,2,-2] if sys.argv[1]=='quad' else [1])
    n,b=greedy_rounds(p,cs)
    print(f"p={p:3d} {sys.argv[1]:5s}: |P|={n:5d} lower bound={b}  ratio={b/(2*p):.3f}N  gain over 3(p-1)={b-3*(p-1):+d}", flush=True)
