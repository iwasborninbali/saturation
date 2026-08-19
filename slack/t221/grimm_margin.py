"""grimm_margin.py — the TRUE Hall margin for Grimm's conjecture.
surplus(run) := max s such that a perfect matching survives the deletion of ANY s-1 primes
              = min over nonempty S of (|N(S)| - |S|) + 1   (Hall's defect form).
We compute it directly for small values (which is what matters): surplus >= 1 iff a matching exists;
surplus >= 2 iff a matching survives deleting any single prime; etc.  Capped at CAP.
usage: python3 grimm_margin.py N [CAP]"""
import sys
from itertools import combinations
def spf_sieve(N):
    spf=list(range(N+1)); i=2
    while i*i<=N:
        if spf[i]==i:
            for j in range(i*i,N+1,i):
                if spf[j]==j: spf[j]=i
        i+=1
    return spf
def facs(x,spf):
    s=set()
    while x>1:
        p=spf[x]; s.add(p)
        while x%p==0: x//=p
    return s
def has_matching(adj,k,banned):
    matchR={}
    def try_(u,seen):
        for v in adj[u]:
            if v in banned or v in seen: continue
            seen.add(v)
            if v not in matchR or try_(matchR[v],seen):
                matchR[v]=u; return True
        return False
    for u in range(k):
        if not try_(u,set()): return False
    return True
def surplus(adj,k,cap):
    if not has_matching(adj,k,set()): return 0
    uni=set()
    for a in adj: uni|=a
    s=1
    while s<cap:
        bad=False
        for T in combinations(sorted(uni),s):
            if not has_matching(adj,k,set(T)): bad=True; break
        if bad: return s
        s+=1
    return cap
def run(N,cap):
    spf=spf_sieve(N); primes=[i for i in range(2,N+1) if spf[i]==i]
    from collections import defaultdict
    byk=defaultdict(lambda:[10**9,0]); bywin=defaultdict(lambda:[10**9,0])
    tight=[]
    for a,b in zip(primes,primes[1:]):
        k=b-a-1
        if k==0: continue
        adj=[facs(x,spf) for x in range(a+1,b)]
        s=surplus(adj,k,cap)
        key=1 if k<=2 else (2 if k<=5 else (3 if k<=10 else (4 if k<=20 else 5)))
        B=byk[key]; B[0]=min(B[0],s); B[1]+=1
        import math
        w=int(math.log10(max(b,10)))
        W=bywin[w]; W[0]=min(W[0],s); W[1]+=1
        if s<=1 and k>=6: tight.append((a+1,b-1,k,s))
    names={1:"k<=2",2:"k=3..5",3:"k=6..10",4:"k=11..20",5:"k>20"}
    print(f"N={N} cap={cap}")
    print(" по длине серии: " + "; ".join(f"{names[j]}: мин={byk[j][0]} (серий {byk[j][1]})" for j in sorted(byk)))
    print(" по десятичным окнам: " + "; ".join(f"10^{w}: мин={bywin[w][0]} (серий {bywin[w][1]})" for w in sorted(bywin)))
    print(f" «тугих» серий (запас<=1, длина>=6): {len(tight)}"+(f"; примеры {tight[:4]}" if tight else ""))
run(int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv)>2 else 4)
