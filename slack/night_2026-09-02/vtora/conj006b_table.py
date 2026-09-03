#!/usr/bin/env python3
"""conj006b_table.py — таблица «жёсткость против |S| − a(n)» по стратным свидетелям A280537 из verify_p.log (монитор watch_strata_p.sh).
a(n) берётся как максимум по стратам при данном n (или из argv: n=a,…). Печатает по каждому n: размеры → (жёстких / нежёстких / немаксимальных).
usage: python3 conj006b_table.py [n=a …]"""
import sys, re, collections
known = {}
for a in sys.argv[1:]:
    n, v = a.split('='); known[int(n)] = int(v)
rows = collections.defaultdict(lambda: collections.Counter())
for l in open(__file__.rsplit('/', 1)[0] + '/verify_p.log', encoding='utf-8'):
    m = re.match(r'n(\d+)_c\d+_ord\d+_(\d+)\.txt .*\| n=\d+ m=(\d+) min κ³=(\S+) (ЖЁСТКО|НЕЖЁСТКО|НЕ МАКСИМАЛЬНА)', l)
    if not m: continue
    n, size, st = int(m.group(1)), int(m.group(3)), m.group(5)
    if 'ЧИСТ' not in l and 'ОТКАЗ' not in l: continue
    rows[n][(size, st)] += 1
for n in sorted(rows):
    a = known.get(n, max(s for s, _ in rows[n]))
    print(f"n={n} (a(n) принято {a}):")
    for size in sorted({s for s, _ in rows[n]}, reverse=True):
        c = rows[n]
        print(f"  |S|={size:>3} (a−{a-size}): жёстких {c[(size,'ЖЁСТКО')]}, нежёстких {c[(size,'НЕЖЁСТКО')]}, немаксимальных {c[(size,'НЕ МАКСИМАЛЬНА')]}")
