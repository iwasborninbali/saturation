"""cubic_anatomy.py — G3.2: rich lines of the lifted cubic graph y = f(x) (f = x^3 + a x + b) in the 2p x 2p box, their families (steps (i,j),
J = max(|i|,|j|,|i-j|)), the LP dual cover (rows, columns, all rich lines; cost 2 per line, 1 per point) and its anatomy: weight mass by line size,
by slope class (0, ±1, other), by family scale J; degrees of points in the 3-line hypergraph.  usage: python3 slack/cubic_anatomy.py p a b"""
import sys
from math import gcd
from collections import Counter, defaultdict
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
p=int(sys.argv[1]); a=int(sys.argv[2]) if len(sys.argv)>2 else 1; b=int(sys.argv[3]) if len(sys.argv)>3 else 0; N=2*p
pts=[(x,y) for x in range(N) for y in range(N) if (y-x**3-a*x-b)%p==0]
n=len(pts); idx={q:i for i,q in enumerate(pts)}
# rich lines via per-point direction buckets
seen=set(); L=[]
for i in range(n):
    d=defaultdict(list)
    xi,yi=pts[i]
    for j in range(i+1,n):
        dx=pts[j][0]-xi; dy=pts[j][1]-yi; g=gcd(abs(dx),abs(dy)); dx//=g; dy//=g
        if dx<0 or (dx==0 and dy<0): dx,dy=-dx,-dy
        d[(dx,dy)].append(j)
    for (dx,dy),js in d.items():
        if len(js)>=2:
            mem=tuple(sorted([i]+js))
            if mem not in seen: seen.add(mem); L.append(((dx,dy),mem))
rows=defaultdict(list); cols=defaultdict(list)
for i,(x,y) in enumerate(pts): rows[y].append(i); cols[x].append(i)
lines=[('row',mem) for mem in rows.values() if len(mem)>=2]+[('col',mem) for mem in cols.values() if len(mem)>=2]+[(sl,mem) for sl,mem in L if sl not in ((1,0),(0,1))]
m=len(lines); data=[];ri=[];ci=[]
for j,(tag,mem) in enumerate(lines):
    for q in mem: data.append(1.0); ri.append(q); ci.append(j)
for q in range(n): data.append(1.0); ri.append(q); ci.append(m+q)
A=csr_matrix((data,(ri,ci)),shape=(n,m+n)); c=np.concatenate([2*np.ones(m),np.ones(n)])
res=linprog(c,A_ub=-A,b_ub=-np.ones(n),bounds=[(0,None)]*(m+n),method='highs')
w=res.x[:m]; z=res.x[m:]
print(f"p={p} f=x^3+{a}x+{b}: points {n}, rich lines {len(L)} (sizes {dict(Counter(len(mm) for s,mm in L))}); LP cover = {res.fun:.1f} = {res.fun/N:.3f} N; point mass {z.sum():.1f}")
inv3=pow(3,-1,p)
def family(sl,mem):
    u,v=sl
    if u==0: return None
    P=sorted(pts[q] for q in mem)
    for base in P:
        steps=sorted(((q[0]-base[0])//u) for q in P if q!=base)
        if len(steps)!=2: return None
        i,j=steps
        if (-(i+j)*u*inv3)%p==base[0]%p: return (i,j)
    return None
mass=Counter(); massJ=Counter(); cntJ=Counter()
for jj,(tag,mem) in enumerate(lines):
    if w[jj]<1e-9: continue
    if tag=='row': mass[('row',len(mem))]+=2*w[jj]
    elif tag=='col': mass[('col',len(mem))]+=2*w[jj]
    else:
        sl=tag; k='pm1' if sl in ((1,1),(1,-1)) else 'other'
        mass[(k,len(mem))]+=2*w[jj]
        if len(mem)==3:
            fam=family(sl,mem)
            J=max(abs(fam[0]),abs(fam[1]),abs(fam[0]-fam[1])) if fam else -1
            massJ[J]+=2*w[jj]
for sl,mem in L:
    if len(mem)==3:
        fam=family(sl,mem); J=max(abs(fam[0]),abs(fam[1]),abs(fam[0]-fam[1])) if fam else -1; cntJ[J]+=1
print("  LP mass by (type,size):", {k:round(v,1) for k,v in sorted(mass.items(), key=lambda kv:-kv[1])})
print("  3-line count by J (first 12):", sorted(cntJ.items())[:12], " unmatched(-1):", cntJ.get(-1,0))
print("  LP mass on 3-lines by J (first 12):", [(J,round(massJ[J],1)) for J in sorted(massJ)[:12]])
deg=Counter()
for sl,mem in L:
    if len(mem)==3:
        for q in mem: deg[q]+=1
dd=[deg.get(q,0) for q in range(n)]
print(f"  3-line degrees: mean {np.mean(dd):.2f}, median {np.median(dd)}, min {min(dd)}, max {max(dd)}, frac(deg<=mean/2) {np.mean(np.array(dd)<=np.mean(dd)/2):.3f}")
