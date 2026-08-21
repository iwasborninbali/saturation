/* no4_curve.c — подъём моментной кривой: n = p*k, и почти все четвёрки становятся БЕСПЛАТНЫМИ.
 *
 * Кривая (t, t^2, t^3) mod p даёт p точек без четырёх компланарных: определитель четвёрки сравним
 * с определителем Вандермонда, а тот не ноль при различных t. Это теорема, не находка.
 *
 * Продолжение. Возьмём n = p*k и в каждом классе вычетов t поднимем точку многими способами:
 *     точка = (t mod p, t^2 mod p, t^3 mod p) + p*(x, y, z),   (x,y,z) из [k]^3
 * Подъём НЕ меняет вычетов, поэтому определитель любых четырёх точек с ЧЕТЫРЬМЯ РАЗНЫМИ t
 * по-прежнему сравним с Вандермондом и по-прежнему не ноль. Такие четвёрки проверять не нужно —
 * они запрещены быть компланарными самим модулем.
 *
 * Остаются только четвёрки, где какое-то t повторяется. Их несравнимо меньше, и лишь они считаются.
 * Пространство поиска падает с n^3 = p^3*k^3 до p*k^3 — в p^2 раз.
 *
 * Аргументы: p k секунды семя выход
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
typedef struct { int x,y,z,t; } Q;
static Q cand[8000]; static int ncand; static int n;
static Q S[128]; static int k_;
static Q best[128]; static int bk=0;
static long long det4(Q a,Q b,Q c,Q d){long long ux=b.x-a.x,uy=b.y-a.y,uz=b.z-a.z,vx=c.x-a.x,vy=c.y-a.y,vz=c.z-a.z,wx=d.x-a.x,wy=d.y-a.y,wz=d.z-a.z;return ux*(vy*wz-vz*wy)-uy*(vx*wz-vz*wx)+uz*(vx*wy-vy*wx);}
static int col3(Q a,Q b,Q c){long long ux=b.x-a.x,uy=b.y-a.y,uz=b.z-a.z,vx=c.x-a.x,vy=c.y-a.y,vz=c.z-a.z;return (uy*vz-uz*vy)==0&&(uz*vx-ux*vz)==0&&(ux*vy-uy*vx)==0;}
static int ok(Q q){
    for(int i=0;i<k_;i++) if(S[i].x==q.x&&S[i].y==q.y&&S[i].z==q.z) return 0;
    for(int a=0;a<k_;a++) for(int b=a+1;b<k_;b++) if(col3(S[a],S[b],q)) return 0;
    for(int a=0;a<k_;a++) for(int b=a+1;b<k_;b++) for(int c=b+1;c<k_;c++){
        /* четыре РАЗНЫХ вычета -> определитель сравним с вандермондовым, проверять нечего */
        if(S[a].t!=S[b].t && S[a].t!=S[c].t && S[a].t!=q.t && S[b].t!=S[c].t && S[b].t!=q.t && S[c].t!=q.t) continue;
        if(det4(S[a],S[b],S[c],q)==0) return 0; }
    return 1;
}
int main(int argc,char**argv){
    int p=atoi(argv[1]), k=atoi(argv[2]); double T=atof(argv[3]);
    unsigned sd=(unsigned)atoi(argv[4]); const char*out=argv[5];
    n=p*k; srand(sd);
    if((long)p*k*k*k>8000){fprintf(stderr,"ОТКАЗ: p*k^3=%ld не помещается\n",(long)p*k*k*k);return 2;}
    ncand=0;
    for(int t=0;t<p;t++){
        int bx=t%p, by=(t*t)%p, bz=(int)(((long)t*t%p)*t%p);
        for(int x=0;x<k;x++)for(int y=0;y<k;y++)for(int z=0;z<k;z++){
            cand[ncand].x=bx+p*x; cand[ncand].y=by+p*y; cand[ncand].z=bz+p*z; cand[ncand].t=t; ncand++; }
    }
    fprintf(stderr,"p=%d k=%d n=%d кандидатов %d (вместо n^3=%d, в %d раз меньше)\n",p,k,n,ncand,n*n*n,(n*n*n)/ncand);
    int ord[8000]; clock_t st=clock(); long rs=0;
    while((double)(clock()-st)/CLOCKS_PER_SEC<T){
        rs++; k_=0;
        for(int i=0;i<ncand;i++)ord[i]=i;
        for(int i=ncand-1;i>0;i--){int j=rand()%(i+1);int t=ord[i];ord[i]=ord[j];ord[j]=t;}
        for(int i=0;i<ncand;i++) if(ok(cand[ord[i]])) S[k_++]=cand[ord[i]];
        for(int it=0;it<2000;it++){
            if((double)(clock()-st)/CLOCKS_PER_SEC>T) break;
            if(k_>bk){bk=k_;memcpy(best,S,k_*sizeof(Q));fprintf(stderr,"  %d точек (перезапуск %ld)\n",bk,rs);fflush(stderr);
                if(out){FILE*g=fopen(out,"w");if(g){for(int i=0;i<bk;i++)fprintf(g,"%d %d %d\n",best[i].x,best[i].y,best[i].z);fclose(g);}}}
            int kick=1+rand()%3;
            for(int q=0;q<kick&&k_>0;q++){int i=rand()%k_;S[i]=S[--k_];}
            for(int i=ncand-1;i>0;i--){int j=rand()%(i+1);int t=ord[i];ord[i]=ord[j];ord[j]=t;}
            for(int i=0;i<ncand;i++) if(ok(cand[ord[i]])) S[k_++]=cand[ord[i]];
        }
        if(k_>bk){bk=k_;memcpy(best,S,k_*sizeof(Q));}
    }
    fprintf(stderr,"итог %d точек при n=%d, перезапусков %ld\n",bk,n,rs);
    if(out){FILE*g=fopen(out,"w");if(g){for(int i=0;i<bk;i++)fprintf(g,"%d %d %d\n",best[i].x,best[i].y,best[i].z);fclose(g);}}
    return 0;
}
