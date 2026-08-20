#!/bin/bash
# sweep_cleanup.sh — снос рабочих каталогов, чей процесс не жив.
#
# Уборка, стоящая в КОНЦЕ процесса, не выполняется у убитого процесса, а убиваем мы их постоянно.
# У меня так накопилось 149 ГБ в каталогах рекурсии, и диск переполнился; переполнение проявилось
# не как ошибка счёта, а как ИСЧЕЗНОВЕНИЕ ВЫВОДА — ENOSPC при записи stdout, — то есть кончающийся
# диск сначала ломает наблюдение и только потом работу.
# Поэтому уборка делается по ВЛАДЕЛЬЦУ и снаружи, а не изнутри рабочего.
SP=/tmp/claude-1000/-home-pmbot-projects-solver-kit/df30d6f4-57eb-4267-abb8-3e2d3cd04a69/scratchpad
alive=$(ps -eo comm --no-headers | awk '/solve_or_spl|work_parent_f|work_unit_fi/ {n++} END{print n+0}')
freed=0
for d in $SP/sos $SP/wu $SP/wp $SP/w3 $SP/w4 $SP/chain $SP/deep /dev/shm/wp_first /dev/shm/wu_first; do
  [ -d "$d" ] || continue
  if [ "$alive" -eq 0 ]; then
    s=$(du -sm "$d" 2>/dev/null | cut -f1); rm -rf "$d" && freed=$((freed + ${s:-0}))
  fi
done
echo "живых рабочих: $alive; освобождено: ${freed}МБ; свободно на /tmp: $(df -BG /tmp|tail -1|awk '{print $4}')"
[ "$alive" -gt 0 ] && echo "  каталоги НЕ тронуты: есть живые рабочие, снос сломал бы идущий счёт"
