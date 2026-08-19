"""constant.py — the block constant from the descent law (first solver) and the saving table (second solver).
Signature <-> xi-chain dictionary (first solver, THREAD[167]):
  interior vertex i (between edges i and i+1):  (xi_{i-1}, xi_i) = (0,1) -> (8,4,4)='8';  (1,0) -> (6,6,2,2)='6';  else (7,5,3,1)='7'
  left end: '(4,2,2)'='a' iff xi_1 = 1, else 'b';   right end: 'a' iff xi_{k-1} = 0, else 'b'.
Density of a run of length k with descent set S: 2^{-(k+2)} * D_k(S)/k!,  D_k(S) = #permutations of [k] with descent set exactly S.
Saving/p = sum_k sum_S density * sav(signature(S)); alpha <= 4(p-1) - saving."""
import json, sys
from math import factorial
from itertools import product

def beta_le(k, S):   # #permutations with descent set CONTAINED in S -> multinomial
    S=sorted(S); parts=[]; prev=0
    for s in S: parts.append(s-prev); prev=s
    parts.append(k-prev)
    r=factorial(k)
    for a in parts: r//=factorial(a)
    return r

def D(k,S):          # exact descent set: inclusion-exclusion
    S=set(S); tot=0
    subs=[[]]
    for x in sorted(S):
        subs=subs+[t+[x] for t in subs]
    for T in subs:
        tot += (-1)**(len(S)-len(T))*beta_le(k,T)
    return tot

def sig_of(xi):      # xi = tuple of k-1 bits (xi_1..xi_{k-1})
    k=len(xi)+1
    out=['a' if xi[0]==1 else 'b']
    for i in range(1,k-1):
        pair=(xi[i-1],xi[i])
        out.append('8' if pair==(0,1) else ('6' if pair==(1,0) else '7'))
    out.append('a' if xi[-1]==0 else 'b')
    return ''.join(out)

tab=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'slack/t221/fast_sig_table.json'))['saving']
K=int(sys.argv[2]) if len(sys.argv)>2 else 8
tot=0.0; missing=0.0; rows=[]
for k in range(2,K+1):
    dens_k=2.0**(-(k+2)); sub=0.0; miss=0.0
    for xi in product((0,1),repeat=k-1):
        S=[i+1 for i,b in enumerate(xi) if b==1]
        d=dens_k*D(k,S)/factorial(k)
        s=sig_of(xi); s=min(s,s[::-1])
        if s in tab: sub+=d*tab[s]
        else: miss+=d
    tot+=sub; missing+=miss
    rows.append((k,sub,miss))
    print(f"  k={k}: contribution={sub:.5f}  (density of signatures missing from the table: {miss:.6f})")
print(f"\nsaving/p (k<={K}) = {tot:.4f}  =>  alpha <= {4-tot:.4f} (p-1)")
tail=sum(2.0**(-(k+2))*4*(k-1) for k in range(K+1,60))
print(f"tail bound (k>{K}, using sav <= 4(k-1)): {tail:.4f}  =>  full constant in [{4-tot-tail:.4f}, {4-tot:.4f}]")
