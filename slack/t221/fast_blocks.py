"""fast_blocks.py (second solver) — direct construction of a block from a run of consecutive QRs, WITHOUT building all of P_{-1}.
Run t_0..t_{k-1} (all squares, neighbours non-squares).  u_i = sqrt(t_i).  Edge i (between t_i, t_{i+1}) carries the H(1) classes
a in {A, 1/A, -A, -1/A} with A = u_i + u_{i+1} (1/A = u_{i+1} - u_i, since (u_i+u_{i+1})(u_{i+1}-u_i) = t_{i+1}-t_i = 1),
and their R-images (H(-1) classes).  Each class contributes its four lifts in the box.  Signature = profiles of the slope-+1 groups
at the vertices (residue d_i = 2 u_i).  Collects a table signature -> exact IP saving over many primes."""
import sys, json
from collections import defaultdict
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

CODE={(8,4,4):'8',(7,5,3,1):'7',(6,6,2,2):'6',(4,2,2):'a',(3,3,1,1):'b',(5,4,2,1):'c',(6,3,3):'d',(2,1,1):'e',(4,4,2,2):'f',(2,2,2,2):'g',(1,1):'h',(2,2):'i',(4,2,1,1):'j',(3,3,2):'k'}

def block_points(p, run, sqrtt):
    h=(p-1)//2
    X=lambda u: u if u<=h else u-p       # centred rep in [-h,h]
    pts=set()
    for i in range(len(run)-1):
        A=(sqrtt[run[i]]+sqrtt[run[i+1]])%p
        cls=set()
        for a in (A,(p-A)%p):
            if a==0: continue
            b=pow(a,p-2,p)
            cls|={(a,b),(b,a),((p-a)%p,(p-b)%p),((p-b)%p,(p-a)%p)}
        for (a,b) in cls:                 # H(1) class: base copy (X(a), b in [1,p-1])
            if a==0 or b==0: continue
            x0,y0=X(a),b
            for r in (0,1):
                for s in (0,1):
                    pts.add((x0+r*p, y0+s*p))          # H(1) lift
                    pts.add((p-(x0+r*p), y0+s*p))      # R-image: H(-1)
    return sorted(pts)

def profile(p, pts, d):
    cnt=defaultdict(int)
    for (x,y) in pts:
        if (x-y)%p==d%p: cnt[x-y]+=1
    return tuple(sorted(cnt.values(),reverse=True))

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

def scan(p, TAB, CNT, kmax=9):
    sq=bytearray(p); sqrtt=[0]*p
    for x in range((p+1)//2):
        sq[(x*x)%p]=1; sqrtt[(x*x)%p]=x
    t=0; seen=[False]*p
    for t0 in range(p):
        if seen[t0] or not sq[t0]: continue
        t=t0
        while sq[(t-1)%p]: t=(t-1)%p
        run=[]; z=t
        while sq[z] and not seen[z]: seen[z]=True; run.append(z); z=(z+1)%p
        k=len(run)
        if k<2: continue
        if 0 in run or (p-1) in run: continue          # degenerate edges near t=0,-1: handled separately
        CNT[k]+=1
        if k>kmax: continue
        U=block_points(p,run,sqrtt)
        sig=''.join(CODE.get(profile(p,U,(2*sqrtt[s])%p),'?') for s in run)
        sig=min(sig,sig[::-1])
        if sig in TAB or '?' in sig: 
            if '?' in sig: CNT['bad']+=1
            CNT[sig]+=1; continue
        CNT[sig]+=1
        TAB[sig]=ip_saving(U)

TAB={}; CNT=defaultdict(int)
def primes(a,b):
    s=bytearray([1])*(b+1); s[0]=s[1]=0
    for i in range(2,int(b**.5)+1):
        if s[i]: s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(a,b+1) if s[i]]
ps=primes(int(sys.argv[1]),int(sys.argv[2]))
for i,p in enumerate(ps):
    scan(p,TAB,CNT)
    if i%20==0: print(f"  p={p}: signatures={len(TAB)} bad={CNT['bad']}", flush=True)
print(f"\nTOTAL signatures={len(TAB)}  bad={CNT['bad']}")
for s in sorted(TAB,key=lambda s:(len(s),s)):
    print(f"  {s:10s} sav={TAB[s]:6.2f} count={CNT[s]}")
json.dump({'saving':TAB,'count':{k:v for k,v in CNT.items() if isinstance(k,str)}},open('slack/t221/fast_sig_table9.json','w'),indent=0)
