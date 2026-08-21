/* exact3d.c — ИСЧЕРПЫВАЮЩИЙ поиск в кубе [n]^3 без четырёх компланарных,
 * с законным отсечением по ЁМКОСТИ.
 *
 * ЗАЧЕМ. Вопрос «есть ли 19 точек при n=7» перебором плоскостей закрыт на 79.6% и снят
 * по бюджету: остатку требовалось около шестидесяти часов. В двумерии то же отсечение
 * по ёмкости сократило исчерпывающее дерево в 26-76 раз. Проверяем, хватит ли этого здесь.
 *
 * ЁМКОСТЬ. В каждой осевой плоскости не более 3 точек: четвёртая была бы компланарна.
 * Значит из живых клеток слоя возьмёшь не больше min(3 - занято, живых в слое). Сумма
 * по слоям — граница сверху на добавимое; так по каждой из трёх осей, берём наименьшую.
 * Ветка с k + ёмкость < цель мертва ДОКАЗУЕМО — ни одна достижимая не срезается.
 *
 * СМЕРТЬ. Две точки убивают свою прямую (третья на ней дала бы три коллинеарных, а с любой
 * четвёртой — компланарную четвёрку). Три невыровненные убивают свою плоскость.
 *
 * СБОРКА: cc -O3 -march=native -o exact3d exact3d.c
 * ЗАПУСК: ./exact3d <n> <цель> <отсечение 0|1> [секунд]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXW 16
typedef struct { unsigned long long w[MAXW]; } BS;
static int N,NN,NW,TARGET,PRUNE;
static signed char *PX,*PY,*PZ;
static int chosen[64];
static int slab[3][64];                 /* сколько выбрано в каждом слое по каждой оси */
static long long nodes=0; static int best=0;
static double LIMIT; static struct timespec T0; static int stopped=0;

static inline void bs_set(BS*a,int i){ a->w[i>>6]|=1ULL<<(i&63); }
static inline void bs_clr(BS*a,int i){ a->w[i>>6]&=~(1ULL<<(i&63)); }
static inline int  bs_get(const BS*a,int i){ return (a->w[i>>6]>>(i&63))&1ULL; }
static inline int  bs_pop(const BS*a){int s=0;for(int t=0;t<NW;t++)s+=__builtin_popcountll(a->w[t]);return s;}
static inline int idx(int x,int y,int z){ return (x*N+y)*N+z; }
static int gcd_(int a,int b){a=a<0?-a:a;b=b<0?-b:b;while(b){int t=a%b;a=b;b=t;}return a?a:1;}

static double elapsed(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t);
    return (t.tv_sec-T0.tv_sec)+1e-9*(t.tv_nsec-T0.tv_nsec); }

static void kill_line(BS*s,int i,int j){
    int dx=PX[j]-PX[i],dy=PY[j]-PY[i],dz=PZ[j]-PZ[i];
    int g=gcd_(gcd_(dx,dy),dz); dx/=g;dy/=g;dz/=g;
    for(int d=-1;d<=1;d+=2){
        int x=PX[i],y=PY[i],z=PZ[i];
        while(1){ x+=d*dx;y+=d*dy;z+=d*dz;
            if(x<0||y<0||z<0||x>=N||y>=N||z>=N) break; bs_clr(s,idx(x,y,z)); }
    }
    bs_clr(s,i); bs_clr(s,j);
}
static void kill_plane(BS*s,int i,int a,int b){
    long long ux=PX[a]-PX[i],uy=PY[a]-PY[i],uz=PZ[a]-PZ[i];
    long long vx=PX[b]-PX[i],vy=PY[b]-PY[i],vz=PZ[b]-PZ[i];
    long long nx=uy*vz-uz*vy, ny=uz*vx-ux*vz, nz=ux*vy-uy*vx;
    if(!nx&&!ny&&!nz) return;
    long long d=nx*PX[i]+ny*PY[i]+nz*PZ[i];
    for(int x=0;x<N;x++)for(int y=0;y<N;y++){
        long long r=d-nx*x-ny*y;
        if(nz){ if(r%nz) continue; long long z=r/nz; if(z<0||z>=N) continue; bs_clr(s,idx(x,y,(int)z)); }
        else { if(r!=0) continue; for(int z=0;z<N;z++) bs_clr(s,idx(x,y,z)); }
    }
}
static int capacity(const BS*alive){
    int c[3][64];
    for(int o=0;o<3;o++) for(int t=0;t<N;t++) c[o][t]=0;
    for(int w=0;w<NW;w++){
        unsigned long long a=alive->w[w];
        while(a){ int b=__builtin_ctzll(a); a&=a-1; int i=(w<<6)+b;
            c[0][PX[i]]++; c[1][PY[i]]++; c[2][PZ[i]]++; }
    }
    int m=1<<30;
    for(int o=0;o<3;o++){
        int s=0;
        for(int t=0;t<N;t++){ int мест=3-slab[o][t]; if(мест<0)мест=0;
            s += c[o][t]<мест?c[o][t]:мест; }
        if(s<m) m=s;
    }
    return m;
}
static void dfs(int start,int k,BS alive){
    if(stopped) return;
    nodes++;
    if((nodes&0xFFFFF)==0 && elapsed()>LIMIT){ stopped=1; return; }
    if(k>best) best=k;
    if(k>=TARGET) return;
    int запас = PRUNE ? capacity(&alive) : bs_pop(&alive);
    if(k+запас < TARGET) return;
    for(int c=start;c<NN;c++){
        if(!bs_get(&alive,c)) continue;
        BS na=alive;
        for(int t=0;t<=c;t++) bs_clr(&na,t);
        for(int t=0;t<k;t++) kill_line(&na,c,chosen[t]);
        for(int a=0;a<k;a++) for(int b=a+1;b<k;b++) kill_plane(&na,c,chosen[a],chosen[b]);
        chosen[k]=c; slab[0][PX[c]]++; slab[1][PY[c]]++; slab[2][PZ[c]]++;
        dfs(c+1,k+1,na);
        slab[0][PX[c]]--; slab[1][PY[c]]--; slab[2][PZ[c]]--;
        if(stopped) return;
    }
}
int main(int argc,char**argv){
    if(argc<4){ fprintf(stderr,"usage: exact3d <n> <цель> <отсечение 0|1> [секунд]\n"); return 2; }
    int n=atoi(argv[1]); TARGET=atoi(argv[2]); PRUNE=atoi(argv[3]);
    LIMIT=(argc>4)?atof(argv[4]):1e18;
    N=n; NN=n*n*n; NW=(NN+63)/64;
    if(NW>MAXW){ fprintf(stderr,"n слишком велик\n"); return 2; }
    PX=malloc(NN);PY=malloc(NN);PZ=malloc(NN);
    { int t=0; for(int x=0;x<n;x++)for(int y=0;y<n;y++)for(int z=0;z<n;z++){PX[t]=x;PY[t]=y;PZ[t]=z;t++;} }
    for(int o=0;o<3;o++) for(int t=0;t<N;t++) slab[o][t]=0;
    BS alive; memset(&alive,0,sizeof alive);
    for(int i=0;i<NN;i++) bs_set(&alive,i);
    clock_gettime(CLOCK_MONOTONIC,&T0);
    dfs(0,0,alive);
    printf("n=%d цель=%d отсечение=%s: %s достигнуто %d, узлов %lld, %.2fс\n",
           n,TARGET,PRUNE?"ЁМКОСТЬ":"живые",
           stopped?"ОБОРВАНО ПО ВРЕМЕНИ —":"ИСЧЕРПАНО —", best, nodes, elapsed());
    return 0;
}
