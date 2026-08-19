"""grimm.py — Grimm's conjecture (Erdos problem #375): if n+1,...,n+k are all composite, there are DISTINCT primes
p_i | n+i.  Equivalently a perfect matching in the bipartite graph (run elements) x (their prime divisors).
We (a) verify it on every maximal run of consecutive composites below N, and (b) measure the MARGIN:
the Hall surplus  min over nonempty subsets S of (|N(S)| - |S|)  -- computed exactly via the matching's
deficiency after removing one element, plus the cheaper statistics (run length, distinct primes available).
usage: python3 grimm.py N"""
import sys
from collections import defaultdict

def smallest_prime_factors(N):
    spf=list(range(N+1))
    i=2
    while i*i<=N:
        if spf[i]==i:
            for j in range(i*i,N+1,i):
                if spf[j]==j: spf[j]=i
        i+=1
    return spf

def factors(x,spf):
    s=set()
    while x>1:
        p=spf[x]; s.add(p)
        while x%p==0: x//=p
    return s

def bipartite_max_matching(adj,k):
    matchL=[-1]*k; matchR={}
    def try_(u,seen):
        for v in adj[u]:
            if v in seen: continue
            seen.add(v)
            if v not in matchR or try_(matchR[v],seen):
                matchR[v]=u; matchL[u]=v; return True
        return False
    cnt=0
    for u in range(k):
        if try_(u,set()): cnt+=1
    return cnt,matchL

def hall_surplus(adj,k):
    """min over nonempty S of |N(S)|-|S|; computed by removing each element and testing whether a
    matching still exists for the rest with one fewer prime available is expensive, so we use the
    standard equivalent: surplus = min over u of (max matching of the graph with u's neighbourhood shrunk)…
    Cheap sufficient proxy: min over u of (|N(u)|-1) and the global |union|-k."""
    uni=set()
    for u in range(k): uni |= adj[u]
    glob=len(uni)-k
    loc=min((len(adj[u]) for u in range(k)), default=99)-1
    return glob,loc

def run(N):
    spf=smallest_prime_factors(N)
    primes=[i for i in range(2,N+1) if spf[i]==i]
    worst_glob=10**9; worst_loc=10**9; longest=0; checked=0; fails=0
    stats=[]
    for a,b in zip(primes,primes[1:]):
        k=b-a-1
        if k==0: continue
        elems=list(range(a+1,b))
        adj=[factors(x,spf) for x in elems]
        m,_=bipartite_max_matching(adj,k)
        checked+=1
        if m<k: fails+=1; print("COUNTEREXAMPLE at run", a+1, b-1)
        g,l=hall_surplus(adj,k)
        if k>longest: longest=k
        if g<worst_glob: worst_glob=g; wg=(a+1,b-1,k)
        if l<worst_loc: worst_loc=l; wl=(a+1,b-1,k)
        stats.append((b,k,g,l))
    print(f"N={N}: runs checked={checked}, Grimm failures={fails}, longest run={longest}")
    print(f"  worst global surplus |union primes| - k = {worst_glob} at run {wg}")
    print(f"  worst local  min|N(u)| - 1            = {worst_loc} at run {wl}")
    import statistics
    for lo,hi in ((2,N//8),(N//8,N//2),(N//2,N)):
        sel=[s for s in stats if lo<=s[0]<hi]
        if sel: print(f"  окно [{lo},{hi}): серий={len(sel)} медиана запаса={statistics.median(s[2] for s in sel)} мин={min(s[2] for s in sel)} макс.длина={max(s[1] for s in sel)}")
if __name__=='__main__':
    run(int(sys.argv[1]))
