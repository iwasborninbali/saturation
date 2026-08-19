"""blocking_orbits.py — for the pair: given a maximum lawful M of H(1) (orbit-wise), how are the blocking pairs of a point q in H(-1) spread
over the V-orbits of H(1)?  If every q is blocked by pairs from >= 2 distinct orbits, one deletion cannot unblock two q's at once."""
import sys
from collections import defaultdict
from itertools import combinations
def run(p):
    h=(p-1)//2; X=lambda u: u if u<=h else u-p; inv=lambda a: pow(a,p-2,p)
    base={a:(X(a),inv(a)) for a in range(1,p)}
    orb={a:frozenset({a,(p-inv(a))%p,inv(a),(p-a)%p}) for a in range(1,p)}
    H1=[]; owner={}
    for a in range(1,p):
        x0,y0=base[a]
        for r in (0,1):
            for s in (0,1):
                q=(x0+r*p,y0+s*p); H1.append(q); owner[q]=a
    H2=[(p-x,y) for (x,y) in H1]     # R-images: the second hyperbola
    # maximum M: orbit-wise unique/9 choices -> take the greedy orbit optimum (any one)
    def lawful(S):
        c=defaultdict(int)
        for (x,y) in S:
            for k in (('r',y),('c',x),('d',x-y),('a',x+y)):
                c[k]+=1
                if c[k]>2: return False
        return True
    M=set()
    orbits=defaultdict(list)
    for q in H1: orbits[orb[owner[q]]].append(q)
    for O,P in orbits.items():
        best=None
        for m in range(len(P),0,-1):
            for S in combinations(P,m):
                if lawful(S): best=S; break
            if best: break
        M|=set(best)
    assert lawful(M) and len(M)==3*(p-1), (len(M),3*(p-1))
    # blocking pairs of q in H2: pairs {a,b} in M collinear with q
    stat=[]
    for q in H2:
        pairs=[]
        for a,b in combinations(M,2):
            if (b[0]-a[0])*(q[1]-a[1])==(b[1]-a[1])*(q[0]-a[0]): pairs.append((a,b))
        os=defaultdict(int)
        for a,b in pairs:
            os[frozenset({orb[owner[a]],orb[owner[b]]})]+=1
        norb=len({o for pr in pairs for o in (orb[owner[pr[0]]],orb[owner[pr[1]]])})
        stat.append((len(pairs),norb))
    import statistics as st
    npairs=[s[0] for s in stat]; norbs=[s[1] for s in stat]
    print(f"p={p}: |M|={len(M)}  blocking pairs per q: min={min(npairs)} mean={st.mean(npairs):.1f} max={max(npairs)}; "
          f"distinct orbits touched: min={min(norbs)} mean={st.mean(norbs):.1f} max={max(norbs)}; q with 0 pairs: {sum(1 for n in npairs if n==0)}; "
          f"q blocked within a single orbit: {sum(1 for n in norbs if n<=1)}")
for p in map(int,sys.argv[1:]): run(p)
