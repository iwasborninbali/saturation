/* no4_sym_proof.c — ДОКАЗАТЕЛЬСТВО симметричного максимума, а не поиск.
 *
 * Отличие от первой версии обхода в двух вещах, и обе решающие:
 *   1) вниз передаётся список ещё ЖИВЫХ орбит (совместимых с текущим набором), а не индекс начала.
 *      Оценка сверху становится npts + 3*|живых| вместо npts + 3*|оставшихся| — на порядки туже,
 *      потому что после десятка точек живых остаются единицы.
 *   2) планка best задаётся снаружи известной находкой. Тогда обход не ищет её заново, а проверяет
 *      только ветви, способные её ПРЕВЗОЙТИ. Исчерпание такого дерева означает: больше нет.
 *
 * Аргументы: n планка [секунды]
 * Исход: «МАКСИМУМ <= планка, дерево исчерпано» — это утверждение. «время вышло» — это ничто.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static int n,m; typedef struct{int x,y,z;} P;
#define MAXORB 9000
static P orb[MAXORB][3]; static int orbsz[MAXORB], norb=0;
static P pts[64]; static int npts=0;
static int best; static P bestp[64]; static int bestn=0;
static long long nodes=0; static double T; static clock_t st; static int timedout=0;
static int shard=-1, nshard=1, depth0=0;
static long long det4(P a,P b,P c,P d){long long ux=b.x-a.x,uy=b.y-a.y,uz=b.z-a.z,vx=c.x-a.x,vy=c.y-a.y,vz=c.z-a.z,wx=d.x-a.x,wy=d.y-a.y,wz=d.z-a.z;return ux*(vy*wz-vz*wy)-uy*(vx*wz-vz*wx)+uz*(vx*wy-vy*wx);}
static int col3(P a,P b,P c){long long ux=b.x-a.x,uy=b.y-a.y,uz=b.z-a.z,vx=c.x-a.x,vy=c.y-a.y,vz=c.z-a.z;return (uy*vz-uz*vy)==0&&(uz*vx-ux*vz)==0&&(ux*vy-uy*vx)==0;}
/* совместима ли орбита o с текущим набором */
static int ok_add(int o){
    int k=orbsz[o], tot=npts+k; P all[64];
    memcpy(all,pts,npts*sizeof(P));
    for(int i=0;i<k;i++) all[npts+i]=orb[o][i];
    for(int a=0;a<tot;a++)for(int b=a+1;b<tot;b++)for(int c=b+1;c<tot;c++){
        if(c<npts) continue; if(col3(all[a],all[b],all[c])) return 0; }
    for(int a=0;a<tot;a++)for(int b=a+1;b<tot;b++)for(int c=b+1;c<tot;c++)for(int d=c+1;d<tot;d++){
        if(d<npts) continue; if(det4(all[a],all[b],all[c],all[d])==0) return 0; }
    return 1;
}

/* ——— ёмкость: законное отсечение, не эвристика ———
 * В каждой осевой плоскости не более трёх точек: четыре точки одного слоя лежат в его плоскости.
 * Значит из слоя можно добавить не больше min(3 - занято, живых_в_слое), а всего по оси — сумму
 * этого по слоям. Три оси дают три независимые оценки сверху, берём наименьшую.
 * Если набрано + ёмкость <= планки, ветка не может её превзойти и срезается ДОКАЗУЕМО.
 * Идея второго солвера, в двумерии дала от 6.7 до 76 крат; здесь мерится впервые. */
static int capacity(int *live, int nlive) {
    int occ[3][32], liv[3][32];
    memset(occ, 0, sizeof occ); memset(liv, 0, sizeof liv);
    for (int i = 0; i < npts; i++) { occ[0][pts[i].x]++; occ[1][pts[i].y]++; occ[2][pts[i].z]++; }
    for (int i = 0; i < nlive; i++) { int o = live[i];
        for (int t = 0; t < orbsz[o]; t++) { liv[0][orb[o][t].x]++; liv[1][orb[o][t].y]++; liv[2][orb[o][t].z]++; } }
    int cap = 1 << 30;
    for (int a = 0; a < 3; a++) {
        int c = 0;
        for (int L = 0; L < n; L++) {
            int room = 3 - occ[a][L]; if (room < 0) room = 0;
            c += room < liv[a][L] ? room : liv[a][L];
        }
        if (c < cap) cap = c;
    }
    return cap;
}

static void dfs(int *live,int nlive){
    if(timedout) return;
    if((++nodes & 0xFFFF)==0 && T>0 && (double)(clock()-st)/CLOCKS_PER_SEC>T){timedout=1;return;}
    if(npts>best){best=npts;bestn=npts;memcpy(bestp,pts,npts*sizeof(P));
        fprintf(stderr,"  ПРЕВЗОЙДЕНА ПЛАНКА: %d (узлов %lld)\n",best,nodes);}
    int sum=0; for(int i=0;i<nlive;i++) sum+=orbsz[live[i]];
    if(npts+sum<=best) return;                       /* оценка по живым */
    if(npts+capacity(live,nlive)<=best) return;      /* оценка по ёмкости — туже */
    for(int i=0;i<nlive;i++){
        if(depth0==0 && shard>=0 && (i%nshard)!=shard) continue;
        int rem=0; for(int t=i;t<nlive;t++) rem+=orbsz[live[t]];
        if(npts+rem<=best) return;
        int o=live[i];
        if(!ok_add(o)) continue;
        int save=npts;
        for(int t=0;t<orbsz[o];t++) pts[npts++]=orb[o][t];
        depth0++;
        int *nl=malloc(sizeof(int)*(nlive-i)); int nn=0;
        for(int t=i+1;t<nlive;t++) if(ok_add(live[t])) nl[nn++]=live[t];
        dfs(nl,nn); free(nl);
        depth0--;
        npts=save;
        if(timedout) return;
    }
}
int main(int argc,char**argv){
    n=atoi(argv[1]);
    if(argc>5){shard=atoi(argv[4]); nshard=atoi(argv[5]);} m=n-1; best=atoi(argv[2]); T=argc>3?atof(argv[3]):0;
    if (n > 31 || (long)n*n*n > 27000 || (long)n*n*n/3 + n > 9000) {
        fprintf(stderr, "ОТКАЗ: n=%d не помещается в статические массивы. Молча портить память нельзя.\n", n);
        return 2; }
    static int seen[27000]; memset(seen,0,sizeof seen);
    for(int x=0;x<n;x++)for(int y=0;y<n;y++)for(int z=0;z<n;z++){
        int id=(x*n+y)*n+z; if(seen[id])continue;
        P p={x,y,z},cur=p; int k=0;
        do{ int cid=(cur.x*n+cur.y)*n+cur.z;
            if(!seen[cid]){seen[cid]=1;orb[norb][k++]=cur;}
            P q={cur.y,cur.z,cur.x}; cur=q;
        }while(!(cur.x==p.x&&cur.y==p.y&&cur.z==p.z)&&k<3);
        orbsz[norb]=k; norb++; }
    fprintf(stderr,"n=%d орбит=%d планка=%d\n",n,norb,best);
    int *live=malloc(sizeof(int)*norb); for(int i=0;i<norb;i++) live[i]=i;
    st=clock(); dfs(live,norb);
    if(timedout) printf("n=%d доля %d/%d ВРЕМЯ ВЫШЛО — ничего не доказано (узлов %lld, лучшее %d)\n",n,shard,nshard,nodes,best);
    else printf("n=%d доля %d/%d ДЕРЕВО ИСЧЕРПАНО: симметричный максимум = %d (узлов %lld)\n",n,shard,nshard,best,nodes);
    if(bestn){char f[256];snprintf(f,sizeof f,"%s/proof_n%d.txt",getenv("OUT")?getenv("OUT"):".",n);
        FILE*g=fopen(f,"w"); if(g){for(int i=0;i<bestn;i++)fprintf(g,"%d %d %d\n",bestp[i].x,bestp[i].y,bestp[i].z);fclose(g);} }
    return 0;
}
