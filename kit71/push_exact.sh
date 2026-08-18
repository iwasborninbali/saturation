#!/bin/bash
# unattended: when the CP-SAT journals for alpha(23)/alpha(29), k=-1, contain a RESULT line, commit and push them (once each)
cd "$(dirname "$0")/.."
done23=0; done29=0
while [ $done23 -eq 0 ] || [ $done29 -eq 0 ]; do
  for p in 23 29; do
    f=slack/verification/exact_p${p}_km1_cpsat.txt
    v="done$p"
    if [ "${!v}" -eq 0 ] && grep -q "^RESULT" $f 2>/dev/null; then
      git pull -q --rebase --autostash origin main
      line=$(grep "^RESULT" $f | sed 's/witness.*//' | cut -c1-200)
      printf '\n## [auto] первый солвер: α(%s), k=−1 — итог CP-SAT (6 потоков, %s ч): %s (журнал %s)\n' "$p" "$([ $p -eq 23 ] && echo 12 || echo 6)" "$line" "$f" >> docs/THREAD.md
      git add $f docs/THREAD.md; git -c user.name="solver-kit71 (Claude, linux-12c)" -c user.email="claude@nusadua.dev" commit -q -m "exact alpha(p=$p, k=-1) CP-SAT result (auto-commit)" && git push -q origin main
      eval "$v=1"
    fi
  done
  sleep 300
done
