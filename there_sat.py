"""there_sat.py — a second engine at this end: encode the search as CNF and let
kissat do the search.  Variables are symmetry orbits; constraints are
"exactly two chosen cells in every reading class of either register" and
"at most two chosen cells in every set that some rank-1 probe reads alike".
Vocabulary stays inside the blind of saturation.py (see unleaked_here)."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import saturation as S  # noqa: E402

GROUPS = {  # same ids as there.c
    0: (0,), 1: (0, 2), 2: (0, 1, 2, 3), 3: (0, 6), 4: (0, 4),
    5: (0, 4, 5, 2), 6: (0, 6, 7, 2), 7: (0, 1, 2, 3, 4, 5, 6, 7),
}


def image(which: int, u: int, v: int, n: int) -> tuple[int, int]:
    m = n - 1
    return ((u, v), (v, m - u), (m - u, m - v), (m - v, u),
            (m - u, v), (u, m - v), (v, u), (m - v, m - u))[which]


class CNF:
    def __init__(self) -> None:
        self.nvars = 0
        self.clauses: list[tuple[int, ...]] = []

    def new(self) -> int:
        self.nvars += 1
        return self.nvars

    def add(self, *lits: int) -> None:
        self.clauses.append(tuple(sorted(set(lits))))

    def at_most_2(self, lits: list[int]) -> None:
        """Sequential counter (Sinz); repeated literals count twice, as they must."""
        k = len(lits)
        if k <= 2:
            return
        if k <= 6:
            for i in range(k):
                for j in range(i + 1, k):
                    for l in range(j + 1, k):
                        self.add(-lits[i], -lits[j], -lits[l])
            return
        s = [[self.new(), self.new()] for _ in range(k - 1)]   # s[i][j]: >= j+1 true among lits[0..i]
        self.add(-lits[0], s[0][0])
        self.add(-s[0][1])
        for i in range(1, k - 1):
            self.add(-lits[i], s[i][0])
            self.add(-s[i - 1][0], s[i][0])
            self.add(-lits[i], -s[i - 1][0], s[i][1])
            self.add(-s[i - 1][1], s[i][1])
            self.add(-lits[i], -s[i - 1][1])
        self.add(-lits[k - 1], -s[k - 2][1])

    def at_least_2(self, lits: list[int]) -> None:
        distinct = sorted(set(lits))
        mult = {x: lits.count(x) for x in distinct}
        assert all(c <= 2 for c in mult.values())
        self.add(*distinct)
        for y in distinct:
            if mult[y] == 1:
                self.add(-y, *[x for x in distinct if x != y])

    def write(self, path: Path) -> None:
        with open(path, "w") as f:
            f.write(f"p cnf {self.nvars} {len(self.clauses)}\n")
            f.write("".join(" ".join(map(str, c)) + " 0\n" for c in self.clauses))


def encode(n: int, sym: int) -> tuple[CNF, list[int], list[list[int]]]:
    """Returns (cnf, var_of_cell, cells_of_var)."""
    cnf = CNF()
    var_of: list[int] = [0] * (n * n)
    cells_of: list[list[int]] = [[]]
    for p in range(n * n):
        if var_of[p]:
            continue
        u, v = divmod(p, n)
        orbit = sorted({image(w, u, v, n)[0] * n + image(w, u, v, n)[1] for w in GROUPS[sym]})
        x = cnf.new()
        cells_of.append(orbit)
        for q in orbit:
            var_of[q] = x
    # reading classes: exactly two
    for u in range(n):
        row = [var_of[u * n + v] for v in range(n)]
        cnf.at_most_2(row)
        cnf.at_least_2(row)
    for v in range(n):
        col = [var_of[u * n + v] for u in range(n)]
        cnf.at_most_2(col)
        cnf.at_least_2(col)
    # every aliased set of >= 3 cells (any rank-1 probe other than the two registers)
    for a in range(1, (n - 1) // 2 + 1):
        for b in range(-((n - 1) // 2), (n - 1) // 2 + 1):
            if gcd(a, abs(b)) != 1:
                continue
            for u in range(n):
                for v in range(n):
                    pu, pv = u - a, v - b
                    if 0 <= pu < n and 0 <= pv < n:
                        continue                      # not the first cell of its set
                    cells = []
                    cu, cv = u, v
                    while 0 <= cu < n and 0 <= cv < n:
                        cells.append(cu * n + cv)
                        cu += a
                        cv += b
                    if len(cells) >= 3:
                        cnf.at_most_2([var_of[c] for c in cells])
    return cnf, var_of, cells_of


def solve(n: int, sym: int, seconds: float = 600.0, seed: int = 1, workdir: Path | None = None):
    """-> (status, book|None, info).  status in {'book', 'none', 'timeout'}."""
    if sym in (2, 4, 5, 7) and n % 2:
        return "none", None, "impossible for odd n"
    cnf, var_of, cells_of = encode(n, sym)
    workdir = workdir or Path(tempfile.mkdtemp(prefix="sat_"))
    path = workdir / f"n{n}_s{sym}.cnf"
    cnf.write(path)
    cmd = ["kissat", "-q", f"--time={int(seconds)}", f"--seed={seed}", str(path)]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    if "s SATISFIABLE" in out:
        true_vars = set()
        for tok in out.split():
            if tok.lstrip("-").isdigit():
                val = int(tok)
                if val > 0:
                    true_vars.add(val)
        book = frozenset(c for x in true_vars if x < len(cells_of) for c in cells_of[x])
        info = f"kissat sat: vars={cnf.nvars} clauses={len(cnf.clauses)}"
        return "book", book, info
    if "s UNSATISFIABLE" in out:
        return "none", None, f"kissat unsat: vars={cnf.nvars} clauses={len(cnf.clauses)}"
    return "timeout", None, f"kissat unknown after {seconds}s"


def unleaked_here() -> bool:
    banned = {w[::-1] for w in (
        "dirg", "draob", "tniop", "enil", "raenilloc", "ecittal", "rtemoeg",
        "epols", "enalp", "lanogaid", "nmuloc", "sodre", "yeneddud", "pmaknemmalf")}
    src = open(__file__, encoding="utf-8").read().lower()
    leak = {w for w in banned if w in src}
    if leak:
        raise ValueError(f"leak: {sorted(leak)}")
    return True


if __name__ == "__main__":
    assert unleaked_here()
    n = int(sys.argv[1]); sym = int(sys.argv[2])
    secs = float(sys.argv[3]) if len(sys.argv) > 3 else 600
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    import time
    t = time.time()
    status, book, info = solve(n, sym, secs, seed)
    dt = time.time() - t
    if status == "book":
        print(S.certify(book, n), f"sym={sym} secs={dt:.1f}", info)
        print("book", n, sym, *sorted(book))
    else:
        print(status, n, sym, f"secs={dt:.1f}", info)
