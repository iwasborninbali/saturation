import sys
from collections import defaultdict
def run(p, acc):
    h=(p-1)//2
    pts=[(x,y) for x in range(-h,3*h+2) for y in range(0,2*p) if (x*y)%p in (1,p-1)]
    plus=defaultdict(lambda: defaultdict(list))
    for (x,y) in pts: plus[(x-y)%p][x-y].append((x,y))
    def prof(g): return tuple(sorted((len(v) for v in g.values()),reverse=True))
    ptype={d:prof(plus[d]) for d in plus}
    sqrt=defaultdict(list)
    for x in range(1,p): sqrt[(x*x)%p].append(x)
    inv=lambda x: pow(x,p-2,p)
    X=lambda u: u if u<=h else u-p
    for d in plus:
        if ptype[d]!=(7,5,3,1) or d>(p-1)//2: continue
        # sigma pair: a - 1/a = d  -> a roots of a^2 - d a - 1
        # which pair is shared? sigma shared iff sign X(a) != sign X(1/a) for a root a
        A=[a for a in range(1,p) if (a-inv(a))%p==d]
        B=[b for b in range(1,p) if (b+inv(b))%p==d]
        assert len(A)==2 and len(B)==2,(p,d,A,B)
        a=A[0]; sig_shared = (X(a)>0)!=(X(inv(a))>0)
        b=B[0]; tau_shared = (X(b)>0)==(X(inv(b))>0)
        assert sig_shared!=tau_shared,(p,d)
        # neighbours: e+^2=d^2+4 (shares H(1) classes = sigma side), e-^2 = d^2-4 (tau side)
        for side,s in (('sigma',4),('tau',p-4)):
            t=(d*d+s)%p
            es=set(min(e,p-e) for e in sqrt[t])
            assert len(es)==1,(p,d,es)
            e=es.pop()
            four = (e in ptype and sum(ptype[e])==16)
            usedn = e in ptype and ptype[e] in ((8,4,4),(7,5,3,1))
            key=('shared' if (side=='sigma')==sig_shared else 'unshared')
            acc[key]['n']+=1; acc[key]['four']+=four; acc[key]['used']+=usedn
            if four: acc[key]['used|four']+=usedn
            if e in ptype: acc[key]['type '+str(ptype[e])]+=1
acc=defaultdict(lambda: defaultdict(int))
for p in map(int,sys.argv[1:]): run(p,acc)
for k,v in acc.items():
    n=v['n']; print(k, 'n=',n, 'P(4-class)=%.3f'%(v['four']/n), 'P(used)=%.3f'%(v['used']/n), 'P(used|4-class)=%.3f'%(v['used|four']/max(v['four'],1)))
    print('   types:', {kk:round(vv/n,3) for kk,vv in v.items() if kk.startswith('type')})
