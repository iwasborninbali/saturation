"""mixed_family.py — smallest mixed perturbations of rct4 / dia2 (balance lemma), unique modulo D4.
  --c4v2 : C4 base + one V2 orbit {(a,b),(m-a,m-b),(b,a),(m-b,m-a)} + one diagonal loop (d,d) or (d,m-d)   [use with sym 9]
  --v2c4 : V2 base + one C4 orbit {(a,b),(m-a,m-b),(b,m-a),(m-b,a)}                                       [use with sym 10]
    python3 kit71/bench/mixed_family.py N --c4v2 > list.txt
"""
import sys
from cycle_family import canon, pair_cells

def main():
    n = int(sys.argv[1]); m = n - 1; h = m // 2
    mode = sys.argv[2]
    seen = set(); out = []
    for a in range(n):
        for b in range(n):
            if a == h or b == h or a == b or a + b == m:
                continue
            if mode == "--c4v2":
                base_pairs = [(a, b), (b, a)]
                cells0 = pair_cells(a, b, n) | pair_cells(b, a, n)
                if len(cells0) != 4:
                    continue
                for d in range(h):
                    for anti in (0, 1):
                        loop = (d, m - d) if anti else (d, d)
                        cells = cells0 | pair_cells(*loop, n)
                        if len(cells) != 6:
                            continue
                        key = canon(cells, n)
                        if key in seen:
                            continue
                        seen.add(key)
                        out.append(";".join(f"{x},{y}" for x, y in base_pairs + [loop]))
            else:
                base_pairs = [(a, b), (b, m - a)]
                cells = pair_cells(a, b, n) | pair_cells(b, m - a, n)
                if len(cells) != 4:
                    continue
                key = canon(cells, n)
                if key in seen:
                    continue
                seen.add(key)
                out.append(";".join(f"{x},{y}" for x, y in base_pairs))
    for s in out:
        print(s)
    print(f"# n={n} {mode} unique: {len(out)}", file=sys.stderr)

if __name__ == "__main__":
    main()
