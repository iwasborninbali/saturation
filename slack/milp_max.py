"""milp_max.py — exact maximum lawful subset by mixed-integer programming (HiGHS via scipy.optimize.milp); witnesses verified by the law.
usage: milp_max.py M p N k1,k2,... secs | milp_max.py U p q N secs | milp_max.py PH p k N secs   (same candidate generators as maxlawful_pysat.py)"""
import sys, time, os
sys.path.insert(0, '/home/claude/saturation/slack'); sys.path.insert(0, '/home/claude/saturation')
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
from maxlawful_pysat import cands_M, cands_U, cands_PH, lines
import saturation as S
mode = sys.argv[1]
if mode == 'M':
    p, N = int(sys.argv[2]), int(sys.argv[3]); ks = {int(k) % p for k in sys.argv[4].split(',')}; tl = int(sys.argv[5]); cands = cands_M(p, ks, N); tag = f"M p={p} ks={sorted(ks)} N={N}"
elif mode == 'U':
    p, q, N = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); tl = int(sys.argv[5]); cands = cands_U(p, q, N); tag = f"U p={p} q={q} N={N}"
elif mode == 'PH':
    p, k, N = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); tl = int(sys.argv[5]); cands = cands_PH(p, k, N); tag = f"PH p={p} k={k} N={N}"
L = lines(cands); n = len(cands)
A = lil_matrix((len(L), n))
for i, mem in enumerate(L):
    for k in mem: A[i, k] = 1
print(f"{tag}: candidates={n} lines>=3={len(L)} time_limit={tl}s", flush=True)
t = time.time()
res = milp(-np.ones(n), constraints=LinearConstraint(A.tocsr(), -np.inf, 2), integrality=np.ones(n), bounds=Bounds(0, 1),
           options={"time_limit": tl, "disp": True})
print(res.message, flush=True)
if res.x is not None:
    x = np.round(res.x).astype(int); pts = sorted(cands[i] for i in range(n) if x[i] == 1)
    S.the_law(frozenset(a * N + b for (a, b) in pts), N)
    print(f"RESULT {tag}: MIP value = {-res.fun:.3f} status={res.status} time={time.time()-t:.1f}s dual_bound={-res.mip_dual_bound:.3f} gap={res.mip_gap}", flush=True)
    print("witness:", pts, flush=True)
