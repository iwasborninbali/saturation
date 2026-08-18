"""mixed3.py — smallest 'mixed' orbit defects, one representative per D4-orbit (cell sets):
  --c4v2 : C4 base + one dia2-orbit {(a,b),(m-a,m-b),(b,a),(m-b,m-a)} (a,b off the diagonals and off the central cross,
           i.e. an orbit that is dia2- but not C4-invariant), plus one diagonal loop (d,d) or (d,m-d) when n is odd
           (parity: 2n = 4k + 4 + 2 needs n odd; for even n no loop).                                  [sweep with there_tw sym 9]
  --v2c4 : dia2 base + one C4-orbit {(a,b),(b,m-a),(m-a,m-b),(m-b,a)} that is not dia2-invariant.  [sweep with there_tw sym 10]
Prints PAIRS strings (each half-turn pair as one point).   python3 bench/mixed3.py N --c4v2|--v2c4
"""
import sys
sys.path.insert(0, 'bench')
from defects3 import canon, pair_cells

def main():
    n = int(sys.argv[1]); m = n - 1; h = m // 2; mode = sys.argv[2]
    seen = set(); out = []
    for a in range(n):
        for b in range(n):
            if a == b or a + b == m: continue                 # off the long diagonals
            if (n & 1) and (a == h or b == h): continue       # central cross: simultaneously C4- and dia2-invariant
            if mode == "--c4v2":
                orbit_pairs = [(a, b), (b, a)]                # dia2-orbit as two half-turn pairs
                cells0 = pair_cells(a, b, n) | pair_cells(b, a, n)
                if len(cells0) != 4: continue
                # is it C4-invariant? (then it is a base orbit, not a defect)
                if {(v, m - u) for (u, v) in cells0} == cells0: continue
                if n & 1:
                    for d in range(h):
                        for loop in ((d, d), (d, m - d)):
                            cells = cells0 | pair_cells(*loop, n)
                            if len(cells) != 6: continue
                            key = canon(cells, n)
                            if key in seen: continue
                            seen.add(key); out.append(orbit_pairs + [loop])
                else:
                    key = canon(cells0, n)
                    if key in seen: continue
                    seen.add(key); out.append(orbit_pairs)
            else:
                orbit_pairs = [(a, b), (b, m - a)]            # C4-orbit as two half-turn pairs
                cells0 = pair_cells(a, b, n) | pair_cells(b, m - a, n)
                if len(cells0) != 4: continue
                if {(v, u) for (u, v) in cells0} == cells0: continue   # dia2-invariant: base orbit
                key = canon(cells0, n)
                if key in seen: continue
                seen.add(key); out.append(orbit_pairs)
    for ps in out:
        print(";".join(f"{a},{b}" for a, b in ps))
    print(f"# n={n} {mode}: {len(out)} sub-classes mod D4", file=sys.stderr)

if __name__ == "__main__":
    main()
