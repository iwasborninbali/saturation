/* fast/sa.c — simulated annealing on the "no chosen token is an affine blend of two others"
 * law of saturation.py. State = union of orbits under a chosen subgroup of the 8 motions,
 * with at most 2 tokens per row and per column. Cost = number of collinear (degenerate)
 * triples. This program only PROPOSES books; every reported book re-enters saturation.the_law
 * through solve.py.
 *
 * usage: sa n K group seed seconds T0 T1 outprefix [grow] [startfile]
 *   n        resolution (<= 128)
 *   K        number of tokens to hold (2n for saturation attempts)
 *   group    id | rot2 | diag | adiag | v2 | h | v | c4 | d4
 *   seed     rng seed
 *   seconds  wall-clock budget
 *   T0, T1   start / end temperature (geometric schedule)
 *   outprefix files: <outprefix>_lawful_<K>.txt (token lists), <outprefix>_minconf.txt
 *   grow     0/1: when a lawful state at K < 2n is found, add a token and continue (K grows)
 *   startfile optional token list to start from (must be a union of orbits)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <sys/time.h>

#define MAXN 128
#define MAXC (MAXN * MAXN)
#define MAXK (2 * MAXN + 8)

static int n, m;                 /* resolution, n-1 */
static int G;                    /* group order */
static int img[8][MAXC];         /* motion images of every cell */
static int orb[MAXC][8];         /* orbit cells of a cell (distinct), sorted */
static int orbsz[MAXC];
static int orbrep[MAXC];         /* min cell of the orbit */

/* direction table: (du, dv) -> index of primitive sign-normalized direction */
static int dtab[(2 * MAXN - 1) * (2 * MAXN - 1)];
static int cnt[(2 * MAXN - 1) * (2 * MAXN - 1)];
static int touched[MAXK];

/* the state */
static int occ[MAXC];
static int plist[MAXK], pos[MAXC], np;
static int rc[MAXN], cc[MAXN];
static long conf;                /* collinear triples in the state */

/* orbits held */
static int reps[MAXK], nreps;    /* canonical reps of orbits in the state */
static int repidx[MAXC];         /* index in reps[] of a rep cell, or -1 */

static double now(void) {
    struct timeval tv; gettimeofday(&tv, NULL);
    return tv.tv_sec + tv.tv_usec * 1e-6;
}

/* xorshift rng */
static unsigned long long rs;
static inline unsigned long long rnd(void) {
    rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs;
}
static inline int rint_(int k) { return (int)(rnd() % (unsigned long long)k); }
static inline double runif(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }

static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }

static void build_dirs(void) {
    int W = 2 * n - 1;
    for (int du = -m; du <= m; du++)
        for (int dv = -m; dv <= m; dv++) {
            int a = du, b = dv;
            if (a == 0 && b == 0) { dtab[(du + m) * W + (dv + m)] = 0; continue; }
            int g = gcd(abs(a), abs(b));
            a /= g; b /= g;
            if (a < 0 || (a == 0 && b < 0)) { a = -a; b = -b; }
            dtab[(du + m) * W + (dv + m)] = (a + m) * W + (b + m);
        }
}

/* motions of saturation.py, in the same order */
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

static int cmpint(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }

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
        int u = c / n, v = c % n;
        for (int i = 0; i < G; i++) {
            int uu, vv; motion(gl[i], u, v, &uu, &vv);
            img[i][c] = uu * n + vv;
        }
        int tmp[8], t = 0;
        for (int i = 0; i < G; i++) {
            int x = img[i][c], dup = 0;
            for (int j = 0; j < t; j++) if (tmp[j] == x) dup = 1;
            if (!dup) tmp[t++] = x;
        }
        qsort(tmp, t, sizeof(int), cmpint);
        orbsz[c] = t;
        for (int j = 0; j < t; j++) orb[c][j] = tmp[j];
        orbrep[c] = tmp[0];
    }
}

/* number of collinear triples {c, q, r} with q, r in the state (q, r != c) */
static long tri_through(int c) {
    int W = 2 * n - 1;
    int u = c / n, v = c % n;
    long t = 0; int nt = 0;
    for (int i = 0; i < np; i++) {
        int q = plist[i];
        if (q == c) continue;
        int d = dtab[(q / n - u + m) * W + (q % n - v + m)];
        int k = cnt[d];
        t += k;
        if (k == 0) touched[nt++] = d;
        cnt[d] = k + 1;
    }
    for (int i = 0; i < nt; i++) cnt[touched[i]] = 0;
    return t;
}

static inline void raw_add(int c) {
    occ[c] = 1; pos[c] = np; plist[np++] = c; rc[c / n]++; cc[c % n]++;
}
static inline void raw_del(int c) {
    int i = pos[c], last = plist[--np];
    plist[i] = last; pos[last] = i; occ[c] = 0; rc[c / n]--; cc[c % n]--;
}
static void add_point(int c) { conf += tri_through(c); raw_add(c); }
static void del_point(int c) { conf -= tri_through(c); raw_del(c); }

/* can orbit of cell r be inserted (cells free, capacities)? tentatively adds; returns 1 or 0 (rolled back) */
static int orbit_fits(int r) {
    int k = orbsz[r];
    for (int j = 0; j < k; j++) {
        int c = orb[r][j];
        if (occ[c] || rc[c / n] >= 2 || cc[c % n] >= 2) {
            for (int i = 0; i < j; i++) raw_del(orb[r][i]);
            return 0;
        }
        raw_add(c);
    }
    for (int j = 0; j < k; j++) raw_del(orb[r][j]);
    return 1;
}

static void insert_orbit(int r) {          /* r = canonical rep; assumes fits */
    for (int j = 0; j < orbsz[r]; j++) add_point(orb[r][j]);
    repidx[r] = nreps; reps[nreps++] = r;
}
static void remove_orbit(int r) {
    for (int j = 0; j < orbsz[r]; j++) del_point(orb[r][j]);
    int i = repidx[r], last = reps[--nreps];
    reps[i] = last; repidx[last] = i; repidx[r] = -1;
}
/* structural-only variants for undo (conf restored by caller) */
static void insert_orbit_raw(int r) {
    for (int j = 0; j < orbsz[r]; j++) raw_add(orb[r][j]);
    repidx[r] = nreps; reps[nreps++] = r;
}
static void remove_orbit_raw(int r) {
    for (int j = 0; j < orbsz[r]; j++) raw_del(orb[r][j]);
    int i = repidx[r], last = reps[--nreps];
    reps[i] = last; repidx[last] = i; repidx[r] = -1;
}

static long full_conf(void) {           /* O(K^3/6) reference: only for asserts */
    long t = 0;
    for (int i = 0; i < np; i++) for (int j = i + 1; j < np; j++) for (int k = j + 1; k < np; k++) {
        int a = plist[i], b = plist[j], c = plist[k];
        long ua = a / n, va = a % n, ub = b / n, vb = b % n, uc = c / n, vc = c % n;
        if ((ub - ua) * (vc - va) == (vb - va) * (uc - ua)) t++;
    }
    return t;
}

static void write_tokens(const char *path) {
    FILE *f = fopen(path, "w");
    if (!f) return;
    int tmp[MAXK];
    for (int i = 0; i < np; i++) tmp[i] = plist[i];
    qsort(tmp, np, sizeof(int), cmpint);
    for (int i = 0; i < np; i++) fprintf(f, "%d%c", tmp[i], i + 1 < np ? ' ' : '\n');
    fclose(f);
}

/* try to add one random orbit anywhere it fits; returns 1 on success */
static int add_random_orbit(int tries) {
    for (int t = 0; t < tries; t++) {
        int c = rint_(n * n);
        int r = orbrep[c];
        if (repidx[r] >= 0) continue;
        if (orbit_fits(r)) { insert_orbit(r); return 1; }
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 9) {
        fprintf(stderr, "usage: sa n K group seed seconds T0 T1 outprefix [grow] [startfile]\n");
        return 2;
    }
    n = atoi(argv[1]); m = n - 1;
    int K = atoi(argv[2]);
    const char *gname = argv[3];
    rs = 0x9E3779B97F4A7C15ULL ^ ((unsigned long long)atoll(argv[4]) * 0x2545F4914F6CDD1DULL + 12345);
    for (int i = 0; i < 20; i++) rnd();
    double seconds = atof(argv[5]);
    double T0 = atof(argv[6]), T1 = atof(argv[7]);
    const char *outprefix = argv[8];
    int grow = argc > 9 ? atoi(argv[9]) : 0;
    const char *startfile = argc > 10 ? argv[10] : NULL;
    if (n > MAXN || K > 2 * n) { fprintf(stderr, "bad n/K\n"); return 2; }

    build_dirs();
    build_group(gname);
    for (int c = 0; c < n * n; c++) repidx[c] = -1;
    np = 0; conf = 0; nreps = 0;

    if (startfile) {
        FILE *f = fopen(startfile, "r");
        if (!f) { fprintf(stderr, "cannot open %s\n", startfile); return 2; }
        int t;
        while (fscanf(f, "%d", &t) == 1) {
            if (t < 0 || t >= n * n) continue;
            int r = orbrep[t];
            if (repidx[r] >= 0) continue;
            if (orbit_fits(r)) insert_orbit(r);
            else fprintf(stderr, "start token %d: orbit does not fit, skipped\n", t);
        }
        fclose(f);
        fprintf(stderr, "start: %d tokens, %ld triples\n", np, conf);
    }
    /* fill to K: random walk — add where possible, else evict a random orbit */
    {
        long guard = 0;
        while (np < K && guard < 50000000L) {
            guard++;
            if (!add_random_orbit(64)) {
                if (nreps > 0) { int r = reps[rint_(nreps)]; remove_orbit(r); }
            }
        }
        if (np < K) fprintf(stderr, "warning: could only place %d of %d tokens initially\n", np, K);
        fprintf(stderr, "initial: %d tokens, %ld triples\n", np, conf);
    }
    if (full_conf() != conf) { fprintf(stderr, "conf mismatch at start\n"); return 3; }

    double t0 = now(), tlast = t0;
    long it = 0, acc = 0;
    long best_conf = conf; int best_np = np;
    int best_lawful = 0;
    char path[512];
    double T = T0;
    long minconf_written = -1;

    for (;;) {
        it++;
        if ((it & 1023) == 0) {
            double el = now() - t0;
            if (el > seconds) break;
            T = T0 * pow(T1 / T0, el / seconds);
            if (now() - tlast > 5.0) {
                tlast = now();
                fprintf(stderr, "[%6.0fs] it=%ld K=%d conf=%ld best_conf=%ld T=%.4f acc=%.3f lawful_best=%d\n",
                        el, it, np, conf, best_conf, T, (double)acc / 1024.0, best_lawful);
                acc = 0;
            }
        }
        /* bookkeeping of lawful states */
        if (conf == 0) {
            if (np > best_lawful) {
                best_lawful = np;
                snprintf(path, sizeof path, "%s_lawful_%d.txt", outprefix, np);
                write_tokens(path);
                fprintf(stderr, "LAWFUL %d tokens -> %s\n", np, path);
                if (np == 2 * n) { fprintf(stderr, "SATURATED n=%d\n", n); printf("SATURATED %s\n", path); fflush(stdout); return 0; }
            }
            if (grow) {
                if (add_random_orbit(1000)) { K = np; best_conf = conf; }
            }
        }
        if (conf < best_conf || (conf == best_conf && np > best_np)) {
            best_conf = conf; best_np = np;
            if (conf < 40 && conf != minconf_written) {
                minconf_written = conf;
                snprintf(path, sizeof path, "%s_minconf.txt", outprefix);
                write_tokens(path);
            }
        }
        if (np < K) add_random_orbit(4);
        if (nreps < 2) continue;

        long before = conf;
        int kind = rint_(3);
        if (kind == 0) {
            /* relocate one orbit to a random cell */
            int i = rint_(nreps), r = reps[i];
            int c = rint_(n * n), r2 = orbrep[c];
            if (r2 == r || repidx[r2] >= 0) continue;
            remove_orbit(r);
            if (!orbit_fits(r2)) { insert_orbit_raw(r); conf = before; continue; }
            insert_orbit(r2);
            long d = conf - before;
            if (d <= 0 || runif() < exp(-d / T)) { acc++; }
            else { remove_orbit_raw(r2); insert_orbit_raw(r); conf = before; }
        } else if (kind == 1) {
            /* swap the column parts of two orbit reps (optionally flipped) */
            int i = rint_(nreps), j = rint_(nreps);
            if (i == j) continue;
            int r1 = reps[i], r2 = reps[j];
            int u1 = r1 / n, v1 = r1 % n, u2 = r2 / n, v2 = r2 % n;
            int f = rint_(4);
            int nv1 = (f & 1) ? m - v2 : v2, nv2 = (f & 2) ? m - v1 : v1;
            int a = orbrep[u1 * n + nv1], b = orbrep[u2 * n + nv2];
            if (a == b || a == r1 || a == r2 || b == r1 || b == r2) continue;
            if (repidx[a] >= 0 || repidx[b] >= 0) continue;
            remove_orbit(r1); remove_orbit(r2);
            if (!orbit_fits(a)) { insert_orbit_raw(r2); insert_orbit_raw(r1); conf = before; continue; }
            insert_orbit(a);
            if (!orbit_fits(b)) { remove_orbit_raw(a); insert_orbit_raw(r2); insert_orbit_raw(r1); conf = before; continue; }
            insert_orbit(b);
            long d = conf - before;
            if (d <= 0 || runif() < exp(-d / T)) { acc++; }
            else { remove_orbit_raw(b); remove_orbit_raw(a); insert_orbit_raw(r2); insert_orbit_raw(r1); conf = before; }
        } else {
            /* flip one orbit: (u,v) -> (u, m-v) or (m-u, v) */
            int i = rint_(nreps), r = reps[i];
            int u = r / n, v = r % n;
            int c = (rnd() & 1) ? u * n + (m - v) : (m - u) * n + v;
            int r2 = orbrep[c];
            if (r2 == r || repidx[r2] >= 0) continue;
            remove_orbit(r);
            if (!orbit_fits(r2)) { insert_orbit_raw(r); conf = before; continue; }
            insert_orbit(r2);
            long d = conf - before;
            if (d <= 0 || runif() < exp(-d / T)) { acc++; }
            else { remove_orbit_raw(r2); insert_orbit_raw(r); conf = before; }
        }
    }
    if (full_conf() != conf) { fprintf(stderr, "conf mismatch at end (%ld vs %ld)\n", full_conf(), conf); return 3; }
    fprintf(stderr, "done: it=%ld K=%d conf=%ld best_conf=%ld lawful_best=%d\n", it, np, conf, best_conf, best_lawful);
    printf("DONE n=%d K=%d best_conf=%ld lawful_best=%d\n", n, np, best_conf, best_lawful);
    return 0;
}
