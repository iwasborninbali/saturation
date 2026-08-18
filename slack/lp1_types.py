"""lp1_types.py — T2.17 (third solver): does the LP(1) saving decompose over residue-group types?  For k=-1 and given p:
 * LP(1) = LP with rows, columns, slope-±1 lines (>=3 points); saving S = 4(p-1) - LP(1).
 * slope-(+1) residue groups G_d (d = x-y mod p), type = (line-size profile, #kappa classes, #lambda classes); slope-(-1) groups are their R-images.
 * per type t: B_t = number of (+1)-groups; Delta_t = LP(1)[without the ±1 lines of all groups of type t and their R-images] - LP(1)
   (marginal contribution of type t to the saving); Sol_t = 4(p-1) - LP(1)[rows, cols, and ONLY the ±1 lines of type-t groups] (solitary saving).
 * additivity test: sum_t Delta_t vs S and sum_t Sol_t vs S; and per-group marginals Delta_G for the variance within a type (option 'groups').
usage: python3 slack/lp1_types.py p [groups]"""
import sys, numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
from collections import defaultdict, Counter
p=int(sys.argv[1]); do_groups=len(sys.argv)>2 and sys.argv[2]=='groups'
h=(p-1)//2
pts=[(x,y) for x in range(-h,3*h+2) for y in range(0,2*p) if (x*y)%p in (1,p-1)]
idx={q:i for i,q in enumerate(pts)}; n=len(pts)
lines=defaultdict(list)
for (x,y) in pts:
    lines[('r',y)].append(idx[(x,y)]); lines[('c',x)].append(idx[(x,y)])
    lines[('d',x-y)].append(idx[(x,y)]); lines[('a',x+y)].append(idx[(x,y)])
L=[(key,mem) for key,mem in lines.items() if len(mem)>=3]
def lp(keep):
    rows=[i for i,(key,mem) in enumerate(L) if keep(key)]
    data=[];ri=[];ci=[]
    for r,i in enumerate(rows):
        for j in L[i][1]: data.append(1.0); ri.append(r); ci.append(j)
    A=csr_matrix((data,(ri,ci)),shape=(len(rows),n))
    res=linprog(-np.ones(n),A_ub=A,b_ub=2*np.ones(len(rows)),bounds=[(0,1)]*n,method='highs')
    return -res.fun
V=lp(lambda key: True); S=4*(p-1)-V
# groups (+1) and types; R maps (+1)-group at residue d to the (-1)-line residue: x+y ≡ p-d, i.e. antidiagonal residue e=(x+y) mod p = (-d) mod p
grp=defaultdict(list)
for i,(x,y) in enumerate(pts): grp[(x-y)%p].append(i)
gtype={}
for d,mem in grp.items():
    cs=Counter((pts[i][0]-pts[i][1]) for i in mem); prof=tuple(sorted(cs.values(),reverse=True))
    nk=sum(1 for a in range(1,p) if (a-pow(a,-1,p))%p==d); nl=sum(1 for b in range(1,p) if (b+pow(b,-1,p))%p==(-d)%p)
    gtype[d]=(prof,nk,nl)
types=defaultdict(list)
for d,t in gtype.items(): types[t].append(d)
def dres_of(key):   # residue label of a ±1 line: for 'd': d=c mod p (its +1 group); for 'a': its R-preimage +1 group has d ≡ -c mod p
    t,c=key
    if t=='d': return c%p
    if t=='a': return (-c)%p
    return None
print(f"p={p}: LP(1)={V:.3f} = {V/(p-1):.4f}(p-1); saving S={S:.3f}; (+1)-groups {len(grp)}, types {len(types)}")
print("   type (profile;#k,#l): B_t | Delta_t (marginal, both slopes) | Sol_t (solitary) | Delta_t/B_t | Sol_t/B_t")
sumD=0; sumS=0; rows_out=[]
for t,ds in sorted(types.items(), key=lambda kv:(-len(kv[1]))):
    dset=set(ds)
    Vwo=lp(lambda key: key[0] in 'rc' or dres_of(key) not in dset)
    Vonly=lp(lambda key: key[0] in 'rc' or dres_of(key) in dset)
    D=Vwo-V; So=4*(p-1)-Vonly; sumD+=D; sumS+=So
    prof,nk,nl=t
    print(f"   {str(prof):20s} k{nk} l{nl}: {len(ds):4d} | {D:8.3f} | {So:8.3f} | {D/len(ds):6.3f} | {So/len(ds):6.3f}", flush=True)
    rows_out.append((t,len(ds),D,So))
print(f"   sum Delta_t = {sumD:.3f}, sum Sol_t = {sumS:.3f}, S = {S:.3f}  (additive iff both ≈ S)")
if do_groups:
    print("   per-group marginals Delta_G (both slopes: group + its R-image) by type: mean [min,max] over groups")
    for t,ds in sorted(types.items(), key=lambda kv:(-len(kv[1]))):
        vals=[]
        for d in ds:
            Vwo=lp(lambda key,d=d: key[0] in 'rc' or dres_of(key)!=d)
            vals.append(Vwo-V)
        prof,nk,nl=t
        print(f"   {str(prof):20s} k{nk} l{nl}: {np.mean(vals):6.3f} [{min(vals):6.3f},{max(vals):6.3f}]  n={len(vals)}", flush=True)
