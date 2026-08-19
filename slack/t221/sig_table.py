"""sig_table.py — complete table 'signature -> exact IP saving' for runs of consecutive QRs (blocks of P_{-1}), k <= 6.
Signature = string of vertex types along the run: interior in {8,7,6}, ends in {a=(4,2,2), b=(3,3,1,1)} (canonical up to reversal).
Collected over many primes; prints coverage of the theoretically possible signatures."""
import sys, json, itertools
from collections import defaultdict
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

CODE={(8,4,4):'8',(7,5,3,1):'7',(6,6,2,2):'6',(4,2,2):'a',(3,3,1,1):'b',(5,4,2,1):'c',(6,3,3):'d',(2,1,1):'e',(4,4,2,2):'f',(2,2,2,2):'g'}
def code(prof): return CODE.get(tuple(sorted(prof,reverse=True)),'?')

def blocks(p):
    h=(p-1)//2
    pts=[(x,y) for x in range(-h,3*h+2) for y in range(0,2*p) if (x*y)%p in (1,p-1)]
    byres=defaultdict(set); plus=defaultdict(lambda: defaultdict(int))
    for q in pts:
        byres[('p',(q[0]-q[1])%p)].add(q); byres[('m',(q[0]+q[1])%p)].add(q)
        plus[(q[0]-q[1])%p][q[0]-q[1]]+=1
    prof={d:tuple(sorted(plus[d].values(),reverse=True)) for d in plus}
    orb={}
    for d in range(0,(p+1)//2):
        O=byres[('p',d%p)]|byres[('p',(-d)%p)]|byres[('m',d%p)]|byres[('m',(-d)%p)]
        if O: orb[(d*d)%p]=(O,d)
    seen=set(); out=[]
    for x in orb:
        if x in seen: continue
        y=x
        while (y-4)%p in orb and (y-4)%p!=x: y=(y-4)%p
        C=[]; z=y
        while z in orb and z not in seen: seen.add(z); C.append(z); z=(z+4)%p
        sig=''.join(code(prof.get(orb[t][1],())) for t in C); sig=min(sig,sig[::-1])
        out.append((sig,sorted(set().union(*[orb[t][0] for t in C]))))
    return out

def ip_saving(U):
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

TAB={}; CNT=defaultdict(int)
def primes(a,b): return [q for q in range(a,b) if all(q%d for d in range(2,int(q**.5)+1))]
for p in primes(200,2600):
    for sig,U in blocks(p):
        CNT[sig]+=1
        if sig in TAB or len(sig)>6 or len(U)>800: continue
        TAB[sig]=ip_saving(U)
poss=set()
for k in range(2,7):
    for ends in itertools.product('ab',repeat=2):
        for inter in itertools.product('867',repeat=max(0,k-2)):
            s=ends[0]+''.join(inter)+ends[1]; poss.add(min(s,s[::-1]))
seen=set(TAB)
print(f"signatures found: {len(TAB)} (with counts over {len(primes(200,1400))} primes); possible with k<=6: {len(poss)}; missing: {len(poss-seen)}")
for s in sorted(TAB,key=lambda s:(len(s),s)):
    print(f"  {s:8s} saving={TAB[s]:6.2f}  count={CNT[s]}")
miss=sorted(poss-seen,key=lambda s:(len(s),s))
print("missing (k<=5):",[s for s in miss if len(s)<=5][:40])
json.dump({'saving':TAB,'count':dict(CNT)},open('slack/t221/sig_table.json','w'),indent=0)
