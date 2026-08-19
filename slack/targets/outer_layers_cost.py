"""outer_layers_cost.py — сколько стоит потребовать, чтобы ОБА крайних слоя несли планарный максимум 2n.

Слой трёхмерной конфигурации есть плоская решётка n x n без трёх коллинеарных, поэтому несёт не более
2n точек. Вопрос: совместимо ли достижение этого потолка в обоих крайних слоях с глобальным оптимумом?

Ответ (kissat, профиль навязан по ОДНОЙ оси, то есть сильная форма):
    n=4: оба крайних по 8  -> максимум всего 28 = a(4). Ничего не стоит.
    n=5: оба крайних по 10 -> максимум всего 39 < a(5) = 40. Стоит РОВНО ОДНУ точку.
    n=6: оба крайних по 12 -> максимум всего 64 = a(6). Ничего не стоит.

То есть аномалия при n=5 не в том, что «формула иногда врёт», а в том, что две оптимальные ПЛОСКИЕ
конфигурации, поставленные в крайние плоскости, при n=5 несовместимы с трёхмерным оптимумом — и ровно
на одну точку. При n=4 и n=6 совместимы.

usage: python3 outer_layers_cost.py n M_от M_до
"""
import sys, subprocess, os
sys.path.insert(0,'/Users/iwasborninbali/saturation/slack/targets')
from no3_3d_cnf import lines
from plane4_cnf import CNF

def build(n, M, path, axis=2):
    nc, ln = lines(n)
    F = CNF(nc); x = lambda i: i+1
    for m in ln: F.atmost([x(i) for i in m], 2)
    def layer(t):
        return [x(i) for i in range(nc)
                if (i//(n*n) if axis==0 else (i//n)%n if axis==1 else i%n) == t]
    for t in (0, n-1):                      # оба крайних слоя РОВНО 2n
        c = layer(t)
        F.atmost(c, 2*n)
        F.atmost([-v for v in c], len(c)-2*n)
    F.atleast([x(i) for i in range(nc)], M, 2*n*n+1)
    F.write(path, f"n={n}, outer layers exactly {2*n}, total >= {M}")
    return F

n = int(sys.argv[1])
for M in range(int(sys.argv[2]), int(sys.argv[3])+1):
    build(n, M, '/tmp/o.cnf')
    r = subprocess.run(['kissat','-q','/tmp/o.cnf'], capture_output=True)
    st = {10:'ВЫПОЛНИМО', 20:'невозможно'}.get(r.returncode, f'rc={r.returncode}')
    print(f"  n={n}, оба крайних слоя по {2*n}, всего >= {M}: {st}", flush=True)
    if r.returncode == 20: break
