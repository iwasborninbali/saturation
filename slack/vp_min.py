import sys, itertools, numpy as np
from collections import defaultdict
sys.path.insert(0,'/Users/iwasborninbali/saturation/slack')
p=int(sys.argv[1]); h=(p-1)//2
def X(u): u%=p; return u if u<=h else u-p
def Y(u): u%=p; return u if u else p
classes=[(hyp,a) for a in range(1,p) for hyp in (1,-1)]
base={}
for hyp,a in classes:
    ia=pow(a,-1,p); base[(hyp,a)]=(X(a), Y(ia if hyp==1 else -ia))
def col(cls,ra):
    hyp,a=cls; return base[cls][0]+(ra if hyp==1 else 1-ra)*p
coef=defaultdict(float)
for c1,c2,c3 in itertools.combinations(classes,3):
    avars=sorted({c1[1],c2[1],c3[1]})
    for bits in itertools.product((0,1),repeat=len(avars)):
        rmap=dict(zip(avars,bits)); xs=[col(c,rmap[c[1]]) for c in (c1,c2,c3)]
        if len(set(xs))<3: continue
        for s in itertools.product((0,1),repeat=3):
            (x1,y1),(x2,y2),(x3,y3)=[(xs[i], base[(c1,c2,c3)[i]][1]+s[i]*p) for i in range(3)]
            if (x2-x1)*(y3-y1)==(x3-x1)*(y2-y1):
                items=list(rmap.items()); n=len(items)
                for mask in range(1<<n):
                    mono=tuple(sorted(items[i][0] for i in range(n) if mask>>i&1)); sign=1
                    for i in range(n):
                        if mask>>i&1 and items[i][1]==1: sign=-sign
                    coef[mono]+=sign/(1<<n)
n=p-1; E=coef.get((),0.0); C=np.zeros((n,n))
for m,v in coef.items():
    if len(m)==2: C[m[0]-1,m[1]-1]+=v/2; C[m[1]-1,m[0]-1]+=v/2
lam=np.linalg.eigvalsh(C)[0]
# exact min over the cube: use symmetry eps -> -eps (fix eps_1 = +1), vectorized in chunks
best=1e18; N=1<<(n-1)
chunk=1<<18
for start in range(0,N,chunk):
    idx=np.arange(start,min(N,start+chunk),dtype=np.int64)
    bits=((idx[:,None]>>np.arange(n-1))&1).astype(np.float64)   # n-1 free bits
    eps=np.concatenate([np.ones((len(idx),1)),1-2*bits],axis=1)   # eps_1=+1
    vals=E+np.einsum('ij,jk,ik->i',eps,C,eps)
    m=vals.min()
    if m<best: best=m
print(f"p={p}: E={E:.1f}, lambda_min={lam:.3f}, spectral bound {E+n*lam:.1f}, exact min over all orientations = {best:.1f} (= {best/(p-1):.3f}(p-1))")
