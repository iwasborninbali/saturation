"""large_p.py -- Task C: push the QUADRUPLE H(1) u H(-1) u H(k) u H(-k) and the PAIR H(1) u H(-1)
(as a control) to larger p using ONLY the null-move simulated annealer (exact CP-SAT does not scale
here).  Question: does the quad's advantage over 3(p-1) ~ 1.5N (seen at p=11,13) persist as p grows,
or is it a small-p artefact swamped by the same O(1)/O(p) corrections that make the pair itself read
well above 1.5N at small p?

Method: for each p in a target list and each k in {2,3,5}, run anneal() (null_search.py) with a fixed
total time budget split across a few seeds; keep the best feasible set found; independently CERTIFY it
(re-derive, from scratch, every line through >=3 of the claimed points, by grouping on reduced
slope+intercept -- mathematically equivalent to testing every triple for collinearity, just done in
O(n^2) instead of O(n^3)) before reporting its size.  Also run the pair as a control at the same p, so
that the quad/pair ratio measures the quad's true advantage net of the annealer's own under-performance
(the annealer does not reach the exact pair optimum at all p; the conjectured true pair value is
3(p-1)+O(1)).

usage: large_p.py [budget_seconds] [seeds]   (defaults: 120s per (p,k) config, 2 seeds)
"""
import sys, time, math
sys.path.insert(0, '/home/pmbot/projects/saturation_peer/slack')
from diffusion_sampler import hyper_points, build_lines
from null_search import anneal

LOG = '/home/pmbot/projects/saturation_peer/slack/verification/shells_large_p.txt'


def certify(pts, idx):
    """Independent brute-force-style certification.  Re-derives, from a clean function with no
    shared state with anneal(), every line through >=3 of the points in the claimed set S = pts[idx];
    grouping by reduced (dx,dy,c) is exactly equivalent to checking every triple (i,j,l) for
    collinearity (a triple is collinear iff all three fall in the same (dx,dy,c) group), so this is
    the "iterate over all lines" brute-force check called for in the task hygiene requirement.
    Returns (ok: bool, offending_line_or_None)."""
    S = [pts[i] for i in idx]
    if len(S) != len(set(S)):
        return False, "duplicate point in claimed set"
    from collections import defaultdict
    L = defaultdict(int)
    n = len(S)
    for i in range(n):
        x1, y1 = S[i]
        for j in range(i + 1, n):
            x2, y2 = S[j]
            dx, dy = x2 - x1, y2 - y1
            g = math.gcd(abs(dx), abs(dy)); dx //= g; dy //= g
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            key = (dx, dy, dy * x1 - dx * y1)
            L[key] += 1
            if L[key] >= 3:
                return False, key
    return True, None


def run_config(p, cs, name, budget, seeds, log):
    pts = hyper_points(p, cs)
    lines = build_lines(pts)
    per_seed = budget / seeds
    best = 0; bestS = []
    t0 = time.time()
    for s in range(seeds):
        v, idxs = anneal(pts, lines, seconds=per_seed, seed=s)
        if v > best:
            best, bestS = v, idxs
    ok, bad = certify(pts, bestS)
    el = time.time() - t0
    N = 2 * p
    msg = (f"p={p:4d} {name:9s}: points={len(pts):5d} lines(>=3pts)={len(lines):6d} "
           f"best={best:4d} certified={ok} "
           f"alpha/N={best/N:.4f} alpha/(p-1)={best/(p-1):.4f}  time={el:.0f}s")
    if not ok:
        msg += f"  CERTIFY-FAIL bad_line={bad}"
    print(msg, file=log, flush=True)
    print(msg, flush=True)
    return best, ok


if __name__ == '__main__':
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 120.0
    seeds = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    ps = [41, 53, 61, 71, 89, 101, 127]
    ks = [2, 3, 5]

    with open(LOG, 'a') as log:
        print(f"\n=== large_p.py run started {time.ctime()}  budget={budget}s/config  seeds={seeds} "
              f"p in {ps}  k in {ks} ===", file=log, flush=True)
        print(f"=== large_p.py run started {time.ctime()} ===", flush=True)
        summary = []
        for p in ps:
            pair_best, pair_ok = run_config(p, (1, p - 1), "pair", budget, seeds, log)
            row = {"p": p, "pair": pair_best, "pair_ok": pair_ok}
            for k in ks:
                cs = (1, p - 1, k % p, (p - k) % p)
                quad_best, quad_ok = run_config(p, cs, f"quad_k{k}", budget, seeds, log)
                ratio = quad_best / pair_best if pair_best else float('nan')
                adv = quad_best - pair_best
                msg = (f"p={p:4d} k={k}: quad={quad_best} pair={pair_best} "
                       f"quad-pair={adv:+d} quad/pair={ratio:.4f}")
                print(msg, file=log, flush=True)
                print(msg, flush=True)
                row[f"quad_k{k}"] = quad_best
                row[f"quad_k{k}_ok"] = quad_ok
                row[f"quad_k{k}_ratio"] = ratio
            summary.append(row)
        print("\n--- SUMMARY (best over k in {2,3,5} for the quad) ---", file=log, flush=True)
        print("--- SUMMARY ---", flush=True)
        for row in summary:
            p = row["p"]; pair = row["pair"]
            best_k, best_q = max(((k, row[f"quad_k{k}"]) for k in ks), key=lambda t: t[1])
            ratio = best_q / pair if pair else float('nan')
            line = (f"p={p:4d} N={2*p:4d}  pair={pair:4d} ({pair/(2*p):.4f}N, {pair/(p-1):.4f}(p-1))  "
                    f"best_quad(k={best_k})={best_q:4d} ({best_q/(2*p):.4f}N, {best_q/(p-1):.4f}(p-1))  "
                    f"quad/pair={ratio:.4f}  quad-pair={best_q-pair:+d}")
            print(line, file=log, flush=True)
            print(line, flush=True)
        print(f"=== done {time.ctime()} ===", file=log, flush=True)
        print(f"=== done {time.ctime()} ===", flush=True)
