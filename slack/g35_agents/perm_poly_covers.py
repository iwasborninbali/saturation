"""perm_poly_covers.py — extension of the permutation-cubic cover numerics (G3.5) to other permutation
polynomials: f(x)=x^k with gcd(k,p-1)=1 (k=5,7,11) and the Dickson polynomial D_5(x,1)=x^5-5x^3+5x
(a permutation polynomial of F_p iff gcd(5,p^2-1)=1).

For each (f,p,box) computes:
  (a) cover/N : cost of "weight 1 on every slope-±1 line with >=4 lifted points + singletons" / N, N=2p
  (b) LPpm1/N : LP value over slope-±1 lines only (curve_points+lines('pm1')+solve), /N
  (c) LPall/N : LP value over all lines with >=3 points, /N
  (d) root-count histogram (0..k) of f(t)-t ≡ c and f(t)+t ≡ c over c in F_p, and the fraction of
      "same-class" root sets among residues with >=3 roots (class defined exactly as in the cubic note,
      §1: for slope +1, root t has class 0/1 according to which of the two lifts s_t-r_t in the box's
      2p-window equals c mod p; analogously for slope -1 with s_t+r_t).

usage: perm_poly_covers.py
"""
import sys, math
sys.path.insert(0, '/home/pmbot/projects/saturation_peer/slack')
from lp_curve import curve_points, lines, solve

def is_prime(n):
    if n < 2: return False
    for d in range(2, int(n**0.5) + 1):
        if n % d == 0: return False
    return True

def lifts(u, lo, p):
    v = lo + ((u - lo) % p)
    return [v, v + p]

def poly_dickson5_coeffs():
    # D_5(x,1) = x^5 - 5x^3 + 5x  -> Horner coeffs high->low: 1,0,-5,0,5,0
    return [1, 0, -5, 0, 5, 0]

def f_pow(k):
    return lambda x, p: pow(x, k, p)

def f_dickson5():
    c = poly_dickson5_coeffs()
    def f(x, p):
        v = 0
        for a in c:
            v = (v * x + a) % p
        return v
    return f

def curve_spec_pow(k):
    return f"pow:{k}"

def curve_spec_dickson5():
    c = poly_dickson5_coeffs()
    return "poly:" + ",".join(str(a) for a in c)

def cover_cost(p, curve, x0, y0):
    pts = curve_points(p, curve, x0, y0); n = len(pts)
    ls = lines(pts, 'pm1')
    big = [s for s in ls if len(s) >= 4]
    covered = set(i for s in big for i in s)
    L4 = len(big)
    cost = 2 * L4 + (n - len(covered))
    return cost, n

def lp_values(p, curve, x0, y0):
    pts = curve_points(p, curve, x0, y0)
    out = {}
    for mode in ('pm1', 'all'):
        ls = lines(pts, mode)
        out[mode] = solve(pts, ls)
    return out

def root_count_and_classes(p, f, x0, y0, sign):
    """sign=+1: c=f(t)-t;  sign=-1: c=f(t)+t.
    Returns dict c -> list of (t, class) with class in {0,1}."""
    groups = {}
    for t in range(p):
        y = f(t, p)
        c = (y - sign * t) % p  # sign=+1 -> f(t)-t ; sign=-1 -> f(t)+t  (store using c = y - sign*t)
        r_t = lifts(t, x0, p)[0]
        s_t = lifts(y, y0, p)[0]
        if sign == 1:
            d = s_t - r_t
            lo = y0 - x0 - p  # window (y0-x0-p, y0-x0+p), length 2p
        else:
            d = s_t + r_t
            lo = x0 + y0  # window [x0+y0, x0+y0+2p)
        # find the representative c' == d among the two integers ≡ c (mod p) in the length-2p window
        base = lo + ((d - lo) % p)  # smallest lift of d's residue >= lo, but we want base ≡ c mod p; d already ≡ c
        # base is smallest integer >= lo congruent to d mod p == c mod p
        cls = 0 if d == base else 1
        groups.setdefault(c, []).append((t, cls))
    return groups

def analyze_roots(p, f, k, x0, y0):
    result = {}
    for sign, name in ((1, '+'), (-1, '-')):
        groups = root_count_and_classes(p, f, x0, y0, sign)
        hist = {}
        same_count = 0
        multi_count = 0
        for c, lst in groups.items():
            r = len(lst)
            hist[r] = hist.get(r, 0) + 1
            if r >= 3:
                multi_count += 1
                classes = set(cl for (_, cl) in lst)
                if len(classes) == 1:
                    same_count += 1
        frac_same = same_count / multi_count if multi_count else float('nan')
        result[name] = dict(hist=hist, multi_count=multi_count, same_count=same_count, frac_same=frac_same)
    return result

def main():
    lines_out = []
    def log(s):
        print(s, flush=True)
        lines_out.append(s)

    families = []
    # x^k families, k=5,7,11
    for k in (5, 7, 11):
        primes = []
        cand = 149
        while len(primes) < 3 and cand < 340:
            if is_prime(cand) and math.gcd(k, cand - 1) == 1:
                primes.append(cand)
            cand += 1
        # also try to spread across 150-320
        primes = []
        cand = 151
        while cand < 321:
            if is_prime(cand) and math.gcd(k, cand - 1) == 1:
                primes.append(cand)
            cand += 1
        # pick 3 spread out
        if len(primes) >= 3:
            picks = [primes[0], primes[len(primes)//2], primes[-1]]
        else:
            picks = primes
        for p in picks:
            families.append((f"x^{k}", p, curve_spec_pow(k), f_pow(k), k))

    # dickson5 family: need gcd(5, p^2-1)=1
    primes = []
    cand = 151
    while cand < 321:
        if is_prime(cand) and math.gcd(5, cand * cand - 1) == 1:
            primes.append(cand)
        cand += 1
    if len(primes) >= 3:
        picks = [primes[0], primes[len(primes)//2], primes[-1]]
    else:
        picks = primes
    for p in picks:
        families.append(("D5(x,1)", p, curve_spec_dickson5(), f_dickson5(), 5))

    header = f"{'f':<8}{'p':<6}{'box':<14}{'cover/N':<10}{'LPpm1/N':<10}{'LPall/N':<10}{'hist+':<40}{'hist-':<40}{'sameFrac+':<10}{'sameFrac-':<10}"
    log(header)
    log("-" * len(header))

    for (fname, p, curve, f, k) in families:
        boxes = [(0, 0), (-(p - 1) // 2, 0)]
        for (x0, y0) in boxes:
            cost, n = cover_cost(p, curve, x0, y0)
            N = 2 * p
            cover_over_N = cost / N
            lp = lp_values(p, curve, x0, y0)
            lp_pm1_over_N = lp['pm1'] / N
            lp_all_over_N = lp['all'] / N
            roots = analyze_roots(p, f, k, x0, y0)
            hp = roots['+']; hm = roots['-']
            hist_p = dict(sorted(hp['hist'].items()))
            hist_m = dict(sorted(hm['hist'].items()))
            row = (f"{fname:<8}{p:<6}{str((x0,y0)):<14}{cover_over_N:<10.4f}{lp_pm1_over_N:<10.4f}{lp_all_over_N:<10.4f}"
                   f"{str(hist_p):<40}{str(hist_m):<40}{hp['frac_same']:<10.3f}{hm['frac_same']:<10.3f}")
            log(row)

    log("")
    log("Summary per family (±1-line explicit cover vs 1.5N):")
    seen = set()
    for (fname, p, curve, f, k) in families:
        if fname in seen: continue
        seen.add(fname)
        vals = []
        for (x0, y0) in [(0, 0), (-(p - 1) // 2, 0)]:
            cost, n = cover_cost(p, curve, x0, y0)
            vals.append(cost / (2 * p))
        below = all(v < 1.5 for v in vals)
        log(f"  {fname}: sample cover/N values {['%.3f'%v for v in vals]} (p={p}) -> "
            f"{'stays below 1.5 N' if below else 'reaches/exceeds 1.5 N'} on this sample.")

    with open('/home/pmbot/projects/saturation_peer/slack/verification/perm_poly_covers.txt', 'w') as fh:
        fh.write("\n".join(lines_out) + "\n")

if __name__ == '__main__':
    main()
