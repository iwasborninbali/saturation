"""window_rule.py — is the component saving an ADDITIVE function of bounded windows along the chain?
Model: saving(t_1..t_L) = sum_i w(t_{i-1}, t_i, t_{i+1}) with boundary symbol '.'; fit exactly by least squares over all observed
components and report the residuals.  Types: 8=(4,8,4), 7=(3,7,5,1)/(1,5,7,3), 6=(2,6,6,2), a=(4,2,2), b=(3,3,1,1), o=other/empty."""
import sys
from collections import defaultdict
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def code(prof):
    m={(4,8,4):'8',(3,7,5,1):'7',(1,5,7,3):'7',(2,6,6,2):'6',(4,2,2):'a',(3,3,1,1):'b',(6,6,2,2):'6',(7,5,3,1):'7',(5,4,2,1):'c',(6,3,3):'d',(2,4,2):'a'}
    return m.get(tuple(sorted(prof,reverse=True)),'o')

def collect(p, data, capn=700):
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
    seen=set(); comps=[]
    for x in orb:
        if x in seen: continue
        y=x
        while (y-4)%p in orb and (y-4)%p!=x: y=(y-4)%p
        C=[]; z=y
        while z in orb and z not in seen: seen.add(z); C.append(z); z=(z+4)%p
        comps.append(C)
    for C in comps:
        sig=''.join(code(prof.get(orb[x][1],())) for x in C)
        sig=min(sig,sig[::-1])
        U=sorted(set().union(*[orb[x][0] for x in C]))
        if len(U)>capn: continue
        if sig in data and len(data[sig])>=3: continue
        idx={q:i for i,q in enumerate(U)}; lines=defaultdict(list)
        for (x,y) in U:
            lines[('r',y)].append(idx[(x,y)]); lines[('c',x)].append(idx[(x,y)])
            lines[('d',x-y)].append(idx[(x,y)]); lines[('a',x+y)].append(idx[(x,y)])
        L=[m for m in lines.values() if len(m)>=3]
        A=np.zeros((len(L),len(U)))
        for i,m in enumerate(L):
            for j in m: A[i,j]=1
        r=milp(c=-np.ones(len(U)),constraints=LinearConstraint(A,-np.inf,2*np.ones(len(L))),bounds=Bounds(0,1),integrality=np.ones(len(U)))
        data[sig].append(round(len(U)/2-(-r.fun),4))

data=defaultdict(list)
for p in map(int,sys.argv[1:]): collect(p,data)
amb=[k for k,v in data.items() if len(set(v))>1]
print(f"components types={len(data)}  ambiguous={len(amb)} {amb[:5]}")
# fit additive window rule of radius 1
keys=sorted(data); rows=[]; ys=[]; feats={}
for k in keys:
    s='.'+k+'.'; vec=defaultdict(int)
    for i in range(1,len(s)-1):
        vec[s[i-1:i+2]]+=1
    rows.append(vec); ys.append(data[k][0])
for v in rows:
    for f in v: feats.setdefault(f,len(feats))
A=np.zeros((len(rows),len(feats))); 
for i,v in enumerate(rows):
    for f,c in v.items(): A[i,feats[f]]=c
y=np.array(ys)
w,res,rank,sv=np.linalg.lstsq(A,y,rcond=None)
pred=A@w; err=np.abs(pred-y)
print(f"radius-1 window fit: features={len(feats)} rank={rank} max|err|={err.max():.4f} mean|err|={err.mean():.4f}")
bad=[(keys[i],ys[i],round(pred[i],3)) for i in np.argsort(-err)[:6]]
print("worst:",bad)
inv={v:k for k,v in feats.items()}
print("weights:", {inv[j]:round(w[j],3) for j in range(len(feats)) if abs(w[j])>0.01})
