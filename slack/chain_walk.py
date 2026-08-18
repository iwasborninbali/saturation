"""chain_walk.py — C1 (second solver): the class-graph of P_k = H(1) ∪ H(k) is a union of even cycles (row-mate kappa_a — mu_{ka}, column-mate
mu_b — kappa_b); with weight 1/2 on the three lines of every (4,8,4) group, the classes of 8-groups have demand 1/2 ('specials').  The row/column
cover LP on each cycle has the tight value 2L - (#specials) iff the alternating recursion is feasible; this script reports, per cycle: length,
#kappa-specials, #mu-specials, the range of the walk (#kappa specials - #mu specials along the cycle), and the exact LP value of the cover with
all 8-group lines forced at 1/2 versus the tight bound.  usage: python3 slack/chain_walk.py p k"""
import sys, numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
from collections import defaultdict
p=int(sys.argv[1]); k=int(sys.argv[2])%p; h=(p-1)//2
pts=[(x,y) for x in range(-h,3*h+2) for y in range(0,2*p) if (x*y)%p in (1,k)]
n=len(pts); lines=defaultdict(list)
for i,(x,y) in enumerate(pts):
    lines[('r',y)].append(i); lines[('c',x)].append(i); lines[('d',x-y)].append(i); lines[('a',x+y)].append(i)
def cls(i):
    x,y=pts[i]; return ('K',x%p) if (x*y)%p==1 else ('M',x%p)
groups=defaultdict(list)
for key,mem in lines.items():
    if key[0] in 'da': groups[(key[0],key[1]%p)].append(key)
g8=[g for g,ks in groups.items() if sorted((len(lines[key]) for key in ks),reverse=True)==[8,4,4]]
special=set()
for g in g8:
    for key in groups[g]:
        for i in lines[key]: special.add(cls(i))
G8=len(g8); print(f"p={p} k={k}: ord(k)={next(m for m in range(1,p) if pow(k,m,p)==1)}; 8-groups (both slopes) G8={G8}; special classes={len(special)} (4*G8={4*G8}; overlaps={4*G8-len(special)})")
# cycles: start from kappa_a, step kappa_x -> mu_{kx} -> kappa_{kx}
seen=set(); cyc=[]
for a in range(1,p):
    if ('K',a) in seen: continue
    x=a; seq=[]
    while ('K',x) not in seen:
        seen.add(('K',x)); seq.append(('K',x)); seq.append(('M',k*x%p)); x=k*x%p
    cyc.append(seq)
tot_tight=0
for seq in cyc:
    L=len(seq); nk=sum(1 for c in seq if c in special and c[0]=='K'); nm=sum(1 for c in seq if c in special and c[0]=='M')
    w=0; mx=mn=0
    for c in seq:
        if c in special: w+= (1 if c[0]=='K' else -1); mx=max(mx,w); mn=min(mn,w)
    print(f"  cycle L={L}: specials K={nk} M={nm}; walk range={mx-mn} (final {w}); tight saving 2*min={2*min(nk,nm)}")
    tot_tight+=2*min(nk,nm)
# exact LP: rows, cols, points + the 8-groups' lines forced at weight 1/2
keys=[key for key in lines if key[0] in 'rc']; forced=[key for g in g8 for key in groups[g]]
m=len(keys); data=[];ri=[];ci=[]
for j,key in enumerate(keys):
    for q in lines[key]: data.append(1.0); ri.append(q); ci.append(j)
for q in range(n): data.append(1.0); ri.append(q); ci.append(m+q)
A=csr_matrix((data,(ri,ci)),shape=(n,m+n))
b=np.ones(n)
for key in forced:
    for q in lines[key]: b[q]-=0.5
b=np.maximum(b,0)
c=np.concatenate([2*np.ones(m),np.ones(n)])
res=linprog(c,A_ub=-A,b_ub=-b,bounds=[(0,None)]*(m+n),method='highs')
rc=res.fun; total=rc+len(forced)*1.0   # each forced line costs 2*(1/2)=1
print(f"  rows/cols LP with forced lines: {rc:.2f} = 4(p-1) - {4*(p-1)-rc:.2f} (tight bound saving {tot_tight}); total cover = {total:.2f} = 4(p-1) - {4*(p-1)-total:.2f}  [net per 8-group {(4*(p-1)-total)/max(1,G8):.3f}]")
