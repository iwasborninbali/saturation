/* equal_effort.c — поиск с РАВНЫМ бюджетом времени, БЕЗ ЦЕЛИ.
 *
 * ЗАЧЕМ. Отношение a(n)/n по нашим нижним границам падает: 2.56, 2.60, 2.55, 2.42, 2.38,
 * 2.36, 2.33, 2.19. Это читается как ответ («предел ниже трёх»), но почти наверняка это
 * след НАС: большие n искались меньше. Мы уже дважды попадались ровно на этом.
 * Отмывка одна: дать КАЖДОМУ n одинаковое время на одинаковом ядре и посмотреть, останется
 * ли кривая падающей. Останется — свойство задачи. Выпрямится — было свойство усилий.
 *
 * ЦЕЛИ НЕТ НАМЕРЕННО. У напарника цель оказалась условием остановки: `if (best >= target) break`,
 * то есть предсказание печатало само себя. Здесь останавливает только часы. Вопрос не
 * «достижимо ли K», а «сколько выйдет за отведённое» — такой вопрос ожиданием не загрязнить.
 *
 * ПОЧЕМУ БЕЗ ПРЕДПОСЧЁТА МАСОК. witness3d держал killp[N][N] битсетов: при n=16 это 8.6 ГБ.
 * Здесь прямая через две точки проходится НА ХОДУ за O(n) шагов, память O(n^3).
 *
 * ПРАВИЛА (обе — «смерть»): две выбранные точки убивают всю свою прямую (третья на ней дала бы
 * три коллинеарных, а с любой четвёртой — компланарную четвёрку); три невыровненные убивают
 * свою плоскость.
 *
 * СБОРКА: cc -O3 -march=native -o equal_effort equal_effort.c
 * ЗАПУСК: ./equal_effort <n> <секунд> [выборка] [семя]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXW 64                      /* 64*64 = 4096 клеток, значит n <= 16 */
typedef struct { unsigned long long w[MAXW]; } BS;

static int N, NN, NW;
static signed char *PX,*PY,*PZ;

static inline void bs_set(BS*a,int i){ a->w[i>>6]|=1ULL<<(i&63); }
static inline void bs_clr(BS*a,int i){ a->w[i>>6]&=~(1ULL<<(i&63)); }
static inline int  bs_pop(const BS*a){ int s=0;for(int t=0;t<NW;t++) s+=__builtin_popcountll(a->w[t]);return s; }

static unsigned long long rs;
static inline unsigned long long rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }

static int alive_list(const BS*a,int*out){
    int c=0;
    for(int t=0;t<NW;t++){
        unsigned long long w=a->w[t];
        while(w){ int b=__builtin_ctzll(w); w&=w-1; out[c++]=(t<<6)+b; }
    }
    return c;
}
static inline int idx(int x,int y,int z){ return (x*N+y)*N+z; }
static int gcd_(int a,int b){ a=a<0?-a:a; b=b<0?-b:b; while(b){int t=a%b;a=b;b=t;} return a?a:1; }

/* убить всю решёточную прямую через клетки i и j */
static void kill_line(BS*s,int i,int j){
    int dx=PX[j]-PX[i], dy=PY[j]-PY[i], dz=PZ[j]-PZ[i];
    int g=gcd_(gcd_(dx,dy),dz); dx/=g; dy/=g; dz/=g;
    for(int dir=-1;dir<=1;dir+=2){
        int x=PX[i], y=PY[i], z=PZ[i];
        while(1){
            x+=dir*dx; y+=dir*dy; z+=dir*dz;
            if(x<0||y<0||z<0||x>=N||y>=N||z>=N) break;
            bs_clr(s,idx(x,y,z));
        }
    }
    bs_clr(s,i); bs_clr(s,j);
}

static void place(const BS*alive,int i,const int*chosen,int k,BS*out,int*buf){
    *out=*alive;
    bs_clr(out,i);
    for(int t=0;t<k;t++) kill_line(out,i,chosen[t]);
    if(k<2) return;
    /* ДВА СПОСОБА СНЯТЬ ПЛОСКОСТЬ, И ВЫБИРАТЬ НАДО ДЕШЁВЫЙ.
     * (1) пройти ЖИВЫЕ клетки и спросить каждую, лежит ли она на плоскости — цена |живых|;
     * (2) ПЕРЕЧИСЛИТЬ узлы самой плоскости и погасить их — цена ~n^2, независимо от живых.
     * Прежняя редакция всегда брала (1). В начале роста живых порядка n^3, то есть в n раз
     * больше, чем узлов плоскости: при n=12 это двенадцатикратная потеря на каждой паре.
     * К концу живых десятки и дешевле уже (1). Поэтому выбираем по фактическому числу. */
    int m=alive_list(out,buf);
    int плоскостьдешевле = (m > N*N);
    for(int a=0;a<k;a++){
        long long ux=PX[chosen[a]]-PX[i], uy=PY[chosen[a]]-PY[i], uz=PZ[chosen[a]]-PZ[i];
        for(int b=a+1;b<k;b++){
            long long vx=PX[chosen[b]]-PX[i], vy=PY[chosen[b]]-PY[i], vz=PZ[chosen[b]]-PZ[i];
            long long nx=uy*vz-uz*vy, ny=uz*vx-ux*vz, nz=ux*vy-uy*vx;
            if(nx==0&&ny==0&&nz==0) continue;      /* выровнены — уже убито прямой */
            long long d=nx*PX[i]+ny*PY[i]+nz*PZ[i];
            if(плоскостьдешевле){
                /* перечисляем узлы плоскости: по двум координатам свободно, третья решается */
                if(nz){
                    for(int x=0;x<N;x++) for(int y=0;y<N;y++){
                        long long r=d-nx*x-ny*y;
                        if(r%nz) continue;
                        long long z=r/nz; if(z<0||z>=N) continue;
                        bs_clr(out,idx(x,y,(int)z));
                    }
                } else if(ny){
                    for(int x=0;x<N;x++) for(int z=0;z<N;z++){
                        long long r=d-nx*x-nz*z;
                        if(r%ny) continue;
                        long long y=r/ny; if(y<0||y>=N) continue;
                        bs_clr(out,idx(x,(int)y,z));
                    }
                } else {
                    for(int y=0;y<N;y++) for(int z=0;z<N;z++){
                        long long r=d-ny*y-nz*z;
                        if(r%nx) continue;
                        long long x=r/nx; if(x<0||x>=N) continue;
                        bs_clr(out,idx((int)x,y,z));
                    }
                }
            } else {
                for(int q=0;q<m;q++){
                    int t=buf[q];
                    if(t<0) continue;
                    long long wx=PX[t]-PX[i], wy=PY[t]-PY[i], wz=PZ[t]-PZ[i];
                    if(nx*wx+ny*wy+nz*wz==0){ bs_clr(out,t); buf[q]=-1; }
                }
            }
        }
    }
}

int main(int argc,char**argv){
    if(argc<3){ fprintf(stderr,"usage: equal_effort <n> <секунд> [выборка] [семя] [веха]\n"); return 2; }
    int n=atoi(argv[1]); double budget=atof(argv[2]);
    int SAMP=(argc>3)?atoi(argv[3]):8;
    /* ВЕХА — значение, время достижения которого записывается. НЕ ОСТАНАВЛИВАЕТ поиск:
     * остановка по достижению и есть тот `break`, который у напарника печатал предсказание
     * само себя. Здесь веха только СМОТРИТ на часы, а поиск идёт до конца бюджета. */
    int MILE=(argc>5)?atoi(argv[5]):0;
    double mile_t=-1.0;
    rs=(argc>4)?(unsigned long long)atoll(argv[4]):88172645463325252ULL;
    if(!rs) rs=1;
    N=n; NN=n*n*n; NW=(NN+63)/64;
    if(NW>MAXW){ fprintf(stderr,"n>16 не помещается\n"); return 2; }
    PX=malloc(NN);PY=malloc(NN);PZ=malloc(NN);
    { int t=0; for(int x=0;x<n;x++)for(int y=0;y<n;y++)for(int z=0;z<n;z++){PX[t]=x;PY[t]=y;PZ[t]=z;t++;} }

    int *chosen=malloc(sizeof(int)*NN), *best=malloc(sizeof(int)*NN);
    int *lst=malloc(sizeof(int)*NN), *buf=malloc(sizeof(int)*NN);
    int bestk=0; long long restarts=0;
    struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
    BS na, alive, bestset;
    while(1){
        clock_gettime(CLOCK_MONOTONIC,&t1);
        if((t1.tv_sec-t0.tv_sec)+1e-9*(t1.tv_nsec-t0.tv_nsec) >= budget) break;
        restarts++;
        memset(&alive,0,sizeof alive);
        for(int i=0;i<NN;i++) bs_set(&alive,i);
        int k=0;
        while(1){
            int cnt=alive_list(&alive,lst);
            if(!cnt) break;
            int pick=-1, bestleft=-1;
            int s=(SAMP<cnt)?SAMP:cnt;
            for(int q=0;q<s;q++){
                int cand=lst[rnd()%(unsigned long long)cnt];
                place(&alive,cand,chosen,k,&na,buf);
                int left=bs_pop(&na);
                if(left>bestleft){ bestleft=left; pick=cand; bestset=na; }
            }
            if(pick<0) break;
            alive=bestset; chosen[k++]=pick;
        }
        if(k>bestk){
            bestk=k; memcpy(best,chosen,sizeof(int)*k);
            if(MILE && mile_t<0 && bestk>=MILE){
                struct timespec tm; clock_gettime(CLOCK_MONOTONIC,&tm);
                mile_t=(tm.tv_sec-t0.tv_sec)+1e-9*(tm.tv_nsec-t0.tv_nsec);
            }
        }
    }
    clock_gettime(CLOCK_MONOTONIC,&t1);
    double el=(t1.tv_sec-t0.tv_sec)+1e-9*(t1.tv_nsec-t0.tv_nsec);
    printf("n=%d лучшее=%d потолок3n=%d перезапусков=%lld время=%.1fс отношение=%.3f веха=%d время_вехи=%s\n",
           n,bestk,3*n,restarts,el,(double)bestk/n,MILE,
           MILE? (mile_t>=0? ({static char b[32]; snprintf(b,sizeof b,"%.2f",mile_t); b;}) : "НЕ_ДОСТИГНУТА") : "-");
    fprintf(stderr,"ТОЧКИ n=%d k=%d:",n,bestk);
    for(int t=0;t<bestk;t++) fprintf(stderr," %d %d %d",PX[best[t]],PY[best[t]],PZ[best[t]]);
    fprintf(stderr,"\n");
    return 0;
}
