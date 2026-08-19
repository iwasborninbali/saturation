"""components_lp.py (second solver) — savings of CONNECTED COMPONENTS of the neighbour graph of used orbits (k=-1).
Vertices: orbits Omega_d of types (4,8,4) ['8'] and (3,7,5,1) ['7'], indexed by x = d^2 mod p; edges x ~ x+4 (Lemma neighbours).
No 8-8 edges (Lemma closure(i)); every vertex has <= 2 neighbours, so components are paths.
For a component with vertex set C: U = union of its orbits (|U| = 64|C| - 32(|C|-1)), closed under rows/columns;
  LP(U) with rows, columns, slope-+-1 lines (cap 2), and IP(U) (exact, HiGHS MILP).  Saving = |U|/2 - value.
usage: python3 slack/t221/components_lp.py p [p ...]"""
import sys
from collections import defaultdict
import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds

def build(p):
    h=(p-1)//2
    return [(x,y) for x in range(-h,3*h+2) for y in range(0,2*p) if (x*y)%p in (1,p-1)]

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

def matrices(U):
    idx={q:i for i,q in enumerate(U)}; n=len(U)
    lines=defaultdict(list)
    for (x,y) in U:
        lines[('r',y)].append(idx[(x,y)]); lines[('c',x)].append(idx[(x,y)])
        lines[('d',x-y)].append(idx[(x,y)]); lines[('a',x+y)].append(idx[(x,y)])
    L=[m for m in lines.values() if len(m)>=3]
    A=np.zeros((len(L),n))
    for i,m in enumerate(L):
        for j in m: A[i,j]=1
    return A,n

def lp_ip(U, do_ip=True):
    A,n=matrices(U)
    r=linprog(-np.ones(n),A_ub=A,b_ub=2*np.ones(len(A)),bounds=[(0,1)]*n,method='highs')
    v_lp=-r.fun
    v_ip=None
    if do_ip:
        m=milp(c=-np.ones(n),constraints=LinearConstraint(A,-np.inf,2*np.ones(len(A))),
               bounds=Bounds(0,1),integrality=np.ones(n))
        v_ip=-m.fun if m.success else None
    return v_lp,v_ip

def run(p, do_ip=True):
    pts=build(p); T=types(p)
    used={x:T[x] for x in T if T[x][0] in '78'}
    # components under x ~ x+4
    seen=set(); comps=[]
    for x in used:
        if x in seen: continue
        y=x
        while (y-4)%p in used and (y-4)%p!=x: y=(y-4)%p
        C=[]; z=y
        while z in used and z not in seen:
            seen.add(z); C.append(z); z=(z+4)%p
        comps.append(C)
    orb={}
    for x,(t,d) in used.items():
        orb[x]=[q for q in pts if (q[0]-q[1])%p in (d,(-d)%p) or (q[0]+q[1])%p in (d,(-d)%p)]
    agg=defaultdict(list)
    for C in comps:
        sig=''.join(used[x][0] for x in C)
        sig=min(sig,sig[::-1])
        U=sorted(set().union(*[set(orb[x]) for x in C]))
        vlp,vip=lp_ip(U, do_ip and len(C)<=3)
        agg[sig].append((len(U),len(U)/2-vlp,(len(U)/2-vip) if vip is not None else None))
    tot_lp=0.0; tot_ip=0.0; n8=n7=0
    for sig in sorted(agg,key=lambda s:(len(s),s)):
        v=agg[sig]
        lps=sorted(set(round(a[1],3) for a in v)); ips=sorted(set(a[2] for a in v if a[2] is not None))
        print(f"  p={p} comp '{sig}' x{len(v)}: |U|={v[0][0]} saving LP={lps} IP={ips}")
        tot_lp+=sum(a[1] for a in v); tot_ip+=sum((a[2] if a[2] is not None else a[1]) for a in v)
        n8+=sig.count('8')*len(v); n7+=sig.count('7')*len(v)
    print(f"  p={p} TOTAL: orbits 8:{n8} 7:{n7}  saving LP={tot_lp:.2f} IP>={tot_ip:.2f}  "
          f"bound/(p-1) LP={(4*(p-1)-tot_lp)/(p-1):.4f} IP={(4*(p-1)-tot_ip)/(p-1):.4f}  (v1.10: {(4*(p-1)-8*n8/2-4*sum(1 for s in agg if s=='7' for _ in agg[s]))/(p-1):.4f} w/ clean only)")
for p in map(int,sys.argv[1:]): run(p)
