"""clean_counts.py -- T2.21 agent task B: clean 7-groups and the resulting bound, k = -1.

Setting (matches slack/lp1_anatomy.py, slack/lp1_types.py, docs/research/pair_bound_notes.md section 24
and B.19 with its addendum (a)-(c), lines ~962-1035): p odd prime, h = (p-1)//2,
    P = { (x,y) in [-h, 3h+1] x [0, 2p-1] : x*y mod p in {1, p-1} }        (|P| = 8(p-1))
Slope-(+1) residue group G_d (d in Z/p) = points of P on integer lines x-y = c, c == d (mod p); type(G_d)
= sorted-descending profile of its integer-line sizes. Slope-(-1) groups are the R-images, R:(x,y)->(p-x,y).
Orbit  Omega_d := G_d u G_{-d} u G'_d u G'_{-d}  (both slopes, both signs) = { q in P : (x-y)%p in {d,-d} }
                                                                             u { q in P : (x+y)%p in {d,-d} }
(the two expressions agree with B.19 addendum (a); Omega_d = Omega_{-d} as SETS, so orbits are indexed by
the canonical representative d in {0,...,h}; d=0 is the self-paired "central" orbit and is excluded from
all *orbit-level* tallies below, matching the task's "count orbits, i.e. pairs +-d").

CLASSIFICATION (section 24, F1/F2; verified here against both slack/km1_lines_5678.py's O(p^2) reference
computation and against brute-force point enumeration -- see clean_counts_verify.py):
4-class group (nk=2 kappa classes, nl=2 lambda classes) has profile (m, m+4, 8-m, 4-m) with
    m=4 (both pairs share centre)  -> type (8,4,4)      "m8"
    m in {1,3} (exactly one shared)-> type (7,5,3,1)     "m7"
    m=2 (neither shared)           -> type (6,6,2,2)     "m6g"   (each such group has TWO 6-point lines;
                                                                   m6g counts the GROUP, not the line)
B = union of all (8,4,4)-orbits (both slopes) -- the block cover of Theorem 17 / B.19(b).
A (7,5,3,1) orbit Omega_d is CLEAN iff it is disjoint from B and from every other (7,5,3,1) orbit Omega_e
(e != +-d).  "meets" == shares >=1 point of P, computed in O(#points) using dictionaries (see below).

FAST (O(p)) MEETS-GRAPH.  Every point of P corresponds to a residue a in (Z/p)* and a branch (H(1) or
H(-1)); for the H(1) branch at residue a the point's diagonal residue is d0 = a - 1/a (mod p) [this is
exactly a's kappa-membership: a is a kappa class of G_{d0}] and its antidiagonal residue is e0 = a + 1/a
(mod p).  (The H(-1) branch at the same a gives the swapped pair (e0,d0) -- same unordered pair, so it
adds no new information; this is checked directly against brute-force point enumeration.)  So a *witnesses*
that orbit canon(d0) and orbit canon(e0) share a point, where canon(x) = min(x mod p, (-x) mod p).  One
proves canon(d0) != canon(e0) always (for a in 1..p-1), so every 'a' gives a genuine cross-orbit edge; the
union of these p-1 edges over a=1..p-1 is *exactly* the "meets" relation among all canonical orbit indices
-- this is the content of B.19 addendum (c) ("the H(1) class kappa=(a,1/a) of G_d has its points in the -1
group at residue e=a+1/a") turned into an O(p) algorithm.  Building the classification (type_of, via a
sieve of modular inverses + O(1) bucket lookups replacing km1_lines_5678.py's O(p) per-d scan) and this
meets-graph are both O(p) total per prime p.

CORRECTION TO A PARENTHETICAL IN B.19 ADDENDUM (c) (documented in the report; verified two independent
ways below): "4 of 28 pairs of (8,4,4)-orbits and 5 of 45 pairs of (7,5,3,1)-orbits at p=113 share points"
used C(m8,2)=28 and C(m7,2)=45 over the RAW per-slope group counts (m8=8, m7=10 groups) without collapsing
the d<->-d mirror pairs into single orbits; since Omega_d = Omega_{-d} identically, those coincide
trivially (yielding exactly m8/2=4 and m7/2=5 "self" pairs) which is exactly the "4 of 28" / "5 of 45"
reported -- i.e. at p=113 there are in fact ZERO genuine (distinct-orbit) meetings among the four (8,4,4)
orbits or the five (7,5,3,1) orbits; the true clean-orbit picture (this note) uses canonical, deduplicated
orbit indices throughout.

Cross-validated against slack/t221_agents/orbit_cover.py (Task A, independent method) for m8/m7/m6g: exact
match at every prime 11<=p<=500 (see report).

usage: python3 slack/t221_agents/clean_counts.py
"""
import sys, os, time
from collections import defaultdict, Counter

# ----------------------------------------------------------------------------------------------------
# primes
def sieve_primes(n):
    s = bytearray([1]) * (n + 1)
    s[0:2] = b'\x00\x00'
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(2, n + 1) if s[i]]

def is_prime(n):
    if n < 2: return False
    for q in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % q == 0: return n == q
    d = n - 1; r = 0
    while d % 2 == 0: d //= 2; r += 1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(r-1):
            x = x*x % n
            if x == n-1: break
        else:
            return False
    return True

# ----------------------------------------------------------------------------------------------------
# O(p) classification + meets-graph
def sieve_inverses(p):
    inv = [0] * p
    inv[1] = 1
    for a in range(2, p):
        inv[a] = (-(p // a) * inv[p % a]) % p
    return inv

def analyse_prime(p):
    """Returns (type_of, adj, m_counts) where:
       type_of[d] = (ttype, n_classes, m, nk, nl) for d in 0..p-1, ttype in {'m8','m7','m6g','other'}
       adj[c] = set of canonical indices sharing a point with canonical index c
       m_counts = dict with N4,m8,m7,m6g (per-slope GROUP counts, d ranges over 0..p-1)"""
    h = (p - 1) // 2
    inv = sieve_inverses(p)
    def X(u):
        r = u % p
        return r if r <= h else r - p
    def Y(u):
        r = u % p
        return r if r else p
    kappa_by_d = defaultdict(list)
    lambda_by_e = defaultdict(list)
    for a in range(1, p):
        ia = inv[a]
        kappa_by_d[(a - ia) % p].append(a)
        lambda_by_e[(a + ia) % p].append(a)
    type_of = [None] * p
    N4 = m8 = m7 = m6g = 0
    for d in range(p):
        As = kappa_by_d.get(d, ())
        Bs = lambda_by_e.get((-d) % p, ())
        nk, nl = len(As), len(Bs)
        centres = [X(a) - Y(inv[a]) for a in As] + [-(X(b) + Y(inv[b])) for b in Bs]
        n = len(centres)
        if n == 0:
            type_of[d] = ('other', 0, None, nk, nl)
            continue
        cmin = min(centres)
        m = centres.count(cmin)
        if n == 4:
            if m == 4: t = 'm8'; m8 += 1
            elif m in (1, 3): t = 'm7'; m7 += 1
            elif m == 2: t = 'm6g'; m6g += 1
            else: t = 'other'
        else:
            t = 'other'
        if nk == 2 and nl == 2:
            N4 += 1
        type_of[d] = (t, n, m, nk, nl)
    # meets graph (canonical indices)
    def canon(x):
        r = x % p
        return r if r <= p - r else p - r
    adj = defaultdict(set)
    for a in range(1, p):
        ia = inv[a]
        d0 = (a - ia) % p
        e0 = (a + ia) % p
        cd, ce = canon(d0), canon(e0)
        adj[cd].add(ce)
        adj[ce].add(cd)
    return type_of, adj, dict(N4=N4, m8=m8, m7=m7, m6g=m6g)

def orbit_stats(p, type_of, adj):
    """Orbit-level (canonical d = 1..h, excluding the self-paired d=0) clean/dirty classification."""
    h = (p - 1) // 2
    orb_type = {d: type_of[d][0] for d in range(1, h + 1)}
    n8o = sum(1 for t in orb_type.values() if t == 'm8')
    n7o = sum(1 for t in orb_type.values() if t == 'm7')
    n6go = sum(1 for t in orb_type.values() if t == 'm6g')
    clean = dirtyB = dirty7 = dirtyBoth = 0
    I7_pairs = set()
    for d in range(1, h + 1):
        if orb_type[d] != 'm7':
            continue
        neigh = adj.get(d, ())
        meetsB = False; meets7 = False
        for e in neigh:
            te = orb_type.get(e)  # None if e==0 (central orbit, excluded) -- still a legitimate neighbour type via type_of
            if te is None:
                te = type_of[e][0]
            if te == 'm8':
                meetsB = True
                I7_pairs.add((min(d, e), max(d, e)))
            elif te == 'm7':
                meets7 = True
                I7_pairs.add((min(d, e), max(d, e)))
        if not meetsB and not meets7: clean += 1
        elif meetsB and not meets7: dirtyB += 1
        elif meets7 and not meetsB: dirty7 += 1
        else: dirtyBoth += 1
    I7 = len(I7_pairs)
    return dict(n8o=n8o, n7o=n7o, n6go=n6go, clean=clean, dirtyB=dirtyB, dirty7=dirty7,
                dirtyBoth=dirtyBoth, I7=I7)

# ----------------------------------------------------------------------------------------------------
# LP(1) (p <= 300 only), lp1_types.py-style
def lp1_value(p):
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import csr_matrix
    h = (p - 1) // 2
    pts = [(x, y) for x in range(-h, 3*h + 2) for y in range(0, 2*p) if (x*y) % p in (1, p-1)]
    idx = {q: i for i, q in enumerate(pts)}; n = len(pts)
    lines = defaultdict(list)
    for (x, y) in pts:
        lines[('r', y)].append(idx[(x,y)]); lines[('c', x)].append(idx[(x,y)])
        lines[('d', x-y)].append(idx[(x,y)]); lines[('a', x+y)].append(idx[(x,y)])
    L = [mem for key, mem in lines.items() if len(mem) >= 3]
    data = []; ri = []; ci = []
    for r, mem in enumerate(L):
        for j in mem: data.append(1.0); ri.append(r); ci.append(j)
    A = csr_matrix((data, (ri, ci)), shape=(len(L), n))
    res = linprog(-np.ones(n), A_ub=A, b_ub=2*np.ones(len(L)), bounds=[(0,1)]*n, method='highs')
    return -res.fun

# ----------------------------------------------------------------------------------------------------
def main():
    t_start = time.time()
    P_MAIN = [p for p in sieve_primes(3000) if 100 <= p <= 3000]
    P_EXTRA = [5003, 10007, 20011, 50021, 100003]   # sparse extension, all verified prime below
    for q in P_EXTRA:
        assert is_prime(q), q
    LP1_MAX = 300

    rows = []
    lp1_rows = {}
    for p in P_MAIN:
        type_of, adj, mc = analyse_prime(p)
        st = orbit_stats(p, type_of, adj)
        assert mc['m8'] == 2 * st['n8o'], (p, mc, st)   # d=0 is never m8-type (checked)
        assert mc['m7'] == 2 * st['n7o'], (p, mc, st)   # d=0 is never m7-type (checked)
        U = 4*(p-1) - 4*mc['m8'] - 4*st['clean']
        row = dict(p=p, **mc, **st, U=U)
        rows.append(row)
        if p <= LP1_MAX:
            V = lp1_value(p)
            S = 4*(p-1) - V
            lp1_rows[p] = (V, S)

    extra_rows = []
    for p in P_EXTRA:
        type_of, adj, mc = analyse_prime(p)
        st = orbit_stats(p, type_of, adj)
        U = 4*(p-1) - 4*mc['m8'] - 4*st['clean']
        extra_rows.append(dict(p=p, **mc, **st, U=U))

    t_elapsed = time.time() - t_start

    out_path = os.path.join(os.path.dirname(__file__), 'clean_counts_output.txt')
    with open(out_path, 'w') as f:
        def w(s=''): f.write(s + '\n')
        w(f"clean_counts.py output -- T2.21 task B (clean 7-groups), k=-1")
        w(f"primes: 100<=p<=3000, all of them (count={len(P_MAIN)}); plus a sparse extension "
          f"{P_EXTRA}; LP(1) computed for p<={LP1_MAX} only.  total runtime {t_elapsed:.2f}s "
          f"(python3, numpy/scipy linprog method='highs' used only for the LP(1) rows).")
        w("Conventions: N4,m8,m7,m6g are PER-SLOPE GROUP counts (d ranges over 0..p-1, i.e. the same "
          "convention as section 24 / lp1_types.py's B_t / Task A's orbit_cover.py). n7orb=m7/2, "
          "n8orb=m8/2, n6gorb=m6g/2 are the corresponding ORBIT counts (canonical d=1..h; the central "
          "group d=0 is never of type m8 or m7, only ever 'other' or m6g -- verified for every prime "
          "below, so the /2 is exact, no +-1 correction needed). clean/dirtyB/dirty7/dirtyBoth partition "
          "the n7orb 7-orbits by whether they meet B (union of all 8,4,4-orbits) and/or another 7-orbit. "
          "cleangrp = 2*clean (clean SLOPE+1 groups; total clean groups both slopes = 4*clean). "
          "I7 = #unordered canonical-orbit pairs {7-orbit,(7-or-8)-orbit} that share a point. "
          "U = 4(p-1) - 4*m8 - 4*clean  (candidate bound, B.19 point 6 convention: 8 points saved per "
          "8-orbit [4*m8, since m8 counts 2 groups per orbit], 4 points saved per clean 7-orbit). "
          "theta = clean/n7orb (fraction of 7-orbits that are clean).")
        w()
        hdr = ("    p |  N4  m8  m7 m6g | n7orb n8orb n6gorb | clean dirtyB dirty7 dirtyBoth cleangrp I7 |"
               "        U    U/(p-1) |  m8/p   m7/p   N4/p clean/p   I7/p  theta")
        w(hdr); w('-'*len(hdr))
        for row in rows:
            p = row['p']
            n7o = row['n7o'] or 1
            theta = row['clean']/row['n7o'] if row['n7o'] else float('nan')
            line = (f"{p:5d} | {row['N4']:3d} {row['m8']:3d} {row['m7']:3d} {row['m6g']:3d} | "
                    f"{row['n7o']:5d} {row['n8o']:5d} {row['n6go']:6d} | "
                    f"{row['clean']:5d} {row['dirtyB']:6d} {row['dirty7']:6d} {row['dirtyBoth']:9d} "
                    f"{2*row['clean']:8d} {row['I7']:2d} | "
                    f"{row['U']:8d} {row['U']/(p-1):9.4f} | "
                    f"{row['m8']/p:.4f} {row['m7']/p:.4f} {row['N4']/p:.4f} {row['clean']/p:.4f} "
                    f"{row['I7']/p:.4f} {theta:.4f}")
            if p in lp1_rows:
                V, S = lp1_rows[p]
                # both U and V=LP(1) are candidate UPPER BOUNDS on alpha; compare like with like (bound
                # vs bound, and saving vs saving = 4(p-1)-bound).  U's own "saving" is 4*m8+4*clean.
                Su = 4*(p-1) - row['U']
                line += (f"   | LP1={V:.3f} S_LP1={S:.3f} S_LP1/(p-1)={S/(p-1):.4f}  S_U={Su:.3f}  "
                         f"U-LP1(bound gap, U should be >= LP1)={row['U']-V:+.3f}")
            w(line)
        w()
        w(f"-- extension beyond 3000 (sparse sample, no LP(1)) --")
        w(hdr.split('|')[0] + "|  N4  m8  m7 m6g | n7orb n8orb n6gorb | clean dirtyB dirty7 dirtyBoth cleangrp I7 |        U    U/(p-1) |  m8/p   m7/p   N4/p clean/p   I7/p  theta")
        for row in extra_rows:
            p = row['p']
            theta = row['clean']/row['n7o'] if row['n7o'] else float('nan')
            w(f"{p:6d} | {row['N4']:3d} {row['m8']:3d} {row['m7']:3d} {row['m6g']:3d} | "
              f"{row['n7o']:5d} {row['n8o']:5d} {row['n6go']:6d} | "
              f"{row['clean']:5d} {row['dirtyB']:6d} {row['dirty7']:6d} {row['dirtyBoth']:9d} "
              f"{2*row['clean']:8d} {row['I7']:2d} | "
              f"{row['U']:8d} {row['U']/(p-1):9.4f} | "
              f"{row['m8']/p:.4f} {row['m7']/p:.4f} {row['N4']/p:.4f} {row['clean']/p:.4f} "
              f"{row['I7']/p:.4f} {theta:.4f}")
        w()
        # summary bands
        w("-- summary: average densities over successive p-bands --")
        bands = [(100,300),(300,600),(600,1000),(1000,1500),(1500,2000),(2000,2500),(2500,3000)]
        for lo,hi in bands:
            band = [r for r in rows if lo<=r['p']<=hi]
            if not band: continue
            n=len(band)
            avg = lambda key: sum(r[key] for r in band)/n
            avg_ratio = lambda key: sum(r[key]/r['p'] for r in band)/n
            theta_avg = sum(r['clean']/r['n7o'] for r in band if r['n7o'])/sum(1 for r in band if r['n7o'])
            w(f" p in [{lo:5d},{hi:5d}] (n={n:3d}): m8/p={avg_ratio('m8'):.4f} m7/p={avg_ratio('m7'):.4f} "
              f"N4/p={avg_ratio('N4'):.4f} clean/p={avg_ratio('clean'):.4f} I7/p={avg_ratio('I7'):.4f} "
              f"theta={theta_avg:.4f} avg(U/(p-1))={sum(r['U']/(r['p']-1) for r in band)/n:.4f}")
        allband = rows + extra_rows
        theta_all = sum(r['clean']/r['n7o'] for r in allband if r['n7o'])/sum(1 for r in allband if r['n7o'])
        w(f" ALL 100..3000+extension (n={len(allband)}): theta_avg={theta_all:.4f}")
    print(f"wrote {out_path}  ({len(rows)} main rows + {len(extra_rows)} extension rows, "
          f"{len(lp1_rows)} LP(1) rows)  total time {t_elapsed:.2f}s")
    return rows, extra_rows, lp1_rows

if __name__ == "__main__":
    main()
