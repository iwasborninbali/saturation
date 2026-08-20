/* no4_estimate.c — оценка размера дерева перебора по Кнуту, ПРЕЖДЕ чем считать всерьёз.
 *
 * Наш собственный протокол оценки стоимости требует мерить, а не надеяться. Здесь оценка
 * несмещённая: от корня идём случайным потомком, домножая накопленный вес на число потомков в
 * каждом узле; сумма весов вдоль пути — несмещённая оценка числа узлов дерева. Усредняем по
 * многим случайным спускам.
 *
 * ОГОВОРКА, которую нельзя опускать: у распределения тяжёлый хвост. Средняя по нескольким сотням
 * спусков занижает, если основная масса дерева сосредоточена в редкой ветви. Поэтому печатаем и
 * медиану, и максимум, и разброс — расхождение между средним и медианой на порядки означает, что
 * оценке нельзя верить, а не что дерево мало.
 *
 *   cc -O3 -o no4_estimate no4_estimate.c && ./no4_estimate n M P0 P1 P2 probes seed
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int n, NC, M;
static int px[512], py[512], pz[512];
static int S[64], sz;
static int blocked[512], linbl[512];
static int lay0[16], lay1[16], lay2[16], P0[16], P1[16], P2[16];
static int kids[512];

static void touch(int p, int d)
{
    for (int i = 0; i < sz; i++) {
        int a = S[i];
        int ux = px[p]-px[a], uy = py[p]-py[a], uz = pz[p]-pz[a];
        for (int q = p+1; q < NC; q++) {
            int vx = px[q]-px[a], vy = py[q]-py[a], vz = pz[q]-pz[a];
            if (uy*vz-uz*vy == 0 && uz*vx-ux*vz == 0 && ux*vy-uy*vx == 0) linbl[q] += d;
        }
    }
    for (int i = 0; i < sz; i++) {
        int a = S[i];
        int ux = px[p]-px[a], uy = py[p]-py[a], uz = pz[p]-pz[a];
        for (int j = i+1; j < sz; j++) {
            int b = S[j];
            int wx = px[b]-px[a], wy = py[b]-py[a], wz = pz[b]-pz[a];
            int nx = uy*wz-uz*wy, ny = uz*wx-ux*wz, nz = ux*wy-uy*wx;
            if (nx == 0 && ny == 0 && nz == 0) continue;
            int rhs = nx*px[a] + ny*py[a] + nz*pz[a];
            for (int q = p+1; q < NC; q++)
                if (nx*px[q] + ny*py[q] + nz*pz[q] == rhs) blocked[q] += d;
        }
    }
}
static int viable(int start)
{
    if (sz + (NC - start) < M) return 0;
    int a0[16], a1[16], a2[16];
    for (int k = 0; k < n; k++) { a0[k]=a1[k]=a2[k]=0; }
    for (int q = start; q < NC; q++) {
        if (blocked[q] || linbl[q]) continue;
        if (lay0[px[q]] >= P0[px[q]] || lay1[py[q]] >= P1[py[q]] || lay2[pz[q]] >= P2[pz[q]]) continue;
        a0[px[q]]++; a1[py[q]]++; a2[pz[q]]++;
    }
    int b0=0,b1=0,b2=0;
    for (int k = 0; k < n; k++) {
        int c0=P0[k]-lay0[k], c1=P1[k]-lay1[k], c2=P2[k]-lay2[k];
        b0 += a0[k]<c0?a0[k]:c0; b1 += a1[k]<c1?a1[k]:c1; b2 += a2[k]<c2?a2[k]:c2;
    }
    int bd = b0<b1?b0:b1; if (b2<bd) bd=b2;
    return sz + bd >= M;
}
int main(int argc, char **argv)
{
    n = atoi(argv[1]); M = atoi(argv[2]);
    { char *t = strtok(argv[3], ","); for (int i=0;i<n;i++){P0[i]=atoi(t); t=strtok(NULL,",");} }
    { char *t = strtok(argv[4], ","); for (int i=0;i<n;i++){P1[i]=atoi(t); t=strtok(NULL,",");} }
    { char *t = strtok(argv[5], ","); for (int i=0;i<n;i++){P2[i]=atoi(t); t=strtok(NULL,",");} }
    long probes = atol(argv[6]); srandom(argc>7?atoi(argv[7]):1);
    NC=0; for(int x=0;x<n;x++)for(int y=0;y<n;y++)for(int z=0;z<n;z++){px[NC]=x;py[NC]=y;pz[NC]=z;NC++;}
    double *est = malloc(probes*sizeof(double));
    for (long t = 0; t < probes; t++) {
        memset(blocked,0,sizeof blocked); memset(linbl,0,sizeof linbl);
        memset(lay0,0,sizeof lay0); memset(lay1,0,sizeof lay1); memset(lay2,0,sizeof lay2);
        sz = 0;
        double D = 1.0, tot = 1.0;
        int start = 0;
        while (sz < M) {
            int nk = 0;
            for (int q = start; q < NC; q++) {
                if (blocked[q] || linbl[q]) continue;
                if (lay0[px[q]] >= P0[px[q]] || lay1[py[q]] >= P1[py[q]] || lay2[pz[q]] >= P2[pz[q]]) continue;
                touch(q,+1); S[sz++]=q; lay0[px[q]]++; lay1[py[q]]++; lay2[pz[q]]++;
                int ok = viable(q+1);
                sz--; lay0[px[q]]--; lay1[py[q]]--; lay2[pz[q]]--; touch(q,-1);
                if (ok) kids[nk++] = q;
            }
            if (nk == 0) break;
            D *= nk; tot += D;
            int pick = kids[random() % nk];
            touch(pick,+1); S[sz++]=pick; lay0[px[pick]]++; lay1[py[pick]]++; lay2[pz[pick]]++;
            start = pick + 1;
        }
        est[t] = tot;
    }
    double sum=0, mx=0; for(long t=0;t<probes;t++){sum+=est[t]; if(est[t]>mx)mx=est[t];}
    for(long i=0;i<probes;i++)for(long j=i+1;j<probes;j++) if(est[j]<est[i]){double s=est[i];est[i]=est[j];est[j]=s;}
    printf("узлов: среднее %.3g, медиана %.3g, максимум %.3g (спусков %ld)\n",
           sum/probes, est[probes/2], mx, probes);
    printf("ОГОВОРКА: если среднее и медиана расходятся на порядки, оценке верить нельзя — "
           "дерево сосредоточено в редкой ветви, и средняя её недобирает.\n");
    return 0;
}
