"""cube_rule_lp.py -- LP over ±1-lines for y=x^3 (p mod 3 == 2), classify lines by (slope,size,type),
and evaluate explicit fractional-weight rules (weight 1 on 4/5/6-lines + w3 on 3-lines of same-groups
[+ optional 1/2 on 2-point side-lines of split groups]) against the raw LP optimum.

usage: cube_rule_lp.py
"""
import sys, math
sys.path.insert(0, '/home/pmbot/projects/saturation_peer/slack')
from lp_curve import curve_points
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix

def diag_lines(pts, minlen=2):
    """All slope +-1 lines through pts with >= minlen points. Returns dict key(dx,dy,c)->sorted idx list."""
    idx = {P: i for i, P in enumerate(pts)}
    n = len(pts)
    L = {}
    for i in range(n):
        x1, y1 = pts[i]
        for j in range(i + 1, n):
            x2, y2 = pts[j]
            dx, dy = x2 - x1, y2 - y1
            if abs(dx) != abs(dy) or dx == 0:
                continue
            # normalize to dx=1
            sdx = 1 if dx > 0 else -1
            dxn, dyn = dx // (abs(dx)), dy // abs(dx)  # dx/|dx| in {1,-1}; but keep dy sign matching
            # simpler: normalized direction (1, s) with s = sign(dx)*sign(dy) via dy/dx
            s = 1 if (dx > 0) == (dy > 0) else -1
            c = y1 - s * x1   # y - s*x = const along the line
            key = (s, c)
            L.setdefault(key, set()).update((i, j))
    return {k: sorted(v) for k, v in L.items() if len(v) >= minlen}

def solve_full(pts, ls_dict):
    """ls_dict: key -> sorted idx list (len>=3 only, for LP). Returns obj, weights dict key->w, keys list."""
    keys = list(ls_dict.keys())
    n = len(pts); m = len(keys)
    A = lil_matrix((n, m + n))
    for k, key in enumerate(keys):
        for i in ls_dict[key]:
            A[i, k] = 1
    for i in range(n):
        A[i, m + i] = 1
    c = np.concatenate([2 * np.ones(m), np.ones(n)])
    res = linprog(c, A_ub=-A.tocsr(), b_ub=-np.ones(n), bounds=(0, None), method='highs')
    w = {keys[k]: res.x[k] for k in range(m)}
    return res.fun, w

def analyze(p, x0, y0, log):
    curve = 'cube'
    pts = curve_points(p, curve, x0, y0)
    n = len(pts)
    N3 = (p + 1) // 6  # +- O(1); exact split later from data
    all_diag = diag_lines(pts, minlen=2)
    lines3 = {k: v for k, v in all_diag.items() if len(v) >= 3}

    # 1) raw LP over pm1 lines (size>=3) + singletons
    obj, w = solve_full(pts, lines3)
    log.append(f"p={p} box=({x0},{y0}) N=2p={2*p} pts={n}")
    log.append(f"  raw LP(pm1, size>=3 lines + singletons): obj={obj:.4f} = {obj/(2*p):.4f} N")

    # classify lines by (slope, size); type by size: 6->same, 3->same(outer), {4,5}->split
    by_group = {}
    for key, idxs in lines3.items():
        s, c = key
        sz = len(idxs)
        typ = {6: 'same', 3: 'same(outer)', 5: 'split', 4: 'split'}.get(sz, 'other(dbl-root?)')
        by_group.setdefault((s, sz, typ), []).append(w[key])

    log.append("  line classification (slope,size,type): count, mean LP-weight")
    for k in sorted(by_group):
        vals = by_group[k]
        log.append(f"    slope={k[0]:+d} size={k[1]} type={k[2]:14s} count={len(vals):4d} mean_w={sum(vals)/len(vals):.4f}")

    n_same6 = sum(1 for k in by_group if k[1] == 6)
    n_same3 = sum(len(by_group[k]) for k in by_group if k[1] == 3)
    n_split5 = sum(len(by_group[k]) for k in by_group if k[1] == 5)
    n_split4 = sum(len(by_group[k]) for k in by_group if k[1] == 4)
    same6_cnt = sum(len(by_group[k]) for k in by_group if k[1] == 6)
    log.append(f"  counts: #6-lines={same6_cnt} #3-lines={n_same3} (expect 2x #6-lines) "
               f"#5-lines={n_split5} #4-lines={n_split4} (expect equal)")

    # 2-point 'side' lines of split groups: diagonal lines of size exactly 2 that are NOT part of a
    # >=3 group ambiguity -- just take all size==2 diagonal lines (rows/cols excluded since |dx|=|dy| forces diagonal)
    lines2 = {k: v for k, v in all_diag.items() if len(v) == 2}
    n_side2 = len(lines2)
    log.append(f"  #2-point diagonal side-lines (all slopes, incl. non-split-related): {n_side2}")

    # 2) explicit rule: weight 1 on size in {4,5,6}; weight w3 on size==3 lines; optional weight 1/2 on size==2 diagonal lines
    def rule_cost(w3, use_side2, side2_w=0.5):
        weight = {}
        for key, idxs in lines3.items():
            sz = len(idxs)
            if sz in (4, 5, 6):
                weight[key] = 1.0
            elif sz == 3:
                weight[key] = w3
        if use_side2:
            for key in lines2:
                weight[key] = side2_w
        covered = [0.0] * n
        line_cost = 0.0
        for key, wt in weight.items():
            if wt == 0:
                continue
            idxs = lines3.get(key) or lines2.get(key)
            line_cost += 2 * wt
            for i in idxs:
                covered[i] += wt
        singleton_cost = sum(max(0.0, 1.0 - c) for c in covered)
        return line_cost + singleton_cost

    log.append("  explicit rule costs (1 on 4/5/6-lines + w3 on 3-lines [+ optional 1/2 on 2pt side-lines]):")
    best = None
    for w3 in (0, 1/4, 1/3, 1/2, 1):
        for use_side2 in (False, True):
            cst = rule_cost(w3, use_side2)
            tag = f"w3={w3:.4f} side2={use_side2}"
            log.append(f"    {tag:28s} cost={cst:.4f} = {cst/(2*p):.4f} N")
            if best is None or cst < best[0]:
                best = (cst, tag)
    log.append(f"  BEST explicit rule: {best[1]} cost={best[0]:.4f} = {best[0]/(2*p):.4f} N")
    log.append(f"  baseline (note's rule, weight1 on 4/5/6-lines only): cost={rule_cost(0, False):.4f} = "
               f"{rule_cost(0, False)/(2*p):.4f} N  [theory: 4p-7.5*N3 = {4*p - 7.5*((p+1)/6):.2f}]")
    log.append("")
    return dict(p=p, x0=x0, y0=y0, n=n, obj=obj, best=best, N3=(p+1)/6)

if __name__ == '__main__':
    log = []
    results = []
    for p in (197, 293, 401):
        assert p % 3 == 2
        for (x0, y0) in ((0, 0), (-(p - 1) // 2, 0)):
            r = analyze(p, x0, y0, log)
            results.append(r)
            print("\n".join(log[-40:]), flush=True)

    with open('/home/pmbot/projects/saturation_peer/slack/verification/cube_rule_lp.txt', 'w') as f:
        f.write("\n".join(log))
        f.write("\n\nSUMMARY\n")
        for r in results:
            f.write(f"p={r['p']} box=({r['x0']},{r['y0']}) N3~{r['N3']:.1f} rawLP={r['obj']:.2f}({r['obj']/(2*r['p']):.4f}N) "
                     f"best_rule={r['best'][1]} cost={r['best'][0]:.2f}({r['best'][0]/(2*r['p']):.4f}N)\n")
    print("DONE")
