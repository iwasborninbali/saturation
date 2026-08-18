"""f(t) = max |S ∩ H(k)| over lawful S ⊆ P_k with |S ∩ H(1)| >= 3(p-1) - t   (MIP, HiGHS)"""
import sys, time; sys.path.insert(0,'/home/claude/saturation/slack')
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix, vstack, csr_matrix
from maxlawful_pysat import cands_M, lines
p=int(sys.argv[1]); k=int(sys.argv[2]); tmax=int(sys.argv[3]); tl=int(sys.argv[4]) if len(sys.argv)>4 else 600
N=2*p; h=(p-1)//2; cands=cands_M(p,{1,k%p},N); n=len(cands)
inH1=np.array([1 if ((x-h)*y-1)%p==0 else 0 for x,y in cands]); inH2=1-inH1
L=lines(cands); A=lil_matrix((len(L),n))
for i,mem in enumerate(L):
    for j in mem: A[i,j]=1
A=A.tocsr()
for t in range(0,tmax+1):
    cons=[LinearConstraint(A,-np.inf,2), LinearConstraint(csr_matrix(inH1.reshape(1,-1)), 3*(p-1)-t, np.inf)]
    t0=time.time(); r=milp(-inH2.astype(float),constraints=cons,integrality=np.ones(n),bounds=Bounds(0,1),options={"time_limit":tl})
    if r.x is None: print(f"p={p} k={k} t={t}: infeasible/none", flush=True); continue
    x=np.round(r.x); s1=int((x*inH1).sum()); s2=int((x*inH2).sum())
    print(f"p={p} k={k}: t={t}: max|S2|={s2} (bound {-r.mip_dual_bound:.1f}) with |S1|={s1} => |S|={s1+s2} = 3(p-1)+{s1+s2-3*(p-1)}  [{time.time()-t0:.0f}s]", flush=True)
