/* no4_sym.c — поиск конфигураций без четырёх компланарных, ИНВАРИАНТНЫХ под подгруппой.
 *
 * Идея: если конфигурация обязана быть неподвижной под g, то выбираются не клетки, а ОРБИТЫ.
 * При n=12 клеток 1728, а орбит цикла (x,y,z)->(y,z,x) всего 588 — пространство втрое меньше,
 * и каждый шаг кладёт сразу три точки.
 *
 * Почему именно цикл, а не отражение и не центральная симметрия:
 *   центральная p -> m-p:  два отрезка {p,m-p} и {q,m-q} проходят через ОДИН центр,
 *                          а две прямые через общую точку всегда компланарны -> четвёрка. Годна одна пара.
 *   отражение x<->y:       отрезки {p,sp} и {q,sq} перпендикулярны зеркалу, значит ПАРАЛЛЕЛЬНЫ
 *                          -> компланарны -> четвёрка. Годна одна пара.
 *   цикл порядка 3:        орбита лежит в плоскости x+y+z=s (перестановка координат хранит сумму),
 *                          значит орбиты обязаны иметь ПОПАРНО РАЗНЫЕ суммы — но это не запрет,
 *                          а всего лишь 34 доступных значения суммы при n=12.
 *   поворот на 180 вокруг оси z: орбиты по 2; при нечётном m неподвижных целых точек нет.
 *
 * Аргументы:  n группа цель секунды семя выход
 *   группа: cyc3 | rot2
 *
 * Проверка полная и независимая от построения: определитель по ВСЕМ четвёркам итогового набора.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static int n, m;
typedef struct { int x, y, z; } P;

/* --- орбиты --- */
#define MAXORB 9000
static P orb[MAXORB][3];
static int orbsz[MAXORB], norb = 0;
static int orbsum[MAXORB];           /* x+y+z, общий для всей орбиты у cyc3 */

static int kickmin = 1, kickspan = 2;
static long long fills = 0;   /* заполнений: проходов жадной укладки до упора — единица, сравнимая между редакциями */
static int chosen[MAXORB], nch = 0;  /* индексы выбранных орбит */
static int inset[MAXORB];
static P pts[256]; static int npts = 0;
static int bestpts_n = 0; static P bestpts[256];

static void apply_cyc3(P p, P *o) { o->x = p.y; o->y = p.z; o->z = p.x; }
static void apply_rot2(P p, P *o) { o->x = m - p.x; o->y = m - p.y; o->z = p.z; }

static void build_orbits(const char *grp) {
    static int seen[27000]; memset(seen, 0, sizeof seen);
    int cyc = strcmp(grp, "cyc3") == 0;
    for (int x = 0; x < n; x++) for (int y = 0; y < n; y++) for (int z = 0; z < n; z++) {
        int id = (x * n + y) * n + z; if (seen[id]) continue;
        P p = {x, y, z}, q; int k = 0;
        P cur = p;
        do {
            int cid = (cur.x * n + cur.y) * n + cur.z;
            if (!seen[cid]) { seen[cid] = 1; orb[norb][k++] = cur; }
            if (cyc) apply_cyc3(cur, &q); else apply_rot2(cur, &q);
            cur = q;
        } while (!(cur.x == p.x && cur.y == p.y && cur.z == p.z) && k < 3);
        orbsz[norb] = k; orbsum[norb] = x + y + z;
        norb++;
    }
}

/* определитель для четвёрки a,b,c,d */
static long long det4(P a, P b, P c, P d) {
    long long ux = b.x - a.x, uy = b.y - a.y, uz = b.z - a.z;
    long long vx = c.x - a.x, vy = c.y - a.y, vz = c.z - a.z;
    long long wx = d.x - a.x, wy = d.y - a.y, wz = d.z - a.z;
    return ux * (vy * wz - vz * wy) - uy * (vx * wz - vz * wx) + uz * (vx * wy - vy * wx);
}
static int collinear3(P a, P b, P c) {
    long long ux = b.x - a.x, uy = b.y - a.y, uz = b.z - a.z;
    long long vx = c.x - a.x, vy = c.y - a.y, vz = c.z - a.z;
    return (uy * vz - uz * vy) == 0 && (uz * vx - ux * vz) == 0 && (ux * vy - uy * vx) == 0;
}


/* ——— быстрый необходимый фильтр по направлениям ———
 * Если никакие четыре не компланарны, то у ЛЮБЫХ двух пар направления различны:
 * параллельные прямые компланарны, а пересекающиеся дают коллинеарную тройку.
 * Условие НЕОБХОДИМОЕ, не достаточное, поэтому полная проверка остаётся следом за ним.
 * Стоит O(k) на кандидата против O(k^3) у полной — и отсеивает большинство до неё.
 * Проверено на свидетелях n=9,10,11,12: совпадений направлений ровно ноль. */
static unsigned char *dseen; static int DM, DSPAN;
static int dtmp[4096], dtn;
static int dircode(int dx, int dy, int dz) {
    int g = 0, a = dx<0?-dx:dx, b = dy<0?-dy:dy, c = dz<0?-dz:dz;
    while (b) { int t = a % b; a = b; b = t; } g = a;
    while (c) { int t = g % c; g = c; c = t; }
    if (g) { dx /= g; dy /= g; dz /= g; }
    if (dx < 0 || (dx == 0 && (dy < 0 || (dy == 0 && dz < 0)))) { dx = -dx; dy = -dy; dz = -dz; }
    return (dx + DM) * DSPAN * DSPAN + (dy + DM) * DSPAN + (dz + DM);
}
static void dir_clear_tmp(void) { for (int i = 0; i < dtn; i++) dseen[dtmp[i]] = 0; dtn = 0; }
static int dir_try(P a, P b) {                       /* 1 если направление свободно, и помечает временно */
    int c = dircode(b.x-a.x, b.y-a.y, b.z-a.z);
    if (dseen[c]) return 0;
    dseen[c] = 1; dtmp[dtn++] = c; return 1;
}
static void dir_commit(void) { dtn = 0; }            /* временные пометки становятся постоянными */
static void dir_rebuild(void) {
    memset(dseen, 0, (size_t)DSPAN*DSPAN*DSPAN); dtn = 0;
    for (int i = 0; i < npts; i++) for (int j = i+1; j < npts; j++)
        dseen[dircode(pts[j].x-pts[i].x, pts[j].y-pts[i].y, pts[j].z-pts[i].z)] = 1;
}

/* можно ли добавить орбиту o к текущему набору */
static int can_add(int o) {
    int k = orbsz[o];
    P np[3]; for (int i = 0; i < k; i++) np[i] = orb[o][i];
    /* дешёвый необходимый фильтр: все новые пары обязаны дать свежие направления */
    for (int i = 0; i < k; i++) {
        for (int j = 0; j < npts; j++) if (!dir_try(pts[j], np[i])) { dir_clear_tmp(); return 0; }
        for (int j = 0; j < i; j++)    if (!dir_try(np[j], np[i]))  { dir_clear_tmp(); return 0; }
    }
    dir_clear_tmp();
    /* тройки внутри новых + существующие */
    int tot = npts + k;
    P all[256]; memcpy(all, pts, npts * sizeof(P));
    for (int i = 0; i < k; i++) all[npts + i] = np[i];
    /* коллинеарные тройки с хотя бы одной новой */
    for (int a = 0; a < tot; a++) for (int b = a + 1; b < tot; b++) for (int c = b + 1; c < tot; c++) {
        if (c < npts) continue;                       /* все три старые — уже проверено */
        if (collinear3(all[a], all[b], all[c])) return 0;
    }
    /* компланарные четвёрки с хотя бы одной новой */
    for (int a = 0; a < tot; a++) for (int b = a + 1; b < tot; b++) for (int c = b + 1; c < tot; c++)
        for (int d = c + 1; d < tot; d++) {
            if (d < npts) continue;
            if (det4(all[a], all[b], all[c], all[d]) == 0) return 0;
        }
    return 1;
}

static void add_orbit(int o) {
    int k = orbsz[o];
    for (int i = 0; i < k; i++) {
        for (int j = 0; j < npts; j++) dseen[dircode(orb[o][i].x-pts[j].x, orb[o][i].y-pts[j].y, orb[o][i].z-pts[j].z)] = 1;
        for (int j = 0; j < i; j++)    dseen[dircode(orb[o][i].x-orb[o][j].x, orb[o][i].y-orb[o][j].y, orb[o][i].z-orb[o][j].z)] = 1;
        pts[npts++] = orb[o][i];
    }
    chosen[nch++] = o; inset[o] = 1;
}
static void rebuild(void) {
    npts = 0;
    for (int i = 0; i < nch; i++) for (int j = 0; j < orbsz[chosen[i]]; j++) pts[npts++] = orb[chosen[i]][j];
    dir_rebuild();
}
static void drop_at(int idx) { inset[chosen[idx]] = 0; chosen[idx] = chosen[--nch]; rebuild(); }

/* полная независимая проверка итога */
static int verify(P *s, int k, int *bad3, int *bad4) {
    *bad3 = 0; *bad4 = 0;
    for (int a = 0; a < k; a++) for (int b = a + 1; b < k; b++) for (int c = b + 1; c < k; c++) {
        if (collinear3(s[a], s[b], s[c])) (*bad3)++;
        for (int d = c + 1; d < k; d++) if (det4(s[a], s[b], s[c], s[d]) == 0) (*bad4)++;
    }
    return *bad3 == 0 && *bad4 == 0;
}


/* добор свободными клетками: область шире орбитной, но ход остаётся наращиванием — тем самым,
   что единственно работает при рассеянных максимумах. Орбиты дают отбор, клетки дают добор. */
static P allcell[28000]; static int nallcell=0;
static int fits1(P q){
    for(int i=0;i<npts;i++) if(pts[i].x==q.x&&pts[i].y==q.y&&pts[i].z==q.z) return 0;
    for(int a=0;a<npts;a++)for(int b=a+1;b<npts;b++) if(collinear3(pts[a],pts[b],q)) return 0;
    for(int a=0;a<npts;a++)for(int b=a+1;b<npts;b++)for(int c=b+1;c<npts;c++)
        if(det4(pts[a],pts[b],pts[c],q)==0) return 0;
    return 1;
}
static void topup(int *ord){
    for(int i=nallcell-1;i>0;i--){int j=rand()%(i+1);int t=ord[i];ord[i]=ord[j];ord[j]=t;}
    for(int i=0;i<nallcell;i++) if(fits1(allcell[ord[i]])) pts[npts++]=allcell[ord[i]];
}

static void dump(const char *out, unsigned seed) {
    fprintf(stderr, "  %d точек\n", bestpts_n); fflush(stderr);
    if (!out) return;
    FILE *f = fopen(out, "w"); if (!f) return;
    fprintf(f, "# n=%d группа=cyc3 точек=%d семя=%u\n", n, bestpts_n, seed);
    for (int i = 0; i < bestpts_n; i++) fprintf(f, "%d %d %d\n", bestpts[i].x, bestpts[i].y, bestpts[i].z);
    fclose(f);
}

int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage: n группа цель секунды семя выход\n"); return 2; }
    n = atoi(argv[1]); m = n - 1;
    if ((long)n*n*n > 27000 || (long)n*n*n/3 + n > 9000) {
        fprintf(stderr, "ОТКАЗ: n=%d не помещается в статические массивы. Молча портить память нельзя.\n", n);
        return 2; }
    const char *grp = argv[2];
    int target = atoi(argv[3]); double T = atof(argv[4]);
    unsigned seed = (unsigned)atoi(argv[5]); const char *out = argv[6];
    if (argc > 7) { kickmin = atoi(argv[7]); kickspan = argc > 8 ? atoi(argv[8]) : 1; }
    srand(seed);
    DM = n - 1; DSPAN = 2*DM + 1;
    dseen = calloc((size_t)DSPAN*DSPAN*DSPAN, 1);
    if (!dseen) { fprintf(stderr, "ОТКАЗ: не хватило памяти под таблицу направлений\n"); return 2; }
    build_orbits(grp);
    nallcell=0; for(int x=0;x<n;x++)for(int y=0;y<n;y++)for(int z=0;z<n;z++){allcell[nallcell].x=x;allcell[nallcell].y=y;allcell[nallcell].z=z;nallcell++;}
    fprintf(stderr, "n=%d группа=%s орбит=%d цель=%d\n", n, grp, norb, target);
    clock_t st = clock();
    int order[MAXORB];
    long restarts = 0;
    while ((double)(clock() - st) / CLOCKS_PER_SEC < T) {
        restarts++;
        nch = 0; npts = 0; memset(inset, 0, sizeof inset); dir_rebuild();
        for (int i = 0; i < norb; i++) order[i] = i;
        for (int i = norb - 1; i > 0; i--) { int j = rand() % (i + 1); int t = order[i]; order[i] = order[j]; order[j] = t; }
        for (int i = 0; i < norb; i++) if (can_add(order[i])) add_orbit(order[i]); fills++;
        { static int co[28000]; for(int q=0;q<nallcell;q++) co[q]=q; topup(co); }
        /* итерированный локальный: выбить 1-2 орбиты, дорастить */
        for (int it = 0; it < 4000 && npts < target; it++) {
            if ((double)(clock() - st) / CLOCKS_PER_SEC > T) break;
            if (npts > bestpts_n) { bestpts_n = npts; memcpy(bestpts, pts, npts * sizeof(P)); dump(out, seed); }
            int kick = kickmin + rand() % kickspan;
            for (int q = 0; q < kick && nch > 0; q++) drop_at(rand() % nch);
            for (int i = norb - 1; i > 0; i--) { int j = rand() % (i + 1); int t = order[i]; order[i] = order[j]; order[j] = t; }
            for (int i = 0; i < norb; i++) if (!inset[order[i]] && can_add(order[i])) add_orbit(order[i]); fills++;
            { static int co[28000]; for(int q=0;q<nallcell;q++) co[q]=q; topup(co); }
        }
        if (npts > bestpts_n) { bestpts_n = npts; memcpy(bestpts, pts, npts * sizeof(P)); dump(out, seed); }
        if (bestpts_n >= target) break;
    }
    int b3, b4; int ok = verify(bestpts, bestpts_n, &b3, &b4);
    fprintf(stderr, "лучшее %d точек, ЗАПОЛНЕНИЙ %lld, внешних %ld, проверка: коллинеарных %d компланарных %d %s\n",
            bestpts_n, fills, restarts, b3, b4, ok ? "ЧИСТО" : "БРАК");
    if (ok && out) {
        FILE *f = fopen(out, "w");
        if (f) {
            fprintf(f, "# n=%d группа=%s точек=%d семя=%u\n", n, grp, bestpts_n, seed);
            for (int i = 0; i < bestpts_n; i++) fprintf(f, "%d %d %d\n", bestpts[i].x, bestpts[i].y, bestpts[i].z);
            fclose(f);
        }
    }
    return bestpts_n >= target ? 0 : 1;
}
