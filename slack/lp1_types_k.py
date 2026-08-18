"""lp1_types_k.py — T2.21 (third solver): LP(1) anatomy for a general second hyperbola H(k) (no R-mirror): group types, solitary savings of the
(4,8,4) groups (rows+cols+the group's 3 lines [+ its RR'-image, the only symmetry]), collective/restricted savings.
usage: python3 slack/lp1_types_k.py p k"""
import sys, numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
from collections import defaultdict, Counter
p=int(sys.argv[1]); k=int(sys.argv[2])%p; h=(p-1)//2
pts=[(x,y) for x in range(-h,3*h+2) for y in range(0,2*p) if (x*y)%p in (1,k)]
idx={q:i for i,q in enumerate(pts)}; n=len(pts)
lines=defaultdict(list)
for (x,y) in pts:
    lines[('r',y)].append(idx[(x,y)]); lines[('c',x)].append(idx[(x,y)])
    lines[('d',x-y)].append(idx[(x,y)]); lines[('a',x+y)].append(idx[(x,y)])
L=[(key,mem) for key,mem in lines.items() if len(mem)>=3]; sizes={key:len(mem) for key,mem in L}
def lp(keep):
    rows=[i for i,(key,mem) in enumerate(L) if keep(key)]
    data=[];ri=[];ci=[]
    for r,i in enumerate(rows):
        for j in L[i][1]: data.append(1.0); ri.append(r); ci.append(j)
    A=csr_matrix((data,(ri,ci)),shape=(len(rows),n))
    res=linprog(-np.ones(n),A_ub=A,b_ub=2*np.ones(len(rows)),bounds=[(0,1)]*n,method='highs')
    return -res.fun
V=lp(lambda key: True); S=4*(p-1)-V
grp=defaultdict(list); grpa=defaultdict(list)
for i,(x,y) in enumerate(pts): grp[(x-y)%p].append(i); grpa[(x+y)%p].append(i)
def prof(mem, key): 
    cs=Counter((pts[i][0]-pts[i][1]) if key=='d' else (pts[i][0]+pts[i][1]) for i in mem); return tuple(sorted(cs.values(),reverse=True))
tp={d:prof(m,'d') for d,m in grp.items()}; tpa={e:prof(m,'a') for e,m in grpa.items()}
cnt=Counter(tp.values()); cnta=Counter(tpa.values())
print(f"p={p} k={k}: LP(1)={V:.3f} = {V/(p-1):.4f}(p-1); saving S={S:.3f}; (+1)-group types: {sorted(cnt.items(), key=lambda kv:-kv[1])}; (-1)-group types: {sorted(cnta.items(), key=lambda kv:-kv[1])}")
# solitary savings of the 8-groups: (+1) group d with its RR'-image (-d-... : line c -> -c-p, residue d -> -d)
d8=[d for d,t in tp.items() if t==(8,4,4)]; e8=[e for e,t in tpa.items() if t==(8,4,4)]
sol=[]
for d in d8:
    dd={d,(-d)%p}
    Vo=lp(lambda key: key[0] in 'rc' or (key[0]=='d' and key[1]%p in dd)); sol.append(4*(p-1)-Vo)
sola=[]
for e in e8:
    ee={e,(-e)%p}
    Vo=lp(lambda key: key[0] in 'rc' or (key[0]=='a' and key[1]%p in ee)); sola.append(4*(p-1)-Vo)
print(f"   (4,8,4) groups: +1: {len(d8)}, -1: {len(e8)}; solitary saving of a group + its RR'-image (both +1): {sorted(Counter(np.round(sol,3)).items())}; -1 side: {sorted(Counter(np.round(sola,3)).items())}")
# all 8-groups together; all groups with >=5-lines; only lines >=5; only lines >=6; without 4-lines
Vall8=lp(lambda key: key[0] in 'rc' or (key[0]=='d' and tp[key[1]%p]==(8,4,4)) or (key[0]=='a' and tpa[key[1]%p]==(8,4,4)))
V5=lp(lambda key: key[0] in 'rc' or sizes[key]>=5); V6=lp(lambda key: key[0] in 'rc' or sizes[key]>=6); Vno4=lp(lambda key: key[0] in 'rc' or sizes[key]!=4)
def has5(key):
    if key[0]=='d': return max(tp[key[1]%p])>=5
    if key[0]=='a': return max(tpa[key[1]%p])>=5
    return True
Vg5=lp(has5)
print(f"   savings: all (4,8,4) groups' lines: {4*(p-1)-Vall8:.3f}; all groups with a >=5-line (all their lines): {4*(p-1)-Vg5:.3f}; only >=5-point lines: {4*(p-1)-V5:.3f}; only >=6: {4*(p-1)-V6:.3f}; all but 4-point lines: {4*(p-1)-Vno4:.3f}; total S={S:.3f}")
# marginal of each type (both slopes)
for t in sorted(set(cnt)|set(cnta), key=lambda t:-max(t)):
    Vwo=lp(lambda key: key[0] in 'rc' or (key[0]=='d' and tp[key[1]%p]!=t) or (key[0]=='a' and tpa[key[1]%p]!=t))
    Vonly=lp(lambda key: key[0] in 'rc' or (key[0]=='d' and tp[key[1]%p]==t) or (key[0]=='a' and tpa[key[1]%p]==t))
    print(f"   type {str(t):18s}: count +1/-1 = {cnt.get(t,0)}/{cnta.get(t,0)}; marginal Delta = {Vwo-V:.3f}; solitary Sol = {4*(p-1)-Vonly:.3f}", flush=True)
