"""Independent set of seven-orbits in the neighbour graph (edges: e^2 = d^2 +- 4), restricted to seven-orbits with no good neighbour.
The graph is a subgraph of the path x -> x+4 on F_p \ {0} (x = d^2), so components are paths and max independent set = sum ceil(L/2)."""
import sys
from collections import defaultdict
def run(p):
    inv=lambda x: pow(x,p-2,p); h=(p-1)//2; X=lambda u: u if u<=h else u-p
    sig=defaultdict(list); tau=defaultdict(list)
    for t in range(1,p):
        sig[(t-inv(t))%p].append(t); tau[(t+inv(t))%p].append(t)
    typ={}
    for d in range(1,p):
        if len(sig[d])==2 and len(tau[d])==2:
            a=sig[d][0]; b=tau[d][0]
            ss=(X(a)>0)!=(X(inv(a))>0); ts=(X(b)>0)==(X(inv(b))>0)
            typ[d]='8' if (ss and ts) else ('7' if (ss or ts) else '6')
    # orbits indexed by x = d^2
    xtype={}
    for d,t in typ.items(): xtype[(d*d)%p]=t
    good={x for x,t in xtype.items() if t=='8'}; seven={x for x,t in xtype.items() if t=='7'}
    n7=len(seven)
    V={x for x in seven if ((x+4)%p not in good) and ((x-4)%p not in good)}
    clean={x for x in V if ((x+4)%p not in seven) and ((x-4)%p not in seven)}
    # components (paths) in V under x ~ x+4
    seen=set(); indep=0; comps=0; lengths=defaultdict(int)
    for x in V:
        if x in seen: continue
        # walk to the left end
        y=x
        while (y-4)%p in V and (y-4)%p!=x: y=(y-4)%p
        L=0; z=y
        while z in V and z not in seen:
            seen.add(z); L+=1; z=(z+4)%p
        indep+=(L+1)//2; comps+=1; lengths[L]+=1
    return n7,len(clean),len(V),indep,dict(sorted(lengths.items()))
tot=defaultdict(int)
for p in map(int,sys.argv[1:]):
    n7,c,v,i,lens=run(p)
    tot['n7']+=n7; tot['clean']+=c; tot['V']+=v; tot['indep']+=i
    print(f"p={p}: 7-orbits={n7} clean={c} ({c/n7:.3f}) V(no good nb)={v} ({v/n7:.3f}) indep={i} ({i/n7:.3f}) path lengths={lens}")
print("pooled: clean/n7=%.4f  V/n7=%.4f  indep/n7=%.4f  (model: 7/16=%.4f, 10/16=%.4f, >=17/32=%.4f)"%(tot['clean']/tot['n7'],tot['V']/tot['n7'],tot['indep']/tot['n7'],7/16,10/16,17/32))
