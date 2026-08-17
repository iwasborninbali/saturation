"""H1b: pure hyperbolas (x+s)(y+t) = k mod q inside the 71-box: which are lawful and largest,
without any repair? Scan all k for primes q in [37, 97], shifts s=t=0; then shifts for top q."""
import sys
from solve import conic_points, triples_through, record, to_book
from saturation import TARGET
N = TARGET
def primes(lo, hi):
    return [p for p in range(lo, hi + 1) if all(p % d for d in range(2, int(p ** .5) + 1))]
def lawful(pts):
    lst = list(pts)
    return all(triples_through(p, lst) == 0 for p in lst)
best = []
for q in primes(37, 97):
    for k in range(1, q):
        raw = conic_points(N, q, 0, 1, 0, 0, 0, -k)
        if len(raw) < 80:
            continue
        if lawful(raw):
            best.append((len(raw), q, k, 0, 0))
            print(f"lawful hyperbola xy={k} mod {q}: size {len(raw)}", flush=True)
best.sort(reverse=True)
print("top pure:", best[:8])
# shifts for the top 3 primes
seen_q = []
for size, q, k, _, _ in best:
    if q in seen_q: continue
    seen_q.append(q)
    if len(seen_q) > 3: break
    for s in range(q):
        for t in range(0, q):
            for kk in range(1, q):
                raw = set((x, y) for x in range(N) for y in range(N) if ((x + s) * (y + t)) % q == kk % q)
                if len(raw) <= best[0][0]:
                    continue
                if lawful(raw):
                    best.append((len(raw), q, kk, s, t))
                    print(f"lawful shifted (x+{s})(y+{t})={kk} mod {q}: size {len(raw)}", flush=True)
best.sort(reverse=True)
print("TOP:", best[:5])
size, q, k, s, t = best[0]
raw = set((x, y) for x in range(N) for y in range(N) if ((x + s) * (y + t)) % q == k % q)
record(to_book(raw, N), N, principle=f"pure hyperbola (x+{s})(y+{t})={k} mod {q} in box 71", note="no repair, no fill")
