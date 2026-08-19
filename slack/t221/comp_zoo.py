"""comp_zoo.py — zoo of component types of the neighbour graph (used orbits: '8' = (4,8,4), '7' = (3,7,5,1)) and their LP/IP savings.
Saving of a component C: |U|/2 - value, |U| = 32(|C|+1).  Aggregated over primes; also the resulting bound 4(p-1) - total saving."""
import sys
from collections import defaultdict
import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds

def types(p):
    inv=lambda t: pow(t,p-2,p); h=(p-1)//2; X=lambda u: u if u<=h else u-p
    sig=defaultdict(list); tau=defaultdict(list)
    for t in range(1,p):
        sig[(t-inv(t))%p].append(t); tau[(t+inv(t))%p].append(t)
    out={}
    for d in range(1,p):
        if len(sig[d])==2 and len(tau[d])==2:
            a=sig[d][0]; b=tau[d][0]
            ss=(X(a)>0)!=(X(inv(a))>0); ts=(X(b)>0)==(X(inv(b))>0)
            out[(d*d)%p]=('8' if (ss and ts) else ('7' if (ss or ts) else '6'), min(d,p-d))
    return out

def solve(U, ip):
    idx={q:i for i,q in enumerate(U)}; n=len(U); lines=defaultdict(list)
    for (x,y) in U:
        lines[('r',y)].append(idx[(x,y)]); lines[('c',x)].append(idx[(x,y)])
        lines[('d',x-y)].append(idx[(x,y)]); lines[('a',x+y)].append(idx[(x,y)])
    L=[m for m in lines.values() if len(m)>=3]
    A=np.zeros((len(L),n))
    for i,m in enumerate(L):
        for j in m: A[i,j]=1
    r=linprog(-np.ones(n),A_ub=A,b_ub=2*np.ones(len(L)),bounds=[(0,1)]*n,method='highs'); vlp=-r.fun
    vip=None
    if ip:
        m=milp(c=-np.ones(n),constraints=LinearConstraint(A,-np.inf,2*np.ones(len(L))),bounds=Bounds(0,1),integrality=np.ones(n))
        if m.success: vip=-m.fun
    return vlp,vip

def run(p, zoo, tot):
    h=(p-1)//2
    pts=[(x,y) for x in range(-h,3*h+2) for y in range(0,2*p) if (x*y)%p in (1,p-1)]
    T=types(p); used={x:T[x] for x in T if T[x][0] in '78'}
    byres=defaultdict(list)
    for q in pts:
        byres[('p',(q[0]-q[1])%p)].append(q); byres[('m',(q[0]+q[1])%p)].append(q)
    orb={}
    for x,(t,d) in used.items():
        orb[x]=set(byres[('p',d)])|set(byres[('p',(-d)%p)])|set(byres[('m',d)])|set(byres[('m',(-d)%p)])
    seen=set(); comps=[]
    for x in used:
        if x in seen: continue
        y=x
        while (y-4)%p in used and (y-4)%p!=x: y=(y-4)%p
        C=[]; z=y
        while z in used and z not in seen:
            seen.add(z); C.append(z); z=(z+4)%p
        comps.append(C)
    sav=0.0
    for C in comps:
        sig=''.join(used[x][0] for x in C); sig=min(sig,sig[::-1])
        U=sorted(set().union(*[orb[x] for x in C]))
        if sig in zoo and len(zoo[sig]['vals'])>=6:
            s=zoo[sig]['best']
        else:
            vlp,vip=solve(U, len(C)<=3)
            s=(len(U)/2-vip) if vip is not None else (len(U)/2-vlp)
            z=zoo[sig]; z['vals'].append(round(s,4)); z['n']+=0; z['best']=s; z['size']=len(U)
        zoo[sig]['n']+=1; sav+=s
    tot['sav']+=sav; tot['p']+=p
    print(f"p={p}: components={len(comps)} saving={sav:.2f} bound/(p-1)={(4*(p-1)-sav)/(p-1):.4f}")

zoo=defaultdict(lambda: {'vals':[], 'n':0, 'best':None, 'size':None}); tot={'sav':0.0,'p':0}
for p in map(int,sys.argv[1:]): run(p,zoo,tot)
print("\nZOO (component type: count, |U|, savings seen):")
for sig in sorted(zoo,key=lambda s:(len(s),s)):
    z=zoo[sig]; print(f"  '{sig}': n={z['n']} |U|={z['size']} savings={sorted(set(z['vals']))}")
print(f"\npooled: saving/p = {tot['sav']/tot['p']:.4f}  =>  bound ~ {4-tot['sav']/tot['p']:.4f} (p-1)")
