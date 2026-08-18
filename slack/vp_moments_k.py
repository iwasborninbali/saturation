"""vp_moments_k.py — T2.11 (third solver): trace moments of C_p (vertical-pair model, k=-1) up to high order against the semicircle
(Wigner) prediction. For each prime: m_2k = tr C^{2k}/(p-1) for k=1..K, rho_k = m_2k/(m_2^k Cat_k) and rho_k^{1/k}; the exact
'doubled-tree' (backtracking-walk) part of tr C^4 and tr C^6 computed from the row-norm profile (rn_a^2 = sum_b C_ab^2, W = C∘C):
  tree_2 = 2 sum_a rn_a^4,  tree_3 = 2 sum_a rn_a^6 + 3 (rn^2)^T W (rn^2)   (Cat_2 = 2, Cat_3 = 5 plane trees; homogeneous rows -> Cat_k m_2^k (p-1)),
so that excess_k = (tr C^{2k} - tree_k)/tree_k isolates the genuine cycle contribution; the empirical spectral distribution of
lambda/sqrt(m_2) against the semicircle on [-2,2] (Kolmogorov distance, fraction of mass outside [-2,2]).
usage: python3 slack/vp_moments_k.py K p1 p2 ..."""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/',1)[0])
from vp_traces import build
from math import comb
def cat(k): return comb(2*k,k)//(k+1)
K=int(sys.argv[1])
for a in sys.argv[2:]:
    p=int(a); E,C,nt=build(p); n=p-1
    lam=np.linalg.eigvalsh(C); m2=(lam**2).sum()/n
    rn2=(C**2).sum(axis=1); W=C**2
    tree2=2*(rn2**2).sum(); tree3=2*(rn2**3).sum()+3*rn2@W@rn2
    t4=(lam**4).sum(); t6=(lam**6).sum()
    print(f"p={p}: E/(p-1)={E/n:.2f}  m2={m2:.3f}  lam_min={lam[0]:.3f} (={lam[0]/np.sqrt(m2):.3f} sqrt m2)  lam_max={lam[-1]:.3f} (={lam[-1]/np.sqrt(m2):.3f} sqrt m2)  rn2 max/mean={rn2.max()/rn2.mean():.3f} min/mean={rn2.min()/rn2.mean():.3f}")
    print("   k:      "+" ".join(f"{k:8d}" for k in range(1,K+1)))
    rho=[(lam**(2*k)).sum()/n/(m2**k*cat(k)) for k in range(1,K+1)]
    print("   rho_k:  "+" ".join(f"{r:8.3f}" for r in rho))
    print("   rho^1/k:"+" ".join(f"{r**(1/k):8.3f}" for k,r in zip(range(1,K+1),rho)))
    print(f"   tree parts: tr C^4 = {t4:.1f}, doubled-tree part {tree2:.1f} (ratio {t4/tree2:.3f}, cycle excess {(t4-tree2)/tree2:+.3f});"
          f"  tr C^6 = {t6:.1f}, tree part {tree3:.1f} (ratio {t6/tree3:.3f}, excess {(t6-tree3)/tree3:+.3f})")
    # empirical spectral distribution vs semicircle
    x=np.sort(lam/np.sqrt(m2)); F=np.arange(1,n+1)/n
    sc=lambda t: np.where(t<=-2,0,np.where(t>=2,1,0.5+(t*np.sqrt(np.maximum(4-t*t,0))+4*np.arcsin(np.clip(t/2,-1,1)))/(4*np.pi)))
    ks=max(np.abs(F-sc(x)).max(), np.abs((F-1/n)-sc(x)).max())
    out=np.mean(np.abs(x)>2)
    print(f"   ESD vs semicircle(var m2): KS distance {ks:.3f}; mass outside [-2,2]: {out:.3f} ({int(out*n)} eigenvalues); quantiles of |lam|/sqrt(m2) at 90/99%: {np.quantile(np.abs(x),0.9):.2f}/{np.quantile(np.abs(x),0.99):.2f}", flush=True)
