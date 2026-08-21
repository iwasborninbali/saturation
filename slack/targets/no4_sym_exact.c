/* no4_sym_exact.c — ПОЛНЫЙ перебор конфигураций, неподвижных под циклом (x,y,z)->(y,z,x).
 *
 * Не поиск. Дерево обходится целиком, поэтому ответ «максимум симметричной конфигурации равен K»
 * — утверждение, а не отчёт о неудаче. Это ровно то, чего стохастическому поиску не хватает:
 * его ненаходка не значит ничего, а исчерпанное дерево значит.
 *
 * Отсечения:
 *   1) выбор орбит в возрастающем порядке индекса — каждое множество встречается один раз;
 *   2) верхняя оценка: если уже набрано p, а впереди осталось r орбит, то p + 3r <= best -> в отвал;
 *   3) добавляется только орбита, не создающая ни коллинеарной тройки, ни компланарной четвёрки.
 *
 * Аргументы: n [секунды]   — без времени идёт до конца.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static int n, m;
typedef struct { int x, y, z; } P;
#define MAXORB 1200
static P orb[MAXORB][3]; static int orbsz[MAXORB], norb = 0;
static P pts[64]; static int npts = 0;
static int best = 0; static P bestp[64]; static int bestn = 0;
static long long nodes = 0; static double T = 0; static clock_t st;
static int timedout = 0;

static long long det4(P a, P b, P c, P d) {
    long long ux=b.x-a.x, uy=b.y-a.y, uz=b.z-a.z, vx=c.x-a.x, vy=c.y-a.y, vz=c.z-a.z, wx=d.x-a.x, wy=d.y-a.y, wz=d.z-a.z;
    return ux*(vy*wz-vz*wy) - uy*(vx*wz-vz*wx) + uz*(vx*wy-vy*wx);
}
static int col3(P a, P b, P c) {
    long long ux=b.x-a.x, uy=b.y-a.y, uz=b.z-a.z, vx=c.x-a.x, vy=c.y-a.y, vz=c.z-a.z;
    return (uy*vz-uz*vy)==0 && (uz*vx-ux*vz)==0 && (ux*vy-uy*vx)==0;
}
static int ok_add(int o) {
    int k = orbsz[o], tot = npts + k; P all[64];
    memcpy(all, pts, npts*sizeof(P));
    for (int i=0;i<k;i++) all[npts+i]=orb[o][i];
    for (int a=0;a<tot;a++) for (int b=a+1;b<tot;b++) for (int c=b+1;c<tot;c++) {
        if (c<npts) continue;
        if (col3(all[a],all[b],all[c])) return 0;
    }
    for (int a=0;a<tot;a++) for (int b=a+1;b<tot;b++) for (int c=b+1;c<tot;c++) for (int d=c+1;d<tot;d++) {
        if (d<npts) continue;
        if (det4(all[a],all[b],all[c],all[d])==0) return 0;
    }
    return 1;
}
static void dfs(int start) {
    if (timedout) return;
    if (++nodes % 200000 == 0 && T > 0 && (double)(clock()-st)/CLOCKS_PER_SEC > T) { timedout = 1; return; }
    if (npts > best) { best = npts; bestn = npts; memcpy(bestp, pts, npts*sizeof(P));
        fprintf(stderr, "  новый максимум %d (узлов %lld)\n", best, nodes); }
    for (int o = start; o < norb; o++) {
        if (npts + 3*(norb-o) <= best) return;          /* отсечение по оценке сверху */
        if (!ok_add(o)) continue;
        int save = npts;
        for (int i=0;i<orbsz[o];i++) pts[npts++]=orb[o][i];
        dfs(o+1);
        npts = save;
        if (timedout) return;
    }
}
int main(int argc, char **argv) {
    n = atoi(argv[1]); m = n-1;
    const char *grp = argc>2 ? argv[2] : "cyc3";
    int cyc = strcmp(grp, "cyc3") == 0;
    T = argc>3 ? atof(argv[3]) : 0;
    static int seen[13*13*13]; memset(seen,0,sizeof seen);
    for (int x=0;x<n;x++) for (int y=0;y<n;y++) for (int z=0;z<n;z++) {
        int id=(x*n+y)*n+z; if (seen[id]) continue;
        P p={x,y,z}, cur=p; int k=0;
        do { int cid=(cur.x*n+cur.y)*n+cur.z;
             if (!seen[cid]) { seen[cid]=1; orb[norb][k++]=cur; }
             P q; if (cyc) { q.x=cur.y; q.y=cur.z; q.z=cur.x; } else { q.x=m-cur.x; q.y=m-cur.y; q.z=cur.z; } cur=q;
        } while (!(cur.x==p.x&&cur.y==p.y&&cur.z==p.z) && k<3);
        orbsz[norb]=k; norb++;
    }
    fprintf(stderr, "n=%d группа=%s орбит=%d — полный обход\n", n, grp, norb);
    st = clock(); dfs(0);
    printf("n=%d группа=%s МАКСИМУМ %s %d (узлов %lld)\n", n, grp,
           timedout ? "НЕ ДОКАЗАН, время вышло; найдено" : "= ", best, nodes);
    if (bestn) { char f[256]; snprintf(f,sizeof f,"%s/symexact_%s_n%d.txt", getenv("OUT")?getenv("OUT"):".", grp, n);
        FILE*g=fopen(f,"w"); if(g){ for(int i=0;i<bestn;i++) fprintf(g,"%d %d %d\n",bestp[i].x,bestp[i].y,bestp[i].z); fclose(g);} }
    return 0;
}
