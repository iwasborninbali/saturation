/* fast/lns.c — large-neighbourhood search on LAWFUL books: destroy a spatial cluster of orbits,
 * repair by bounded exact DFS over the orbits that became admissible (field F == 0 on all cells),
 * accept if the repair is at least as large (sideways moves keep the walk alive).
 * Only proposes; solve.py re-enters through saturation.the_law.
 *
 * usage: lns n group seed seconds outprefix startfile [nodebudget] [rmin] [rmax]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <sys/time.h>

#define MAXN 128
#define MAXC (MAXN * MAXN)
#define MAXK (2 * MAXN + 8)

static int n, m, G;
static int orb[MAXC][8], orbsz[MAXC], orbrep[MAXC];
static int occ[MAXC], plist[MAXK], pos[MAXC], np;
static int rc[MAXN], cc[MAXN];
static long conf;
static int F[MAXC];
static int reps[MAXK], nreps, repidx[MAXC];
static int gcdtab[MAXN][MAXN];

static double now(void) { struct timeval tv; gettimeofday(&tv, NULL); return tv.tv_sec + tv.tv_usec * 1e-6; }
static unsigned long long rs;
static inline unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static inline int rint_(int k) { return (int)(rnd() % (unsigned long long)k); }
static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
static int cmpint(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }

static void motion(int g, int u, int v, int *pu, int *pv) {
    switch (g) {
        case 0: *pu = u; *pv = v; break;
        case 1: *pu = v; *pv = m - u; break;
        case 2: *pu = m - u; *pv = m - v; break;
        case 3: *pu = m - v; *pv = u; break;
        case 4: *pu = v; *pv = u; break;
        case 5: *pu = m - u; *pv = v; break;
        case 6: *pu = u; *pv = m - v; break;
        default: *pu = m - v; *pv = m - u; break;
    }
}
static void build_group(const char *name) {
    int gl[8], k = 0;
    if (!strcmp(name, "id")) { gl[k++] = 0; }
    else if (!strcmp(name, "rot2")) { gl[k++] = 0; gl[k++] = 2; }
    else if (!strcmp(name, "diag")) { gl[k++] = 0; gl[k++] = 4; }
    else if (!strcmp(name, "adiag")) { gl[k++] = 0; gl[k++] = 7; }
    else if (!strcmp(name, "v2")) { gl[k++] = 0; gl[k++] = 2; gl[k++] = 4; gl[k++] = 7; }
    else if (!strcmp(name, "h")) { gl[k++] = 0; gl[k++] = 5; }
    else if (!strcmp(name, "v")) { gl[k++] = 0; gl[k++] = 6; }
    else if (!strcmp(name, "hv")) { gl[k++] = 0; gl[k++] = 2; gl[k++] = 5; gl[k++] = 6; }
    else if (!strcmp(name, "c4")) { gl[k++] = 0; gl[k++] = 1; gl[k++] = 2; gl[k++] = 3; }
    else if (!strcmp(name, "d4")) { for (int i = 0; i < 8; i++) gl[k++] = i; }
    else { fprintf(stderr, "unknown group %s\n", name); exit(2); }
    G = k;
    for (int c = 0; c < n * n; c++) {
        int u = c / n, v = c % n, tmp[8], t = 0;
        for (int i = 0; i < G; i++) {
            int uu, vv; motion(gl[i], u, v, &uu, &vv);
            int x = uu * n + vv, dup = 0;
            for (int j = 0; j < t; j++) if (tmp[j] == x) dup = 1;
            if (!dup) tmp[t++] = x;
        }
        qsort(tmp, t, sizeof(int), cmpint);
        orbsz[c] = t; for (int j = 0; j < t; j++) orb[c][j] = tmp[j]; orbrep[c] = tmp[0];
    }
}
static inline void walk(int a, int b, int d) {
    int au = a / n, av = a % n, bu = b / n, bv = b % n;
    int du = bu - au, dv = bv - av;
    int g = gcdtab[abs(du)][abs(dv)];
    du /= g; dv /= g;
    int u = au, v = av;
    while (u - du >= 0 && u - du <= m && v - dv >= 0 && v - dv <= m) { u -= du; v -= dv; }
    while (u >= 0 && u <= m && v >= 0 && v <= m) { F[u * n + v] += d; u += du; v += dv; }
}
static void add_point(int c) {
    conf += F[c];
    for (int i = 0; i < np; i++) walk(c, plist[i], +1);
    occ[c] = 1; pos[c] = np; plist[np++] = c; rc[c / n]++; cc[c % n]++;
}
static void del_point(int c) {
    int i = pos[c], last = plist[--np];
    plist[i] = last; pos[last] = i; occ[c] = 0; rc[c / n]--; cc[c % n]--;
    for (int k = 0; k < np; k++) walk(c, plist[k], -1);
    conf -= F[c];
}
/* orbit admissible now: all cells free, F == 0, capacities (counting the orbit's own cells) */
static int orbit_admissible(int r) {
    int k = orbsz[r]; static int ru[8], rv[8];
    for (int j = 0; j < k; j++) { int c = orb[r][j]; if (occ[c] || F[c] != 0) return 0; ru[j] = c / n; rv[j] = c % n; }
    for (int j = 0; j < k; j++) {
        int cu = 0, cv = 0;
        for (int i = 0; i < k; i++) { if (ru[i] == ru[j]) cu++; if (rv[i] == rv[j]) cv++; }
        if (rc[ru[j]] + cu > 2 || cc[rv[j]] + cv > 2) return 0;
    }
    return 1;
}
static void insert_orbit(int r) { for (int j = 0; j < orbsz[r]; j++) add_point(orb[r][j]); repidx[r] = nreps; reps[nreps++] = r; }
static void remove_orbit(int r) {
    for (int j = 0; j < orbsz[r]; j++) del_point(orb[r][j]);
    int i = repidx[r], last = reps[--nreps]; reps[i] = last; repidx[last] = i; repidx[r] = -1;
}
static long full_conf(void) {
    long t = 0;
    for (int i = 0; i < np; i++) for (int j = i + 1; j < np; j++) for (int k = j + 1; k < np; k++) {
        int a = plist[i], b = plist[j], c = plist[k];
        long ua = a / n, va = a % n, ub = b / n, vb = b % n, uc = c / n, vc = c % n;
        if ((ub - ua) * (vc - va) == (vb - va) * (uc - ua)) t++;
    }
    return t;
}
static void write_tokens(const char *path) {
    FILE *f = fopen(path, "w"); if (!f) return;
    int tmp[MAXK]; for (int i = 0; i < np; i++) tmp[i] = plist[i];
    qsort(tmp, np, sizeof(int), cmpint);
    for (int i = 0; i < np; i++) fprintf(f, "%d%c", tmp[i], i + 1 < np ? ' ' : '\n');
    fclose(f);
}

/* ---- bounded exact repair: DFS over candidate orbits ---- */
static int cand[MAXC], ncand;
static long nodes, node_budget;
static int best_found, best_set[64], cur_set[64], ncur;

static void dfs(int start, int remaining_possible) {
    if (nodes++ > node_budget) return;
    if (ncur > best_found) { best_found = ncur; for (int i = 0; i < ncur; i++) best_set[i] = cur_set[i]; }
    if (ncur + remaining_possible <= best_found) return;
    for (int i = start; i < ncand; i++) {
        if (nodes > node_budget) return;
        int r = cand[i];
        if (!orbit_admissible(r)) continue;
        insert_orbit(r);
        if (conf != 0) { remove_orbit(r); continue; }     /* the orbit itself made a triple */
        cur_set[ncur++] = r;
        dfs(i + 1, ncand - i - 1);
        ncur--;
        remove_orbit(r);
        if (ncur + (ncand - i - 1) <= best_found) return;
    }
}

int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage: lns n group seed seconds outprefix startfile [nodebudget] [rmin] [rmax]\n"); return 2; }
    n = atoi(argv[1]); m = n - 1;
    const char *gname = argv[2];
    rs = 0x9E3779B97F4A7C15ULL ^ ((unsigned long long)atoll(argv[3]) * 0x2545F4914F6CDD1DULL + 31337);
    for (int i = 0; i < 20; i++) rnd();
    double seconds = atof(argv[4]);
    const char *outprefix = argv[5];
    const char *startfile = argv[6];
    node_budget = argc > 7 ? atol(argv[7]) : 5000;
    int rmin = argc > 8 ? atoi(argv[8]) : 2, rmax = argc > 9 ? atoi(argv[9]) : 8;
    for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) gcdtab[a][b] = gcd(a, b);
    build_group(gname);
    for (int c = 0; c < n * n; c++) repidx[c] = -1;
    FILE *f = fopen(startfile, "r"); if (!f) { fprintf(stderr, "cannot open %s\n", startfile); return 2; }
    int t;
    while (fscanf(f, "%d", &t) == 1) {
        if (t < 0 || t >= n * n) continue;
        int r = orbrep[t]; if (repidx[r] >= 0) continue;
        if (orbit_admissible(r)) insert_orbit(r);
    }
    fclose(f);
    if (conf != 0 || full_conf() != 0) { fprintf(stderr, "start not lawful\n"); return 3; }
    fprintf(stderr, "start: %d tokens (%d orbits)\n", np, nreps);

    double t0 = now(), tlast = t0;
    long it = 0, sideways = 0, improvements = 0, restored = 0, tot_nodes = 0, tot_cand = 0, budget_hits = 0;
    int best = np;
    char path[512];
    snprintf(path, sizeof path, "%s_lawful_%d.txt", outprefix, np); write_tokens(path);
    static int D[64]; int nD;

    for (;;) {
        it++;
        if ((it & 63) == 0) {
            double el = now() - t0;
            if (el > seconds) break;
            if (now() - tlast > 5.0) {
                tlast = now();
                fprintf(stderr, "[%6.0fs] it=%ld K=%d best=%d sideways=%ld impr=%ld restored=%ld avg_nodes=%.0f avg_cand=%.1f budget_hits=%ld\n", el, it, np, best, sideways, improvements, restored, (double)tot_nodes / it, (double)tot_cand / it, budget_hits);
            }
        }
        /* destroy: cluster around a random centre — the r orbits with the closest cells */
        int r_target = rmin + rint_(rmax - rmin + 1);
        int cu = rint_(n), cv = rint_(n);
        /* score orbits by min distance of their cells to the centre */
        static long score[MAXK]; static int order[MAXK];
        for (int i = 0; i < nreps; i++) {
            int rr = reps[i]; long best_d = 1L << 40;
            for (int j = 0; j < orbsz[rr]; j++) { int c = orb[rr][j]; long du = c / n - cu, dv = c % n - cv; long d = du * du + dv * dv; if (d < best_d) best_d = d; }
            score[i] = best_d * 16 + rint_(16); order[i] = i;
        }
        /* partial selection of the r_target smallest */
        nD = 0;
        for (int k = 0; k < r_target && k < nreps; k++) {
            int bi = k;
            for (int i = k + 1; i < nreps; i++) if (score[order[i]] < score[order[bi]]) bi = i;
            int tmp = order[k]; order[k] = order[bi]; order[bi] = tmp;
            D[nD++] = reps[order[k]];
        }
        int before = np;
        for (int i = 0; i < nD; i++) remove_orbit(D[i]);
        /* candidates: admissible orbits (including the destroyed ones) */
        ncand = 0;
        for (int c = 0; c < n * n; c++) {
            if (orbrep[c] != c || repidx[c] >= 0) continue;
            if (!orbit_admissible(c)) continue;
            cand[ncand++] = c;
        }
        /* shuffle candidates for diversity */
        for (int i = ncand - 1; i > 0; i--) { int j = rint_(i + 1); int tmp = cand[i]; cand[i] = cand[j]; cand[j] = tmp; }
        nodes = 0; best_found = 0; ncur = 0;
        dfs(0, ncand);
        tot_nodes += nodes; tot_cand += ncand; if (nodes > node_budget) budget_hits++;
        /* apply best_found if it does not lose tokens (in token count) */
        int gained_tokens = 0; for (int i = 0; i < best_found; i++) gained_tokens += orbsz[best_set[i]];
        int lost_tokens = before - np;
        if (gained_tokens >= lost_tokens) {
            for (int i = 0; i < best_found; i++) { if (orbit_admissible(best_set[i])) insert_orbit(best_set[i]); }
            if (conf != 0) { fprintf(stderr, "BUG conf after repair\n"); return 3; }
            if (np > before) improvements++; else sideways++;
        } else {
            for (int i = 0; i < nD; i++) insert_orbit(D[i]);
            restored++;
        }
        if (np > best) {
            best = np;
            snprintf(path, sizeof path, "%s_lawful_%d.txt", outprefix, np); write_tokens(path);
            fprintf(stderr, "LAWFUL %d tokens -> %s (%.0fs)\n", np, path, now() - t0);
            if (np == 2 * n) { printf("SATURATED %s\n", path); fflush(stdout); return 0; }
        }
    }
    if (full_conf() != conf || conf != 0) { fprintf(stderr, "conf mismatch at end\n"); return 3; }
    fprintf(stderr, "done: it=%ld K=%d best=%d sideways=%ld impr=%ld restored=%ld\n", it, np, best, sideways, improvements, restored);
    printf("DONE n=%d best=%d\n", n, best);
    return 0;
}
