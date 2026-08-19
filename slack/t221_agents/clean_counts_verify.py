"""clean_counts_verify.py -- independent brute-force check of clean_counts.py's clean/dirty classification.
For a handful of primes, builds the ACTUAL point set P, the ACTUAL point set of every (7,5,3,1)- and
(8,4,4)-orbit by direct filtering (diag/antidiag residue membership, no shortcuts), and checks ALL pairs
of those orbits for point-set intersection directly (brute force, O(#orbits^2 * |orbit|)) -- completely
independent of clean_counts.py's O(p) meets-graph (which uses the a -> (a-1/a, a+1/a) witness argument).
Also recomputes the type of every group from scratch by literal line-size counting on the point set (not
the class-data shortcut), so this file shares NO code path with clean_counts.py except python's stdlib.
usage: python3 slack/t221_agents/clean_counts_verify.py [p1 p2 ...]
"""
import sys, os
from collections import defaultdict, Counter

def build(p):
    h = (p - 1) // 2
    pts = [(x, y) for x in range(-h, 3*h + 2) for y in range(0, 2*p) if (x*y) % p in (1, p-1)]
    return pts

def group_types_by_enumeration(p, pts):
    """Type of every slope+1 residue group, purely by counting integer-line sizes within the point set
    (independent implementation from clean_counts.analyse_prime, which uses class-data formulas)."""
    grp = defaultdict(list)
    for (x, y) in pts:
        grp[(x - y) % p].append((x, y))
    type_of = {}
    for d, mem in grp.items():
        cs = Counter(x - y for (x, y) in mem)
        prof = tuple(sorted(cs.values(), reverse=True))
        type_of[d] = prof
    return type_of

def classify_profile(prof):
    if prof == (8, 4, 4): return 'm8'
    if prof == (7, 5, 3, 1): return 'm7'
    if prof == (6, 6, 2, 2): return 'm6g'
    return 'other'

def orbit_point_set(p, d, pts):
    dd = d % p
    out = set()
    for (x, y) in pts:
        diag = (x - y) % p; anti = (x + y) % p
        if diag in (dd, (-dd) % p) or anti in (dd, (-dd) % p):
            out.add((x, y))
    return out

def verify(p):
    pts = build(p)
    type_of = group_types_by_enumeration(p, pts)
    h = (p - 1) // 2
    def canon(v):
        r = v % p
        return r if r <= p - r else p - r
    orb_type = {}
    for d in range(1, h + 1):
        t1 = classify_profile(type_of.get(d, ()))
        t2 = classify_profile(type_of.get((-d) % p, ()))
        assert t1 == t2, (p, d, t1, t2, "d and -d type mismatch!")
        orb_type[d] = t1
    sevens = [d for d in range(1, h+1) if orb_type[d] == 'm7']
    eights = [d for d in range(1, h+1) if orb_type[d] == 'm8']
    orb_pts = {d: orbit_point_set(p, d, pts) for d in sevens + eights}
    for d in sevens + eights:
        assert len(orb_pts[d]) == 64, (p, d, len(orb_pts[d]))
    clean = dirtyB = dirty7 = dirtyBoth = 0
    detail = {}
    for d in sevens:
        meetsB = any(orb_pts[d] & orb_pts[e] for e in eights)
        meets7 = any((orb_pts[d] & orb_pts[e]) for e in sevens if e != d)
        detail[d] = (meetsB, meets7)
        if not meetsB and not meets7: clean += 1
        elif meetsB and not meets7: dirtyB += 1
        elif meets7 and not meetsB: dirty7 += 1
        else: dirtyBoth += 1
    return dict(n7=len(sevens), n8=len(eights), clean=clean, dirtyB=dirtyB, dirty7=dirty7,
                dirtyBoth=dirtyBoth), detail

if __name__ == "__main__":
    test_primes = [int(a) for a in sys.argv[1:]] or [101, 113, 127, 137, 199, 251, 283, 307, 401]
    sys.path.insert(0, os.path.dirname(__file__))
    from clean_counts import analyse_prime, orbit_stats
    all_ok = True
    for p in test_primes:
        brute, detail = verify(p)
        type_of, adj, mc = analyse_prime(p)
        fast = orbit_stats(p, type_of, adj)
        keys = ['clean', 'dirtyB', 'dirty7', 'dirtyBoth']
        ok = all(brute[k] == fast[{'clean':'clean','dirtyB':'dirtyB','dirty7':'dirty7','dirtyBoth':'dirtyBoth'}[k]] for k in keys) \
             and brute['n7'] == fast['n7o'] and brute['n8'] == fast['n8o']
        all_ok &= ok
        print(f"p={p:4d}  brute(n7={brute['n7']},n8={brute['n8']},clean={brute['clean']},dirtyB={brute['dirtyB']},"
              f"dirty7={brute['dirty7']},dirtyBoth={brute['dirtyBoth']})  "
              f"fast(n7={fast['n7o']},n8={fast['n8o']},clean={fast['clean']},dirtyB={fast['dirtyB']},"
              f"dirty7={fast['dirty7']},dirtyBoth={fast['dirtyBoth']})  MATCH={ok}")
        assert ok, f"MISMATCH at p={p}"
    print("ALL BRUTE-FORCE CROSS-CHECKS PASSED" if all_ok else "FAILURES ABOVE")
