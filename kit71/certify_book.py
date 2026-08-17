"""certify_book.py — one door for a proposed book: saturation.certify (v1, this repo), exact class
via web/stab.py, encoding for the database, and an append-only record in kit71/results/books_family.json.

    python3 kit71/certify_book.py N "t1 t2 ..." "provenance text"
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "web"))
import saturation as S  # noqa: E402
import stab  # noqa: E402

DB = os.path.join(HERE, "results", "books_family.json")


def main() -> None:
    n = int(sys.argv[1])
    toks = frozenset(int(x) for x in sys.argv[2].replace(",", " ").split())
    prov = sys.argv[3] if len(sys.argv) > 3 else ""
    claim = S.certify(toks, n)                       # raises unless saturated
    cls = stab.classify(toks, n)
    enc = stab.encode(toks, n)
    st = stab.stabilizer(toks, n)
    rec = {"n": n, "class": cls, "stabilizer": st, "encoded": enc, "tokens": sorted(toks),
           "certificate": repr(claim), "provenance": prov}
    db = json.load(open(DB)) if os.path.exists(DB) else []
    if not any(d["n"] == n and d["encoded"] == enc for d in db):
        db.append(rec)
        os.makedirs(os.path.dirname(DB), exist_ok=True)
        json.dump(db, open(DB, "w"), indent=0)
        fresh = True
    else:
        fresh = False
    print(claim)
    print(f"class={cls} stabilizer={st} fresh={fresh}")
    print("encoded:", enc)


if __name__ == "__main__":
    main()
