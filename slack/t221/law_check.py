import sys
from collections import defaultdict
def run(p,acc):
    h=(p-1)//2; inv=lambda x: pow(x,p-2,p); X=lambda u: u if u<=h else u-p
    # groups at residue d: sigma roots a: a-1/a=d ; tau roots b: b+1/b=d
    sig=defaultdict(list); tau=defaultdict(list)
    for t in range(1,p):
        sig[(t-inv(t))%p].append(t); tau[(t+inv(t))%p].append(t)
    for d in range(1,p):
        if len(sig[d])!=2 or len(tau[d])!=2: continue
        a=sig[d][0]; b=tau[d][0]
        ss=(X(a)>0)!=(X(inv(a))>0); ts=(X(b)>0)==(X(inv(b))>0)
        acc[(ss,ts)]+=1
acc=defaultdict(int)
for p in map(int,sys.argv[1:]): run(p,acc)
n=sum(acc.values()); both=acc[(True,True)]; neither=acc[(False,False)]; one=acc[(True,False)]+acc[(False,True)]
print(f"n={n} both={both/n:.4f} one={one/n:.4f} neither={neither/n:.4f}  P(sig shared|tau unshared)={acc[(True,False)]/(acc[(True,False)]+acc[(False,False)]):.4f}  P(tau shared|sig unshared)={acc[(False,True)]/(acc[(False,True)]+acc[(False,False)]):.4f} P(sig shared)={(both+acc[(True,False)])/n:.4f}")
