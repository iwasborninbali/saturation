"""comp_table.py — table of component signatures -> exact IP saving (memoised), and the resulting bound over many primes.
alpha(P_{-1}) <= 4(p-1) - sum over components of saving(signature).  Signature = tuple of +1-line-size profiles along the chain."""
import sys, json
from collections import defaultdict
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

MEMO={}
def saving(U):
    idx={q:i for i,q in enumerate(U)}; lines=defaultdict(list)
    for (x,y) in U:
        lines[('r',y)].append(idx[(x,y)]); lines[('c',x)].append(idx[(x,y)])
        lines[('d',x-y)].append(idx[(x,y)]); lines[('a',x+y)].append(idx[(x,y)])
    L=[m for m in lines.values() if len(m)>=3]
    A=np.zeros((len(L),len(U)))
    for i,m in enumerate(L):
        for j in m: A[i,j]=1
    r=milp(c=-np.ones(len(U)),constraints=LinearConstraint(A,-np.inf,2*np.ones(len(L))),bounds=Bounds(0,1),integrality=np.ones(len(U)))
    return len(U)/2-(-r.fun)

def run(p, cnt, capn=700):
    h=(p-1)//2
    pts=[(x,y) for x in range(-h,3*h+2) for y in range(0,2*p) if (x*y)%p in (1,p-1)]
    byres=defaultdict(set); plus=defaultdict(lambda: defaultdict(int))
    for q in pts:
        byres[('p',(q[0]-q[1])%p)].add(q); byres[('m',(q[0]+q[1])%p)].add(q)
        plus[(q[0]-q[1])%p][q[0]-q[1]]+=1
    prof={d:tuple(sorted(plus[d].values(),reverse=True)) for d in plus}
    orb={}
    for d in range(1,(p+1)//2):
        O=byres[('p',d)]|byres[('p',(-d)%p)]|byres[('m',d)]|byres[('m',(-d)%p)]
        if O: orb[(d*d)%p]=(O,min(d,p-d))
    seen=set(); comps=[]
    for x in orb:
        if x in seen: continue
        y=x
        while (y-4)%p in orb and (y-4)%p!=x: y=(y-4)%p
        C=[]; z=y
        while z in orb and z not in seen:
            seen.add(z); C.append(z); z=(z+4)%p
        comps.append(C)
    tot=0.0; skipped=0
    for C in comps:
        sig=tuple(prof.get(orb[x][1],()) for x in C); sig=min(sig,sig[::-1])
        if sig in MEMO: s=MEMO[sig]
        else:
            U=sorted(set().union(*[orb[x][0] for x in C]))
            if len(U)>capn: skipped+=1; continue
            s=saving(U); MEMO[sig]=s
        cnt[sig]+=1; tot+=s
    print(f"p={p}: components={len(comps)} skipped={skipped} saving={tot:.1f} => alpha <= {(4*(p-1)-tot)/(p-1):.4f}(p-1)")
    return tot,p

cnt=defaultdict(int); T=0.0; P=0
for p in map(int,sys.argv[1:]):
    t,q=run(p,cnt); T+=t; P+=q
print("\nSIGNATURE TABLE (profile chain -> exact saving, count):")
for sig,n in sorted(cnt.items(),key=lambda kv:-kv[1]):
    print(f"  n={n:5d} saving={MEMO[sig]:6.3f}  {sig}")
print(f"\npooled saving/p = {T/P:.4f}  =>  alpha <= {4-T/P:.4f}(p-1) asymptotically (empirical)")
json.dump({str(k):v for k,v in MEMO.items()}, open('slack/t221/comp_savings.json','w'), indent=0)
