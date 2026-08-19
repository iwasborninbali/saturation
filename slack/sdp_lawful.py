"""sdp_lawful.py — H1 experiment: level-1 Lasserre/Lovász–Schrijver SDP for the largest lawful subset of P_{-1} = (H(1) ∪ H(−1)) ∩ box,
box = [-(p-1)/2, -(p-1)/2 + 2p) × [0, 2p) (HJSW), constraints: every line with ≥3 points ℓ: Σ_{i∈ℓ} x_i ≤ 2, lifted:
  variables: y_i = E[x_i], Y_ij = E[x_i x_j]; M = [[1, y^T],[y, Y]] ⪰ 0, Y_ii = y_i, 0 ≤ Y_ij ≤ min(y_i, y_j), Y_ij ≥ y_i + y_j − 1;
  for each line ℓ and each point k:  Σ_{i∈ℓ} Y_ik ≤ 2 y_k  and  Σ_{i∈ℓ} (y_i − Y_ik) ≤ 2 (1 − y_k);   also Σ_{i∈ℓ} y_i ≤ 2.
Compare with LP(all) (rank-1 cover LP) and the exact maxima.  usage: sdp_lawful.py p [p ...]"""
import sys, math, numpy as np, cvxpy as cp, time
sys.path.insert(0, 'slack')
from lp_curve import lines, solve as lp_solve
def points_pm1(p):
    x0 = -(p - 1) // 2; y0 = 0
    pts = set()
    for x in range(1, p):
        for y in (pow(x, -1, p), (-pow(x, -1, p)) % p):
            for X in (x0 + ((x - x0) % p), x0 + ((x - x0) % p) + p):
                for Y in (y0 + ((y - y0) % p), y0 + ((y - y0) % p) + p):
                    pts.add((X, Y))
    return sorted(pts)
exact = {11: 32, 13: 40, 17: 54, 19: 59}
for p in map(int, sys.argv[1:]):
    pts = points_pm1(p); n = len(pts)
    ls = lines(pts, 'all')
    lp = lp_solve(pts, ls)
    t0 = time.time()
    y = cp.Variable(n); Y = cp.Variable((n, n), symmetric=True)
    M = cp.bmat([[np.ones((1, 1)), cp.reshape(y, (1, n), order='C')], [cp.reshape(y, (n, 1), order='C'), Y]])
    cons = [M >> 0, cp.diag(Y) == y, Y >= 0, y <= 1]
    # Y_ij <= y_i, Y_ij <= y_j, Y_ij >= y_i + y_j - 1
    ones = np.ones((n, 1))
    cons += [Y <= cp.reshape(y, (n, 1), order='C') @ ones.T, Y >= cp.reshape(y, (n, 1), order='C') @ ones.T + ones @ cp.reshape(y, (1, n), order='C') - 1]
    for s in ls:
        idx = list(s)
        cons.append(cp.sum(y[idx]) <= 2)
        # lifted: for each k: Σ_{i∈ℓ} Y_ik ≤ 2 y_k ; Σ_{i∈ℓ} (y_i − Y_ik) ≤ 2(1 − y_k)
        S = cp.sum(Y[idx, :], axis=0)              # vector over k
        cons.append(S <= 2 * y)
        cons.append(cp.sum(y[idx]) - S <= 2 * (1 - y))
    prob = cp.Problem(cp.Maximize(cp.sum(y)), cons)
    try:
        prob.solve(solver=cp.CLARABEL, verbose=False)
    except Exception as e:
        prob.solve(solver=cp.SCS, verbose=False, eps=1e-6, max_iters=20000)
    print(f"p={p}: n={n} lines>=3: {len(ls)}  LP(all)={lp:.2f} ({lp/(p-1):.3f}(p-1))  SDP1={prob.value:.2f} ({prob.value/(p-1):.3f}(p-1))  exact={exact.get(p,'?')} ({exact.get(p,0)/(p-1):.3f}(p-1))  [{time.time()-t0:.0f}s]", flush=True)
