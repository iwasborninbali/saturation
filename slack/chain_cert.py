"""chain_cert.py — C1 (second solver): the fractional cover certificate of ONE pair of 8-groups (G_d and its RR'-image G_{-d}) for a general
second hyperbola H(k): LP  min 2*sum(y_lines) + sum(z_points)  s.t. every point covered >= 1, over rows, columns, the 6 lines of the pair,
and single points.  Prints the optimal weights organised by class and by the <k>-chain (row-mate: kappa_a -> mu_{ka}; column-mate: mu_b -> kappa_b).
usage: python3 slack/chain_cert.py p k [which_group_index]"""
import sys, numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
from collections import defaultdict, Counter
p=int(sys.argv[1]); k=int(sys.argv[2])%p; h=(p-1)//2; gi=int(sys.argv[3]) if len(sys.argv)>3 else 0
pts=[(x,y) for x in range(-h,3*h+2) for y in range(0,2*p) if (x*y)%p in (1,k)]
idx={q:i for i,q in enumerate(pts)}; n=len(pts)
def cls(q):
    x,y=pts[q]; return ('K',x%p) if (x*y)%p==1 else ('M',x%p)   # H(1)-class kappa_a (a=x mod p) or H(k)-class mu_b (b = x mod p)
lines=defaultdict(list)
for i,(x,y) in enumerate(pts):
    lines[('r',y)].append(i); lines[('c',x)].append(i); lines[('d',x-y)].append(i); lines[('a',x+y)].append(i)
# groups (slope +1): residue d -> lines with x-y ≡ d
grp=defaultdict(list)
for key,mem in lines.items():
    if key[0]=='d': grp[key[1]%p].append(key)
def profile(d): return tuple(sorted((len(lines[key]) for key in grp[d]),reverse=True))
d8=sorted(d for d in grp if profile(d)==(8,4,4))
print(f"p={p} k={k}: ord(k)={next(m for m in range(1,p) if pow(k,m,p)==1)}; 8-groups (slope+1): {len(d8)}: {d8}")
d=d8[gi]; dd={d,(-d)%p}
keys=[key for key in lines if key[0] in 'rc' or (key[0]=='d' and key[1]%p in dd)]
m=len(keys); data=[];ri=[];ci=[]
for j,key in enumerate(keys):
    for q in lines[key]: data.append(1.0); ri.append(q); ci.append(j)
for q in range(n): data.append(1.0); ri.append(q); ci.append(m+q)
A=csr_matrix((data,(ri,ci)),shape=(n,m+n))
c=np.concatenate([2*np.ones(m),np.ones(n)])
res=linprog(c,A_ub=-A,b_ub=-np.ones(n),bounds=[(0,None)]*(m+n),method='highs')
val=res.fun; y=res.x[:m]; z=res.x[m:]
print(f"cover cost = {val:.3f} = 4(p-1) - {4*(p-1)-val:.3f}; points used: {int((z>1e-9).sum())} (mass {z.sum():.2f})")
w={key:y[j] for j,key in enumerate(keys)}
print("line weights:", {key:round(w[key],3) for key in keys if key[0]=='d'})
# rows/cols by residue: row y -> residue y%p carries classes kappa_{1/y} and mu_{k/y}; column x -> residue x%p carries kappa_x, mu_x
rw=defaultdict(dict); cw=defaultdict(dict)
for key in keys:
    if key[0]=='r': rw[key[1]%p][key[1]//p]=round(w[key],3)
    if key[0]=='c': cw[key[1]%p][(key[1]+h)//p]=round(w[key],3)
dev_r={r:v for r,v in rw.items() if any(abs(t-0.5)>1e-6 for t in v.values())}
dev_c={r:v for r,v in cw.items() if any(abs(t-0.5)>1e-6 for t in v.values())}
print(f"rows deviating from 1/2: {len(dev_r)} residues of {len(rw)}; columns deviating: {len(dev_c)} of {len(cw)}")
# group classes
gcls=sorted({cls(q) for key in keys if key[0]=='d' for q in lines[key]})
print("classes of the pair of groups:", gcls)
# follow the chain from each kappa_a in the groups: kappa_a (rows y≡1/a: rw[1/a]; cols x≡a: cw[a]) -> mu_{ka} (rows 1/a, cols ka) -> kappa_{ka} ...
inv=lambda a: pow(a,-1,p)
for (t,a0) in gcls:
    if t!='K': continue
    a=a0; chain=[]
    for step in range(12):
        chain.append(f"K{a}[rows{rw[inv(a)]} cols{cw[a]}] -> M{k*a%p}[rows{rw[inv(a)]} cols{cw[k*a%p]}]")
        a=k*a%p
        if a==a0: break
    print("chain from K%d:"%a0); print("   "+"\n   ".join(chain))
