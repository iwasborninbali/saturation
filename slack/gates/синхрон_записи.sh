#!/bin/bash
# синхрон_записи.sh <record_id> <файл>... — сверяет md5 файлов записи Zenodo с локальными.
# Поставлен после случая, когда changelog заявил правки, отсутствовавшие в тексте,
# а запись несла утренний tex. Код: 0 синхрон, 1 расхождение, 2 не знаю.
set -u
ID=$1; shift
J=$(curl -s "https://zenodo.org/api/records/$ID") || { echo "НЕ ЗНАЮ: api"; exit 2; }
bad=0
for f in "$@"; do
  b=$(basename "$f")
  rmd5=$(echo "$J"|python3 -c "
import json,sys
d=json.load(sys.stdin)
for x in d.get('files',[]):
    if x['key']=='$b': print(x['checksum'].replace('md5:',''))" 2>/dev/null)
  lmd5=$(md5 -q "$f" 2>/dev/null)
  if [ -z "$rmd5" ]; then echo "  $b: НЕТ В ЗАПИСИ"; bad=1
  elif [ "$rmd5" = "$lmd5" ]; then echo "  $b: синхрон"
  else echo "  $b: РАСХОЖДЕНИЕ (запись $rmd5, локально $lmd5)"; bad=1; fi
done
exit $bad
