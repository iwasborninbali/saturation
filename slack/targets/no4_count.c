/* no4_count.c — ИСЧЕРПЫВАЮЩИЙ подсчёт всех конфигураций заданного размера без четырёх компланарных.
 *
 * Нужен не ради максимума, а ради ЧИСЛА решений: совпадение количества с независимо опубликованным
 * (Э. Пегг, 2014) — проверка несравненно более сильная, чем совпадение максимума. Максимум может
 * сойтись случайно у двух программ с одинаковой ошибкой; количество решений — почти нет.
 *
 * Пруны: (1) в каждом осевом слое не более 3 точек — слой есть плоскость;
 *        (2) три коллинеарные точки запрещены вовсе (любая четвёртая с ними компланарна);
 *        (3) остаток решётки не покрывает недобор.
 *
 *   cc -O2 -o no4_count no4_count.c && ./no4_count n M [dumpfile]
 */
#include <stdio.h>
#include <stdlib.h>

static int n, NC, M;
static int px[512],py[512],pz[512];
static int S[64], sz;
static long long found=0, nodes=0;
static int lay[3][16];
static FILE *dump=NULL;

static inline int det3(int ax,int ay,int az,int bx,int by,int bz,int cx,int cy,int cz){
    return ax*(by*cz-bz*cy)-ay*(bx*cz-bz*cx)+az*(bx*cy-by*cx);
}
static int ok_add(int q){
    for(int i=0;i<sz;i++){int a=S[i];
        int vx=px[q]-px[a],vy=py[q]-py[a],vz=pz[q]-pz[a];
        for(int j=i+1;j<sz;j++){int b=S[j];
            int ux=px[b]-px[a],uy=py[b]-py[a],uz=pz[b]-pz[a];
            if(uy*vz-uz*vy==0&&uz*vx-ux*vz==0&&ux*vy-uy*vx==0) return 0;
            for(int k=j+1;k<sz;k++){int c=S[k];
                int wx=px[c]-px[a],wy=py[c]-py[a],wz=pz[c]-pz[a];
                if(det3(ux,uy,uz,wx,wy,wz,vx,vy,vz)==0) return 0;}}}
    return 1;
}
static void rec(int start){
    nodes++;
    if(sz==M){ found++;
        if(dump){ for(int i=0;i<sz;i++) fprintf(dump,"%d %d %d%s",px[S[i]],py[S[i]],pz[S[i]], i+1<sz?" ":"\n"); }
        return; }
    if(sz + (NC-start) < M) return;
    for(int q=start;q<NC;q++){
        if(sz + (NC-q) < M) return;
        if(lay[0][px[q]]>=3||lay[1][py[q]]>=3||lay[2][pz[q]]>=3) continue;
        if(!ok_add(q)) continue;
        S[sz++]=q; lay[0][px[q]]++; lay[1][py[q]]++; lay[2][pz[q]]++;
        rec(q+1);
        sz--; lay[0][px[q]]--; lay[1][py[q]]--; lay[2][pz[q]]--;
    }
}
int main(int argc,char**argv){
    n=atoi(argv[1]); M=atoi(argv[2]);
    if(argc>3) dump=fopen(argv[3],"w");
    NC=0; for(int x=0;x<n;x++)for(int y=0;y<n;y++)for(int z=0;z<n;z++){px[NC]=x;py[NC]=y;pz[NC]=z;NC++;}
    rec(0);
    printf("n=%d M=%d: помеченных конфигураций %lld (узлов %lld)\n",n,M,found,nodes);
    if(dump) fclose(dump);
    return 0;
}
