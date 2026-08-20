/* no4_fast.c — исчерпывающий перебор конфигураций без четырёх компланарных, с точным профилем
 * слоёв по двум осям. Инкрементальная блокировка вместо перебора троек на каждого кандидата.
 *
 * ИДЕЯ УСКОРЕНИЯ. Прежняя версия для каждого кандидата пробегала все тройки уже выбранных —
 * O(|S|^3) на кандидата, то есть миллионы операций на узел. Здесь состояние поддерживается
 * инкрементально: при добавлении точки p для каждой ПАРЫ (a,b) уже выбранных строится плоскость
 * через a, b, p, и все узлы решётки на ней получают +1 к счётчику запрета; при откате -1.
 * Отдельный счётчик — для прямых: если q коллинеарна с двумя выбранными, её брать нельзя вовсе,
 * потому что три коллинеарные точки делают компланарной ЛЮБУЮ четвёртую. Проверка кандидата
 * становится O(1): оба счётчика должны быть нулевыми.
 *
 * Второе, решающее: блокировать нужно только узлы с индексом БОЛЬШЕ добавляемого. Перебор идёт
 * по возрастанию индекса, поэтому меньшие уже никогда не будут спрошены. Без этого ускорение
 * не окупалось вовсе — первая версия оказалась медленнее той, которую заменяла (302 с против 240
 * на сверке при n=4), потому что блокировка всей решётки на каждом спуске съедала выигрыш.
 *
 * ПОЛНОТА РАЗБИЕНИЯ по парам профилей проверена не рассуждением, а числом: сумма конфигураций
 * по всем 100 парам при n=4, M=10 равна 10960 — столько же, сколько даёт свободный перебор.
 *
 *   cc -O3 -o no4_fast no4_fast.c && ./no4_fast n M "p0,.." "p1,.."
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int n, NC, M;
static int px[512], py[512], pz[512];
static int S[64], sz;
static int blocked[512], linbl[512], inS[512];
static long long found = 0, nodes = 0;
static int lay0[16], lay1[16], lay2[16], P0[16], P1[16], P2[16];

/* блокировка/разблокировка при добавлении p к текущему S (S ещё БЕЗ p) */
static void touch(int p, int d)
{
    for (int i = 0; i < sz; i++) {                     /* прямые через a и p */
        int a = S[i];
        int ux = px[p]-px[a], uy = py[p]-py[a], uz = pz[p]-pz[a];
        for (int q = p+1; q < NC; q++) {      /* только q > p: меньшие индексы больше не спрашиваются */
            int vx = px[q]-px[a], vy = py[q]-py[a], vz = pz[q]-pz[a];
            if (uy*vz-uz*vy == 0 && uz*vx-ux*vz == 0 && ux*vy-uy*vx == 0) linbl[q] += d;
        }
    }
    for (int i = 0; i < sz; i++) {                     /* плоскости через a, b и p */
        int a = S[i];
        int ux = px[p]-px[a], uy = py[p]-py[a], uz = pz[p]-pz[a];
        for (int j = i+1; j < sz; j++) {
            int b = S[j];
            int wx = px[b]-px[a], wy = py[b]-py[a], wz = pz[b]-pz[a];
            int nx = uy*wz-uz*wy, ny = uz*wx-ux*wz, nz = ux*wy-uy*wx;
            if (nx == 0 && ny == 0 && nz == 0) continue;      /* a,b,p коллинеарны — не бывает */
            int rhs = nx*px[a] + ny*py[a] + nz*pz[a];
            for (int q = p+1; q < NC; q++) {
                if (nx*px[q] + ny*py[q] + nz*pz[q] == rhs) blocked[q] += d;
            }
        }
    }
}

static void rec(int start)
{
    nodes++;
    if (sz == M) {
        found++;
        printf("НАЙДЕНО:");
        for (int i = 0; i < sz; i++) printf(" %d,%d,%d", px[S[i]], py[S[i]], pz[S[i]]);
        printf("\n"); fflush(stdout);
        return;
    }
    if (sz + (NC - start) < M) return;
    /* ВЕРХНЯЯ ОЦЕНКА ОСТАТКА. Считаем реально доступные клетки (не запрещённые плоскостями и
       прямыми, не переполняющие профили) и урезаем их по остатку профиля каждого x-слоя: больше,
       чем P0[x]-lay0[x], из слоя x всё равно не взять. Без этой оценки перебор при n=6 уходил в
       часы на кусок — почти всё время тратилось на ветви, где недобор был предрешён.
       Оценка берётся по КАЖДОЙ из трёх осей и минимизируется: три независимых верхних границы
       на остаток, и годится наименьшая. */
    {
        int a0[16], a1[16], a2[16];
        for (int k = 0; k < n; k++) { a0[k] = a1[k] = a2[k] = 0; }
        for (int q = start; q < NC; q++) {
            if (blocked[q] || linbl[q]) continue;
            if (lay0[px[q]] >= P0[px[q]] || lay1[py[q]] >= P1[py[q]] || lay2[pz[q]] >= P2[pz[q]]) continue;
            a0[px[q]]++; a1[py[q]]++; a2[pz[q]]++;
        }
        int b0 = 0, b1 = 0, b2 = 0;
        for (int k = 0; k < n; k++) {
            int c0 = P0[k]-lay0[k], c1 = P1[k]-lay1[k], c2 = P2[k]-lay2[k];
            b0 += a0[k] < c0 ? a0[k] : c0;
            b1 += a1[k] < c1 ? a1[k] : c1;
            b2 += a2[k] < c2 ? a2[k] : c2;
        }
        int bound = b0 < b1 ? b0 : b1; if (b2 < bound) bound = b2;
        if (sz + bound < M) return;
    }
    for (int q = start; q < NC; q++) {
        if (sz + (NC - q) < M) return;
        if (px[q] > 0 && lay0[px[q]-1] != P0[px[q]-1]) return;   /* предыдущий x-слой уже не добрать */
        if (blocked[q] || linbl[q]) continue;
        if (lay0[px[q]] >= P0[px[q]] || lay1[py[q]] >= P1[py[q]] || lay2[pz[q]] >= P2[pz[q]]) continue;
        touch(q, +1);
        S[sz++] = q; inS[q] = 1; lay0[px[q]]++; lay1[py[q]]++; lay2[pz[q]]++;
        rec(q+1);
        sz--; inS[q] = 0; lay0[px[q]]--; lay1[py[q]]--; lay2[pz[q]]--;
        touch(q, -1);
    }
}

int main(int argc, char **argv)
{
    n = atoi(argv[1]); M = atoi(argv[2]);
    { char *t = strtok(argv[3], ","); for (int i = 0; i < n; i++) { P0[i] = atoi(t); t = strtok(NULL, ","); } }
    { char *t = strtok(argv[4], ","); for (int i = 0; i < n; i++) { P1[i] = atoi(t); t = strtok(NULL, ","); } }
    if (argc > 5) { char *t = strtok(argv[5], ","); for (int i = 0; i < n; i++) { P2[i] = atoi(t); t = strtok(NULL, ","); } }
    else for (int i = 0; i < n; i++) P2[i] = 3;          /* без третьего профиля — обычная ёмкость слоя */
    int s0 = 0, s1 = 0, s2 = 0; for (int i = 0; i < n; i++) { s0 += P0[i]; s1 += P1[i]; s2 += P2[i]; }
    if (s0 != M || s1 != M || (argc > 5 && s2 != M)) { printf("ОТКАЗ: профили не дают M (%d, %d, %d против %d)\n", s0, s1, s2, M); return 2; }
    NC = 0;
    for (int x = 0; x < n; x++) for (int y = 0; y < n; y++) for (int z = 0; z < n; z++) { px[NC]=x; py[NC]=y; pz[NC]=z; NC++; }
    rec(0);
    { char b0[80], b1[80]; int o = 0;
      for (int i = 0; i < n; i++) o += sprintf(b0+o, i ? ",%d" : "%d", P0[i]);
      o = 0; for (int i = 0; i < n; i++) o += sprintf(b1+o, i ? ",%d" : "%d", P1[i]);
      char b2[80]; o = 0; for (int i = 0; i < n; i++) o += sprintf(b2+o, i ? ",%d" : "%d", P2[i]);
      printf("n=%d M=%d P0=%s P1=%s P2=%s: конфигураций %lld (узлов %lld)\n", n, M, b0, b1, b2, found, nodes); }
    return 0;
}
