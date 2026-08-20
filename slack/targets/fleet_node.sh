#!/bin/bash
# fleet_node.sh — развёртывание счёта на одной машине флота.
#   fleet_node.sh <индекс машины> <всего машин>
# Доля берётся из fleet.py: кусок i достаётся машине i mod N. Пересечься нельзя по построению.
set -u
I="$1"; NCNT="$2"
cd ~/sat
export SOS_WORK=/tmp/fw SOS_REPO=$HOME/sat
mkdir -p $SOS_WORK
: > /tmp/facts_vm.txt

python3 - "$I" "$NCNT" <<'PY'
import subprocess, sys, os, time
from itertools import combinations
N,CAP,M=7,3,19
SUBS=[s for k in range(CAP+1) for s in combinations(range(N),k)]
W=os.environ["SOS_WORK"]
sys.path.insert(0, os.path.expanduser("~/sat/gates"))
from fleet import shard
def units(col,sub):
    x,y=col//N,col%N
    return [((x*N+y)*N+z)+1 if z in sub else -(((x*N+y)*N+z)+1) for z in range(N)]
def extend(src,dst,col,sub):
    raw=open(src,"rb").read(); i=raw.index(b"p cnf"); nl=raw.index(b"\n",i)
    h=raw[i:nl].split(); body=raw[nl+1:]
    u=units(col,sub)
    head=b"p cnf %s %d\n"%(h[2],int(h[3])+len(u)); tail=b"".join(b"%d 0\n"%v for v in u)
    open(dst,"wb").write(head+body+tail)
    assert os.path.getsize(dst)==len(head)+len(body)+len(tail), f"ОБОРВАН {dst}"
mine = shard(int(sys.argv[1]), int(sys.argv[2]))
print(f"доля машины {sys.argv[1]} из {sys.argv[2]}: {len(mine)} кусков", flush=True)
base=f"{W}/base.cnf"
t0=time.time()
subprocess.run([sys.executable,"plane4_cnf.py","7","19",base,"--sym"],capture_output=True,check=True)
print(f"база за {time.time()-t0:.0f}с", flush=True)
extend(base,f"{W}/c0.cnf",0,SUBS[0]); extend(f"{W}/c0.cnf",f"{W}/s000.cnf",1,SUBS[0])
os.remove(base); os.remove(f"{W}/c0.cnf")
# кэш родителей: узлов всего шесть, детей у каждого много
par={}
for nd,j in mine:
    k=int(nd.rsplit("_s",1)[1])
    if nd not in par:
        p=f"{W}/{nd}.cnf"; extend(f"{W}/s000.cnf", p, 2, SUBS[k]); par[nd]=p
    extend(par[nd], f"{W}/{nd}_s{j:03d}.cnf", 3, SUBS[j])
for p in par.values(): os.remove(p)
os.remove(f"{W}/s000.cnf")
print(f"порождено кусков: {len(mine)}", flush=True)
PY

P=$(( $(nproc) - 1 )); [ "$P" -lt 1 ] && P=1
setsid nohup bash -c "ls $SOS_WORK/case_*_s???.cnf | xargs -P $P -I{} $HOME/sat/sos_second.sh {} 4 120 49 /tmp/facts_vm.txt 7" > /tmp/sos_vm.log 2>&1 < /dev/null &
sleep 5
echo "запущено: параллелизм $P, kissat $(pgrep -c kissat || echo 0)"
