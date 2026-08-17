/* fast/mc.c — min-conflicts / annealed local search with a maintained pair-line field.
 *
 * Law (saturation.py): no three chosen tokens collinear. State: union of orbits under a
 * subgroup of the 8 motions, <= 2 tokens per row/column. Cost = number of collinear triples.
 * Field: F[c] = number of unordered pairs {Q,R} of state tokens whose line passes through
 * cell c (for c in the state, F[c] = T(c) + (np-1)). Maintained by walking lines.
 * This program only PROPOSES; solve.py re-enters every book through the law.
 *
 * usage: mc n K group seed seconds T noise outprefix [grow] [startfile]
 *   grow=1: when a lawful state is reached, add one orbit (K grows) and continue
 *   noise: probability of a random (non-greedy) target
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
static long tabu_until[MAXC];
static long TABU = 0; static int STEEP = 0;

static double now(void) { struct timeval tv; gettimeofday(&tv, NULL); return tv.tv_sec + tv.tv_usec * 1e-6; }
static unsigned long long rs;
static inline unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static inline int rint_(int k) { return (int)(rnd() % (unsigned long long)k); }
static inline double runif(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
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

/* walk the line through cells a and b (a != b), adding d to F on every grid cell of it */
static inline void walk(int a, int b, int d) {
    int au = a / n, av = a % n, bu = b / n, bv = b % n;
    int du = bu - au, dv = bv - av;
    int g = gcdtab[abs(du)][abs(dv)];
    du /= g; dv /= g;
    /* find the first cell of the line inside the grid: go backwards from a */
    int u = au, v = av;
    while (u - du >= 0 && u - du <= m && v - dv >= 0 && v - dv <= m) { u -= du; v -= dv; }
    while (u >= 0 && u <= m && v >= 0 && v <= m) { F[u * n + v] += d; u += du; v += dv; }
}

static inline int T_of(int c) { return F[c] - (np - 1); }   /* c in state */

static void add_point(int c) {                 /* c not in state */
    conf += F[c];
    for (int i = 0; i < np; i++) walk(c, plist[i], +1);
    occ[c] = 1; pos[c] = np; plist[np++] = c; rc[c / n]++; cc[c % n]++;
}
static void del_point(int c) {                 /* c in state */
    int i = pos[c], last = plist[--np];
    plist[i] = last; pos[last] = i; occ[c] = 0; rc[c / n]--; cc[c % n]--;
    for (int k = 0; k < np; k++) walk(c, plist[k], -1);
    conf -= F[c];
}
static int orbit_free(int r) {                 /* cells free + capacities (counting the orbit's own cells) */
    int k = orbsz[r];
    static int ru[8], rv[8];
    for (int j = 0; j < k; j++) {
        int c = orb[r][j];
        if (occ[c]) return 0;
        ru[j] = c / n; rv[j] = c % n;
    }
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
/* cost of inserting orbit r (exact, via insertion then removal) */
static long insert_cost(int r) {
    long before = conf; insert_orbit(r); long d = conf - before; remove_orbit(r); return d;
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
static int add_random_orbit(int tries) {
    for (int t = 0; t < tries; t++) {
        int r = orbrep[rint_(n * n)];
        if (repidx[r] >= 0) continue;
        if (orbit_free(r)) { insert_orbit(r); return 1; }
    }
    return 0;
}
/* add the orbit with the least insertion cost among a sample of free reps */
static int add_best_orbit(int sample) {
    int bestr = -1; long bestc = 1L << 40;
    for (int t = 0; t < sample; t++) {
        int r = orbrep[rint_(n * n)];
        if (repidx[r] >= 0 || !orbit_free(r)) continue;
        long p = 0; for (int j = 0; j < orbsz[r]; j++) p += F[orb[r][j]];
        if (p < bestc) { bestc = p; bestr = r; }
    }
    if (bestr < 0) return 0;
    insert_orbit(bestr); return 1;
}

int main(int argc, char **argv) {
    if (argc < 9) { fprintf(stderr, "usage: mc n K group seed seconds T noise outprefix [grow] [startfile]\n"); return 2; }
    n = atoi(argv[1]); m = n - 1;
    int K = atoi(argv[2]);
    const char *gname = argv[3];
    rs = 0x9E3779B97F4A7C15ULL ^ ((unsigned long long)atoll(argv[4]) * 0x2545F4914F6CDD1DULL + 777);
    for (int i = 0; i < 20; i++) rnd();
    double seconds = atof(argv[5]);
    double T = atof(argv[6]);
    double noise = atof(argv[7]);
    double p2 = getenv("P2") ? atof(getenv("P2")) : 0.3;
    TABU = getenv("TABU") ? atol(getenv("TABU")) : 0;
    STEEP = getenv("STEEP") ? atoi(getenv("STEEP")) : 0;
    const char *outprefix = argv[8];
    int grow = argc > 9 ? atoi(argv[9]) : 0;
    const char *startfile = argc > 10 ? argv[10] : NULL;
    for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) gcdtab[a][b] = gcd(a, b);
    build_group(gname);
    for (int c = 0; c < n * n; c++) repidx[c] = -1;

    if (startfile) {
        FILE *f = fopen(startfile, "r"); if (!f) { fprintf(stderr, "cannot open %s\n", startfile); return 2; }
        int t;
        while (fscanf(f, "%d", &t) == 1) {
            if (t < 0 || t >= n * n) continue;
            int r = orbrep[t]; if (repidx[r] >= 0) continue;
            if (orbit_free(r)) insert_orbit(r); else fprintf(stderr, "start token %d skipped\n", t);
        }
        fclose(f);
        fprintf(stderr, "start: %d tokens, %ld triples\n", np, conf);
    }
    { long guard = 0;
      while (np < K && guard < 20000000L) { guard++; if (!add_random_orbit(64)) { if (nreps > 0) remove_orbit(reps[rint_(nreps)]); } }
      fprintf(stderr, "initial: %d tokens, %ld triples\n", np, conf); }
    if (full_conf() != conf) { fprintf(stderr, "conf mismatch at start %ld %ld\n", full_conf(), conf); return 3; }

    double t0 = now(), tlast = t0;
    long it = 0, acc = 0, best_conf = conf; int best_lawful = 0;
    long minconf_written = -1;
    char path[512];
    int cand[MAXC]; int ncand;
    int confl[MAXK];
    static int best_tokens[MAXK]; int nbest_tokens = 0;
    long RELOAD = getenv("RELOAD") ? atol(getenv("RELOAD")) : 0;   /* iterations between drift checks; 0 = off */
    long DRIFT = getenv("DRIFT") ? atol(getenv("DRIFT")) : 6;       /* conf threshold to reload */

    for (;;) {
        it++;
        if ((it & 255) == 0) {
            double el = now() - t0;
            if (el > seconds) break;
            if (now() - tlast > 5.0) {
                tlast = now();
                fprintf(stderr, "[%6.0fs] it=%ld K=%d conf=%ld best_conf=%ld acc=%ld lawful_best=%d\n", el, it, np, conf, best_conf, acc, best_lawful);
                acc = 0;
            }
        }
        if (conf == 0) {
            if (np > best_lawful) {
                best_lawful = np;
                nbest_tokens = np; for (int i = 0; i < np; i++) best_tokens[i] = plist[i];
                snprintf(path, sizeof path, "%s_lawful_%d.txt", outprefix, np);
                write_tokens(path);
                fprintf(stderr, "LAWFUL %d tokens -> %s (%.0fs)\n", np, path, now() - t0);
                if (np == 2 * n) { fprintf(stderr, "SATURATED n=%d\n", n); printf("SATURATED %s\n", path); fflush(stdout); return 0; }
            }
            if (grow) { if (add_best_orbit(400) || add_random_orbit(1000)) { K = np; best_conf = conf; } }
        }
        if (conf < best_conf) {
            best_conf = conf;
            if (conf != minconf_written) { minconf_written = conf; snprintf(path, sizeof path, "%s_minconf.txt", outprefix); write_tokens(path); }
        }
        if (RELOAD && nbest_tokens > 0 && (it % RELOAD) == 0 && conf > DRIFT) {
            /* drifted: rebuild the best lawful state, then let grow add one orbit */
            while (nreps > 0) remove_orbit(reps[nreps - 1]);
            for (int i = 0; i < nbest_tokens; i++) { int r = orbrep[best_tokens[i]]; if (repidx[r] < 0 && orbit_free(r)) insert_orbit(r); }
            K = np; best_conf = conf;
            continue;
        }
        if (np < K) add_random_orbit(4);
        if (nreps < 2) continue;

        /* choose orbit r1: a conflicting one with prob 1-noise/2, else random */
        int nc = 0;
        for (int i = 0; i < nreps; i++) {
            int rr = reps[i], bad = 0;
            for (int j = 0; j < orbsz[rr]; j++) if (T_of(orb[rr][j]) > 0) { bad = 1; break; }
            if (bad) confl[nc++] = rr;
        }
        int r1;
        if (STEEP && nc > 0 && runif() > noise * 0.5) {
            long bt = -1; r1 = confl[0];
            for (int i = 0; i < nc; i++) { long t = 0; for (int j = 0; j < orbsz[confl[i]]; j++) t += T_of(orb[confl[i]][j]); if (t > bt || (t == bt && (rnd() & 1))) { bt = t; r1 = confl[i]; } }
        } else r1 = (nc > 0 && runif() > noise * 0.5) ? confl[rint_(nc)] : reps[rint_(nreps)];
        int two = (np >= 2 * n) || (runif() < p2);
        int r2 = -1;
        if (two) { do { r2 = reps[rint_(nreps)]; } while (r2 == r1); }

        long before = conf;
        remove_orbit(r1);
        if (two) remove_orbit(r2);

        int ins[2], nins = 0;
        for (int step = 0; step < (two ? 2 : 1); step++) {
            int chosen = -1;
            if (runif() < noise) {
                for (int t = 0; t < 4000 && chosen < 0; t++) {
                    int c = orbrep[rint_(n * n)];
                    if (c == r1 || repidx[c] >= 0 || !orbit_free(c)) continue;
                    chosen = c;
                }
            } else {
                long bestp = 1L << 40; ncand = 0;
                for (int c = 0; c < n * n; c++) {
                    if (orbrep[c] != c || c == r1 || repidx[c] >= 0) continue;
                    if (!orbit_free(c)) continue;
                    long p = 0; for (int j = 0; j < orbsz[c]; j++) p += F[orb[c][j]];
                    if (TABU && tabu_until[c] > it && p > 0) continue;   /* aspiration: proxy 0 always allowed */
                    if (p < bestp) { bestp = p; ncand = 0; }
                    if (p == bestp && ncand < MAXC) cand[ncand++] = c;
                }
                if (ncand > 0) chosen = cand[rint_(ncand)];
            }
            if (chosen < 0) break;
            insert_orbit(chosen); ins[nins++] = chosen;
        }
        long delta = conf - before;
        int complete = (nins == (two ? 2 : 1));
        if (complete && (delta <= 0 || runif() < exp(-delta / T))) {
            acc++;
            if (TABU) { tabu_until[r1] = it + TABU + rint_((int)TABU + 1); if (two) tabu_until[r2] = it + TABU + rint_((int)TABU + 1); }
        }
        else {
            for (int i = nins - 1; i >= 0; i--) remove_orbit(ins[i]);
            if (two) insert_orbit(r2);
            insert_orbit(r1);
        }
    }
    if (full_conf() != conf) { fprintf(stderr, "conf mismatch at end\n"); return 3; }
    fprintf(stderr, "done: it=%ld K=%d conf=%ld best_conf=%ld lawful_best=%d\n", it, np, conf, best_conf, best_lawful);
    printf("DONE n=%d K=%d best_conf=%ld lawful_best=%d\n", n, np, best_conf, best_lawful);
    return 0;
}
