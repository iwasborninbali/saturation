"""other_unions.py -- TASK E: is the "quadruple of shells beats 3/2" effect special to hyperbola shells,
or does ANY union of a few algebraic curves in the HJSW box do the same?  Tests, all in the box
B = [-(p-1)/2, -(p-1)/2+2p) x [0, 2p), N = 2p:

  (i)   H(1) u {y = x^3 + c}                         (hyperbola + cubic, a few c)
  (ii)  {xy=1} u {x^2+y^2=1}                          (two conics of different type)
  (iii) {xy=1} u its image under (x,y)->(-x,y)         (= {xy=-1}, i.e. literally the known pair)
  (iv)  {(x-a)(y-b)=1} u {xy=1} for a few (a,b)        (two hyperbolas, DIFFERENT centres, not two shells)

Pipeline for every union: build the box point set (2x2 lifts per residue pair, same convention as
diffusion_sampler.hyper_points / lp_curve.curve_points: x0=-(p-1)//2, y0=0) -> build_lines (all lines
with >=3 collinear points) -> null_search.anneal (several seeds) for a lawful-set LOWER bound -> an
INDEPENDENT brute-force triple check on the returned point coordinates (not reusing the lines list) ->
lp_curve.solve for the fractional line-cover UPPER bound.

usage: other_unions.py [p1,p2,...] [seconds] [seeds]
"""
import sys, os, time, itertools

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from null_search import anneal
from diffusion_sampler import build_lines
from lp_curve import solve as lp_solve


def box(p):
    h = (p - 1) // 2
    return -h, 0


def lift(p, x0, y0, xy_pairs):
    P = set()
    for x, y in xy_pairs:
        x %= p; y %= p
        bx = x0 + ((x - x0) % p); by = y0 + ((y - y0) % p)
        for r in (0, 1):
            for s in (0, 1):
                P.add((bx + r * p, by + s * p))
    return P


def hyp_xy(p, c, a=0, b=0):
    """(x-a)(y-b) = c mod p, x,y in residues 0..p-1"""
    c %= p; a %= p; b %= p
    out = []
    for x in range(p):
        if (x - a) % p == 0:
            continue
        y = (b + c * pow((x - a) % p, -1, p)) % p
        out.append((x, y))
    return out


def cubic_xy(p, c):
    c %= p
    return [(x, (x * x * x + c) % p) for x in range(p)]


def circle_xy(p, c):
    c %= p
    out = []
    for x in range(p):
        x2 = (x * x) % p
        for y in range(p):
            if (x2 + y * y) % p == c:
                out.append((x, y))
    return out


def certify(pts):
    """independent brute-force collinearity check over ALL triples (does not reuse any lines list)."""
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        for j in range(i + 1, n):
            x2, y2 = pts[j]
            dx, dy = x2 - x1, y2 - y1
            for k in range(j + 1, n):
                x3, y3 = pts[k]
                if dx * (y3 - y1) - dy * (x3 - x1) == 0:
                    return False, (pts[i], pts[j], pts[k])
    return True, None


def evaluate(p, name, xy_union, seconds, seeds):
    x0, y0 = box(p)
    P = sorted(lift(p, x0, y0, xy_union))
    L = build_lines(P)
    best = 0; bestS = []
    for s in range(seeds):
        v, idxs = anneal(P, L, seconds=seconds, seed=s)
        if v > best:
            best, bestS = v, idxs
    Spts = [P[i] for i in bestS]
    ok, bad = certify(Spts)
    lpv = lp_solve(P, L)
    N = 2 * p
    line = (f"p={p} N={N} {name}: |pts|={len(P)} lines={len(L)}  alpha>={best} = {best/N:.3f}N "
            f"(certified indep.-brute-force: {'OK' if ok else 'FAIL '+str(bad)})  LP-upper={lpv:.2f} = {lpv/N:.3f}N")
    print(line, flush=True)
    return best, N, ok


if __name__ == '__main__':
    ps = [int(t) for t in sys.argv[1].split(',')] if len(sys.argv) > 1 else [11, 13, 17, 19]
    seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 8.0
    seeds = int(sys.argv[3]) if len(sys.argv) > 3 else 4

    t0 = time.time()
    print("=== TASK E: other superpositions vs the hyperbola quadruple ===", flush=True)
    print("Reference (known/exact, from prior sessions): pair H(1)uH(-1) alpha = 32,40,54,59 at p=11,13,17,19"
          " = 1.455N,1.538N,1.588N,1.553N.  Quadruple H(+-1)uH(+-2): alpha>=37 (1.68N) at p=11, >=44 (1.69N) at p=13"
          " (exact CP-SAT).  1.5N is the single-shell asymptotic constant.", flush=True)

    for p in ps:
        # (i) hyperbola + cubic, a few shifts c
        for c in (0, 1):
            evaluate(p, f"(i) H(1) u {{y=x^3+{c}}}", hyp_xy(p, 1) + cubic_xy(p, c), seconds, seeds)
        # (ii) two conics of different type
        evaluate(p, "(ii) {xy=1} u {x^2+y^2=1}", hyp_xy(p, 1) + circle_xy(p, 1), seconds, seeds)
        # (iii) hyperbola + its reflection image (x,y)->(-x,y):  xy=1 -> (-x)y=1 i.e. xy=-1 -- literally the pair
        refl = [((-x) % p, y) for (x, y) in hyp_xy(p, 1)]
        evaluate(p, "(iii) {xy=1} u refl_x{xy=1} (= known pair xy=1,xy=-1)", hyp_xy(p, 1) + refl, seconds, seeds)
        # (iv) shifted-centre pair: (x-a)(y-b)=1 union xy=1, for a few centres
        for (a, b) in ((1, 0), ((p - 1) // 2, (p - 1) // 2)):
            evaluate(p, f"(iv) {{(x-{a})(y-{b})=1}} u {{xy=1}}", hyp_xy(p, 1) + hyp_xy(p, 1, a, b), seconds, seeds)
        print(flush=True)

    print(f"[total wall time {time.time()-t0:.0f}s]", flush=True)
