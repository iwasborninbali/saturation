"""lp_bound.py — LP relaxation of "max lawful subset" for a candidate set: max Σx, Σ_{q∈ℓ} x_q ≤ 2 for every line ℓ
with ≥3 candidates, 0 ≤ x ≤ 1 (HiGHS via scipy).  Also the trivial double-counting bound Z + 2|L|.
usage: lp_bound.py M p N k1,k2,...   (union of hyperbolas xy≡k_i mod p, HJSW x-shift, window N×N)
       lp_bound.py U p q N            (xy≡1 mod p ∪ xy≡1 mod q, each with its own HJSW x-shift)
       lp_bound.py file cands.txt"""
import sys, os
from math import gcd
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from maxlawful_pysat import cands_M, cands_U, lines


def lp_bound(cands, verbose=True):
    L = lines(cands); n = len(cands)
    A = lil_matrix((len(L), n))
    for i, mem in enumerate(L):
        for k in mem: A[i, k] = 1
    res = linprog(-np.ones(n), A_ub=A.tocsr(), b_ub=2 * np.ones(len(L)), bounds=[(0, 1)] * n, method="highs")
    on = set(k for mem in L for k in mem); Z = n - len(on)
    if verbose:
        print(f"candidates={n} lines>=3: {len(L)}  Z={Z}  Z+2|L|={Z + 2 * len(L)}  LP={-res.fun:.4f}")
    return -res.fun, res.x, L, Z


if __name__ == "__main__":
    if sys.argv[1] == "M":
        p, N = int(sys.argv[2]), int(sys.argv[3]); ks = {int(k) % p for k in sys.argv[4].split(",")}
        cands = cands_M(p, ks, N); print(f"M p={p} ks={sorted(ks)} N={N}: ", end="")
    elif sys.argv[1] == "U":
        p, q, N = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); cands = cands_U(p, q, N); print(f"U p={p} q={q} N={N}: ", end="")
    else:
        cands = [tuple(map(int, l.split()[:2])) for l in open(sys.argv[2]) if l.strip()]; print(f"file {sys.argv[2]}: ", end="")
    lp_bound(cands)
