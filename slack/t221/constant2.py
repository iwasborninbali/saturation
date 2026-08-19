"""constant2.py — constant from the STANDARD MODEL table (xi-pattern -> saving), no primes, no missing signatures."""
import json,sys
from math import factorial
from itertools import product
def beta_le(k,S):
    S=sorted(S); parts=[]; prev=0
    for s in S: parts.append(s-prev); prev=s
    parts.append(k-prev); r=factorial(k)
    for a in parts: r//=factorial(a)
    return r
def D(k,S):
    S=sorted(set(S)); subs=[[]]
    for x in S: subs=subs+[t+[x] for t in subs]
    return sum((-1)**(len(S)-len(T))*beta_le(k,T) for T in subs)
tab=json.load(open('slack/t221/standard_model.json'))
K=max(len(k)+1 for k in tab)
tot=0.0; miss=0.0
for k in range(2,K+1):
    for xi in product((0,1),repeat=k-1):
        key=''.join(map(str,xi)); d=2.0**(-(k+2))*D(k,[i+1 for i,b in enumerate(xi) if b])/factorial(k)
        v=tab.get(key)
        if v: tot+=d*v[0]
        else: miss+=d
tail=sum(2.0**(-(k+2))*4*(k-1) for k in range(K+1,80))
print(f"K={K}: saving/p >= {tot:.5f} (untabulated density {miss:.2e})  =>  alpha <= {4-tot:.4f}(p-1)")
print(f"tail (k>{K}) <= {tail:.5f}  =>  certificate constant in [{4-tot-tail:.4f}, {4-tot:.4f}]")
