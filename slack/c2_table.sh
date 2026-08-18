#!/bin/bash
# C2 (first solver, unattended): chain_walk.py over k for p=101 (all k), 199 (all k), 401 (representative k by order); table + auto-commit
cd "$(dirname "$0")/.."
out=slack/verification/c2_table.txt
echo "# $(date -u +%FT%TZ) C2: p k ord(k) G8 forcedLP_saving total_saving net_per_group  (from slack/chain_walk.py)" > $out
run() { p=$1; k=$2; r=$(timeout 1800 python3 slack/chain_walk.py $p $k 2>/dev/null); o=$(echo "$r" | grep -o "ord(k)=[0-9]*" | head -1 | cut -d= -f2); g=$(echo "$r" | grep -o "G8=[0-9]*" | head -1 | cut -d= -f2); f=$(echo "$r" | grep -o "forced lines: [0-9.]* = 4(p-1) - [-0-9.]*" | grep -o "\- [-0-9.]*$" | cut -c3-); t=$(echo "$r" | grep -o "total cover = [0-9.]* = 4(p-1) - [-0-9.]*" | grep -o "\- [-0-9.]*$" | cut -c3-); n=$(echo "$r" | grep -o "net per 8-group [-0-9.]*" | grep -o "[-0-9.]*$"); echo "$p $k $o $g $f $t $n" >> $out; }
for k in $(seq 2 100); do run 101 $k; done
git pull -q --rebase --autostash origin main; git add $out; git -c user.name="solver-kit71 (Claude, linux-12c)" -c user.email="claude@nusadua.dev" commit -q -m "C2: chain_walk table p=101 all k (auto)" && git push -q origin main
for k in $(seq 2 198); do run 199 $k; done
git pull -q --rebase --autostash origin main; git add $out; git -c user.name="solver-kit71 (Claude, linux-12c)" -c user.email="claude@nusadua.dev" commit -q -m "C2: chain_walk table p=199 all k (auto)" && git push -q origin main
for k in 2 3 5 6 7 10 11 13 400 399 398 397 396 395 20 21 24 25 29 40 50 100 101 200 201 300 349 350 360 380; do run 401 $k; done
echo "# done $(date -u +%FT%TZ)" >> $out
git pull -q --rebase --autostash origin main; git add $out; git -c user.name="solver-kit71 (Claude, linux-12c)" -c user.email="claude@nusadua.dev" commit -q -m "C2: chain_walk table p=401 representative k (auto, done)" && git push -q origin main
