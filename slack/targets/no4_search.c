/* no4_search.c — независимый стохастический поиск конфигураций без четырёх компланарных в [n]^3.
 *
 * Пишется как ПОПЫТКА ОПРОВЕРЖЕНИЯ: второй солвер получил невыполнимость при M=18, n=7, и просит
 * поискать 18 точек другим способом. Здесь нет ни SAT, ни списка плоскостей — только определитель
 * на четвёрке точек. Общего с проверяемым доказательством ровно ноль, кроме самой задачи.
 *
 * Важное следствие, которым пользуемся: если три точки набора коллинеарны, то ЛЮБАЯ четвёртая
 * компланарна с ними (плоскость через прямую и точку). Значит при |S| >= 4 набор без четырёх
 * компланарных автоматически без трёх коллинеарных, и добавляемая точка не должна лежать ни на
 * одной прямой через две выбранные.
 *
 * Метод: итерированный локальный поиск. Жадно доращиваем случайным порядком до максимального,
 * затем выбиваем 1..3 случайные точки и доращиваем снова, принимая неухудшающее. Найденное
 * записывается в файл В МОМЕНТ НАХОДКИ.
 *
 *   cc -O2 -o no4_search no4_search.c && ./no4_search n target seconds seed out.txt
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static int n, NC, target;
static int px[2048], py[2048], pz[2048];   /* 2048 = запас до n=12; при n=9 клеток 729, а прежние 512 давали ПЕРЕПОЛНЕНИЕ и мусорный ответ */
static int S[128], sz;
static int bestS[128], bestSz = 0;
static char *outpath;

static inline int det3(int ax,int ay,int az,int bx,int by,int bz,int cx,int cy,int cz){
    return ax*(by*cz-bz*cy) - ay*(bx*cz-bz*cx) + az*(bx*cy-by*cx);
}
/* можно ли добавить точку q: ни одна тройка выбранных вместе с q не компланарна,
   и q не коллинеарна ни с какой парой выбранных */
static int ok_add(int q){
    for(int i=0;i<sz;i++){
        int a=S[i];
        for(int j=i+1;j<sz;j++){
            int b=S[j];
            /* коллинеарность q,a,b -> запрещено (тогда любая четвёртая компланарна) */
            int ux=px[b]-px[a], uy=py[b]-py[a], uz=pz[b]-pz[a];
            int vx=px[q]-px[a], vy=py[q]-py[a], vz=pz[q]-pz[a];
            if(uy*vz-uz*vy==0 && uz*vx-ux*vz==0 && ux*vy-uy*vx==0) return 0;
            for(int k=j+1;k<sz;k++){
                int c=S[k];
                int wx=px[c]-px[a], wy=py[c]-py[a], wz=pz[c]-pz[a];
                if(det3(ux,uy,uz,wx,wy,wz,vx,vy,vz)==0) return 0;
            }
        }
    }
    return 1;
}
static void save(void){
    FILE*f=fopen(outpath,"w");
    fprintf(f,"# A280537 no-four-coplanar, n=%d, points=%d (independent stochastic search, no SAT)\n",n,bestSz);
    fprintf(f,"# verified in place by determinants over every quadruple of the set\n");
    for(int i=0;i<bestSz;i++) fprintf(f,"%d %d %d\n",px[bestS[i]],py[bestS[i]],pz[bestS[i]]);
    fclose(f);
}
/* полная перепроверка сохраняемого набора: все четвёрки */
static int recheck(void){
    int bad=0;
    for(int i=0;i<bestSz;i++)for(int j=i+1;j<bestSz;j++)for(int k=j+1;k<bestSz;k++)for(int l=k+1;l<bestSz;l++){
        int a=bestS[i],b=bestS[j],c=bestS[k],d=bestS[l];
        int ux=px[b]-px[a],uy=py[b]-py[a],uz=pz[b]-pz[a];
        int vx=px[c]-px[a],vy=py[c]-py[a],vz=pz[c]-pz[a];
        int wx=px[d]-px[a],wy=py[d]-py[a],wz=pz[d]-pz[a];
        if(det3(ux,uy,uz,vx,vy,vz,wx,wy,wz)==0) bad++;
    }
    return bad;
}
static void grow(int *perm){
    for(int t=0;t<NC;t++){ int q=perm[t]; int in=0;
        for(int i=0;i<sz;i++) if(S[i]==q){in=1;break;}
        if(in) continue;
        if(ok_add(q)) S[sz++]=q;
    }
}
int main(int argc,char**argv){
    n=atoi(argv[1]); target=atoi(argv[2]);
    double T=atof(argv[3]); unsigned seed=(unsigned)atoi(argv[4]); outpath=argv[5];
    NC=0; for(int x=0;x<n;x++)for(int y=0;y<n;y++)for(int z=0;z<n;z++){px[NC]=x;py[NC]=y;pz[NC]=z;NC++;}
    srandom(seed);
    int *perm=malloc(NC*sizeof(int));
    clock_t t0=clock(); long restarts=0, iters=0;
    while((double)(clock()-t0)/CLOCKS_PER_SEC < T){
        for(int i=0;i<NC;i++) perm[i]=i;
        for(int i=NC-1;i>0;i--){int j=random()%(i+1);int t=perm[i];perm[i]=perm[j];perm[j]=t;}
        sz=0; grow(perm); restarts++;
        for(int it=0; it<4000 && (double)(clock()-t0)/CLOCKS_PER_SEC < T; it++){
            iters++;
            if(sz>bestSz){ bestSz=sz; memcpy(bestS,S,sz*sizeof(int)); int bad=recheck();
                printf("  %d точек (перепроверка: компланарных четвёрок %d) после %ld рестартов\n",bestSz,bad,restarts);
                fflush(stdout); if(bad==0) save();
                if(bestSz>=target){ printf("ЦЕЛЬ %d ДОСТИГНУТА\n",target); return 0; } }
            int r=1+random()%3; int keep=sz-r; if(keep<0) keep=0;
            for(int i=sz-1;i>=keep;i--){ int j=random()%(i+1); int t=S[i]; S[i]=S[j]; S[j]=t; }
            sz=keep;
            for(int i=NC-1;i>0;i--){int j=random()%(i+1);int t=perm[i];perm[i]=perm[j];perm[j]=t;}
            grow(perm);
        }
    }
    printf("n=%d: лучшее найденное %d за %.0fс (%ld рестартов, %ld итераций); цель %d НЕ достигнута — "
           "это «не нашёл», а не «не существует»\n",n,bestSz,T,restarts,iters,target);
    return 0;
}
