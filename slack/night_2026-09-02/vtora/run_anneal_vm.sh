#!/bin/zsh
# run_anneal_vm.sh — запуск темперинга T-модели в кубе на ВМ saturation-alg-1: n=7, m=74, S сидов в фоне (по одному ядру на сид).
# usage: zsh run_anneal_vm.sh start S sweeps | status | fetch
export CLOUDSDK_CORE_ACCOUNT=saturation-agent@loyobondar-prod.iam.gserviceaccount.com CLOUDSDK_CORE_PROJECT=loyobondar-prod
VM=saturation-alg-1; Z=us-east4-b; HERE=/Users/iwasborninbali/saturation/slack/night_2026-09-02/vtora
case "$1" in
  start)
    S=${2:-16}; SW=${3:-20000}
    gcloud compute scp --zone $Z --quiet $HERE/cube_anneal.py $VM:~/cube_anneal.py
    gcloud compute ssh $VM --zone $Z --quiet --command "mkdir -p ~/anneal && cd ~/anneal && for s in \$(seq 1 $S); do nohup python3 ~/cube_anneal.py 7 74 $SW 200 \$s anneal_n7_m74_s\$s > anneal_n7_m74_s\$s.log 2>&1 & done; sleep 2; ps aux | grep -c '[c]ube_anneal'"
    ;;
  status)
    gcloud compute ssh $VM --zone $Z --quiet --command "cd ~/anneal 2>/dev/null && ls *_T0.txt 2>/dev/null; for f in anneal_n7_m74_s*.log; do echo \"\$f: \$(tail -1 \$f | cut -c1-110)\"; done; uptime"
    ;;
  fetch)
    mkdir -p $HERE/anneal_vm && gcloud compute scp --zone $Z --quiet --recurse "$VM:~/anneal/*" $HERE/anneal_vm/ && ls $HERE/anneal_vm | head -40
    ;;
esac
