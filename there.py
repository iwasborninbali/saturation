"""there.py — the other end of saturation.find(n).

saturation.py states the task and verifies; it refuses to search.  This file
searches (there.c does the work) and hands every book back through
saturation.certify before it is allowed to exist in books.json.

    python3 there.py 2 46            # search resolutions 2..46, print certificates
    python3 there.py 47 --secs 3600  # one resolution, longer budget

Symmetry classes (ids as in there.c): 0 none, 1 half turn, 2 quarter turns,
3 swap of registers, 4 flip, 5 both flips, 6 both swaps, 7 all eight,
8 quarter turns off the two long axes + one half-turn pair on the main axis (odd n).
Vocabulary stays inside the blind of saturation.py (see unleaked_here)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import saturation as S  # noqa: E402

BOOKS = HERE / "books.json"
BIN = HERE / "there"
SRC = HERE / "there.c"

# classes to try, easiest first; odd n cannot carry 2, 4, 5, 7 (see there.c)
EVEN_ORDER = (2, 6, 1, 3, 4, 5, 7, 0)
ODD_ORDER = (8, 6, 1, 3, 0)
QUICK = {7: 60, 5: 60, 6: 90, 4: 60}          # sparse classes get a short budget


def build() -> None:
    if not BIN.exists() or BIN.stat().st_mtime < SRC.stat().st_mtime:
        subprocess.run(["cc", "-O3", "-march=native", "-o", str(BIN), str(SRC)], check=True)


def load() -> dict:
    return json.loads(BOOKS.read_text()) if BOOKS.exists() else {}


def save(db: dict) -> None:
    tmp = BOOKS.with_suffix(".tmp")
    tmp.write_text(json.dumps(db, indent=0, sort_keys=True))
    tmp.replace(BOOKS)


def run_one(n: int, sym: int, seed: int, secs: float) -> dict:
    cmd = [str(BIN), str(n), str(sym), str(seed), str(secs)]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
    res = {"n": n, "sym": sym, "seed": seed, "raw": out.split(" :")[0]}
    if out.startswith("book"):
        head, _, tail = out.partition(" :")
        res["status"] = "book"
        res["book"] = sorted(int(x) for x in tail.split())
        for kv in head.split():
            if "=" in kv:
                k, v = kv.split("=")
                res[k] = v
    elif out.startswith("none"):
        res["status"] = "none"
    elif out.startswith("skip"):
        res["status"] = "skip"
    else:
        res["status"] = "timeout"
    return res


def search(n: int, secs: float, seeds: int = 8, syms=None, log=print) -> dict | None:
    """Try classes in order; per class, `seeds` parallel seeds; first book wins."""
    build()
    order = syms or (EVEN_ORDER if n % 2 == 0 else ODD_ORDER)
    for sym in order:
        if sym in (2, 4, 5, 7) and n % 2:
            continue
        if sym == 8 and n % 2 == 0:
            continue
        t = time.time()
        budget = min(secs, QUICK.get(sym, secs))
        with ThreadPoolExecutor(max_workers=seeds) as ex:
            futs = [ex.submit(run_one, n, sym, s, budget) for s in range(1, seeds + 1)]
            found, nones = None, 0
            for f in as_completed(futs):
                if f.cancelled():
                    continue
                r = f.result()
                if r["status"] == "book" and found is None:
                    found = r
                    for g in futs:
                        g.cancel()
                    subprocess.run(["pkill", "-f", f"{BIN} {n} {sym} "], capture_output=True)
                elif r["status"] == "none":
                    nones += 1
        if found:
            book = frozenset(found["book"])
            claim = S.certify(book, n)                    # raises if not saturated
            found["certificate"] = repr(claim)
            found["engine"] = "there.c"
            log(f"{claim}  sym={sym} seed={found['seed']} nodes={found.get('nodes')} secs={found.get('secs')}")
            return found
        log(f"n={n} sym={sym}: {'no book in this class (exhausted)' if nones else 'not found'} "
            f"in {time.time() - t:.0f}s")
    return None


def find(n: int, secs: float = 600.0, seeds: int = 8) -> S.Book:
    """saturation.find, implemented at this end: cached if known, searched if not."""
    db = load()
    if str(n) in db:
        return S.saturated(frozenset(db[str(n)]["book"]), n)
    res = search(n, secs, seeds)
    if res is None:
        raise NotImplementedError(f"n={n}: not found within {secs}s per class at this end")
    db = load()
    db[str(n)] = res
    save(db)
    return frozenset(res["book"])


def unleaked_here() -> bool:
    banned = {w[::-1] for w in (
        "dirg", "draob", "tniop", "enil", "raenilloc", "ecittal", "rtemoeg",
        "epols", "enalp", "lanogaid", "nmuloc", "sodre", "yeneddud", "pmaknemmalf")}
    for f in (__file__, SRC, HERE / "there_sat.py"):
        src = open(f, encoding="utf-8").read().lower()
        leak = {w for w in banned if w in src}
        if leak:
            raise ValueError(f"leak in {f}: {sorted(leak)}")
    return True


if __name__ == "__main__":
    assert unleaked_here()
    secs, seeds, args, skip = 600.0, 8, [], False
    for i, a in enumerate(sys.argv[1:], 1):
        if skip:
            skip = False
            continue
        if a == "--secs":
            secs, skip = float(sys.argv[i + 1]), True
        elif a == "--seeds":
            seeds, skip = int(sys.argv[i + 1]), True
        elif not a.startswith("--"):
            args.append(a)
    lo = int(args[0]); hi = int(args[1]) if len(args) > 1 else lo
    for n in range(lo, hi + 1):
        db = load()
        if str(n) in db:
            print(S.certify(frozenset(db[str(n)]["book"]), n), f"(cached; sym={db[str(n)]['sym']})")
            continue
        try:
            find(n, secs, seeds)
        except NotImplementedError as e:
            print("open:", e)
