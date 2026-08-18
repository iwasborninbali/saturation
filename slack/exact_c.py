"""exact_c.py — Theorem C in exact form (second solver, 19.08): for the class-cycles of P_k = H(1) ∪ H(k) with s(v) = number of (4,8,4)-groups
containing class v, A_c = sum of s over kappa-classes of cycle c, B_c = over mu-classes, R = max over cycles of the range (max - min over prefixes)
of the walk W_i = sum_{j<=i} (+s at kappa, -s at mu):
     alpha(P_k) <= 4(p-1) - (2*G8 - 2*sum_c |A_c - B_c|)/R.
Verified against the class-level LP with uniform t = 1/R (the LP can only be better).  usage: python3 slack/exact_c.py p k [p k ...]"""
import sys; sys.path.insert(0, 'slack')
from cyc_model import build, lp
args = [int(x) for x in sys.argv[1:]]
for p, k in zip(args[::2], args[1::2]):
    M = build(p, k); G8 = len(M['groups'])
    s = {}
    for g, cl in M['groups']:
        for v in cl: s[v] = s.get(v, 0) + 1
    R = 0; imb = 0
    for seq in M['cycles']:
        W = 0; mx = mn = 0
        for i, v in enumerate(seq):
            W += s.get(v, 0) * (1 if i % 2 == 0 else -1); mx = max(mx, W); mn = min(mn, W)
        imb += abs(W); R = max(R, mx - mn)
    saving = (2 * G8 - 2 * imb) / R
    sav_lp, _, _ = lp(M, t_fixed={g: 1.0 / R for g, _ in M['groups']})
    print(f"p={p} k={k}: G8={G8} cycles={len(M['cycles'])} R={R} sum|A-B|={imb} -> saving {saving:.2f} => alpha <= {4*(p-1)-saving:.2f} = {(4*(p-1)-saving)/(p-1):.4f}(p-1); LP(t=1/R) net {sav_lp:.2f}", flush=True)
