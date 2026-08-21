/* search2d.c — поиск больших расстановок без трёх на прямой, с ВЫБОРОМ ПРАВИЛА ВЫБОРА.
 *
 * ЗАЧЕМ. Измерено на полном материале при n=6 и n=7: расстановки, ДОРАСТАЮЩИЕ до максимума,
 * отличаются от упирающихся тем, что они УПОРЯДОЧЕННЕЕ — меньше различных направлений,
 * меньше суммарная площадь троек, выше пик спектра. Обогащение x3.5 в лучших 5%.
 * Это порядок предпочтения, а не запрет, и потому его место — в ВЫБОРЕ КАНДИДАТА.
 * Здесь он ставится рядом с прежним правилом, чтобы сравнить, а не чтобы поверить.
 *
 * ПРАВИЛА:
 *   0 — прежнее: брать кандидата, оставляющего БОЛЬШЕ ЖИВЫХ («беречь место»);
 *   1 — новое: брать кандидата, добавляющего МЕНЬШЕ НОВЫХ НАПРАВЛЕНИЙ («беречь порядок»);
 *   2 — оба: сначала по направлениям, ничьи разрешаются живыми;
 *   3 — ЁМКОСТЬ: в строке не больше двух точек, значит из живых клеток строки возьмёшь
 *       не больше min(2 - уже_в_строке, живых_в_строке). Сумма по строкам — граница сверху
 *       на число добавимых; то же по столбцам, берём меньшую. Измерено на полном материале
 *       при n=6: ёмкость разделяет ведущих к максимуму от тупиковых на 1.3..5.5 сигмы против
 *       1.1..3.0 у простого счёта живых, и при этом «k + ёмкость < цель» убивает до 97%
 *       тупиковых, НЕ ГУБЯ НИ ОДНОЙ ведущей — то есть это законное отсечение, а не эвристика.
 *
 * СБОРКА: cc -O3 -march=native -o search2d search2d.c
 * ЗАПУСК: ./search2d <n> <секунд> <правило> [выборка] [семя]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXW 64                       /* 4096 клеток -> n <= 64 */
typedef struct { unsigned long long w[MAXW]; } BS;
static int N,NN,NW;
static unsigned char *DIRCNT;         /* сколько раз направление уже использовано */
static int DW;                        /* ширина таблицы направлений */

static inline void bs_set(BS*a,int i){ a->w[i>>6]|=1ULL<<(i&63); }
static inline void bs_clr(BS*a,int i){ a->w[i>>6]&=~(1ULL<<(i&63)); }
static inline int  bs_pop(const BS*a){int s=0;for(int t=0;t<NW;t++)s+=__builtin_popcountll(a->w[t]);return s;}
static unsigned long long rs;
static inline unsigned long long rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
static int alive_list(const BS*a,int*o){int c=0;for(int t=0;t<NW;t++){unsigned long long w=a->w[t];
    while(w){int b=__builtin_ctzll(w);w&=w-1;o[c++]=(t<<6)+b;}}return c;}
static int gcd_(int a,int b){a=a<0?-a:a;b=b<0?-b:b;while(b){int t=a%b;a=b;b=t;}return a?a:1;}

/* примитивное направление между клетками i и j, приведённое к канону, в индекс таблицы */
static inline int dirindex(int i,int j){
    int dx=(j%N)-(i%N), dy=(j/N)-(i/N);
    int g=gcd_(dx,dy); dx/=g; dy/=g;
    if(dx<0 || (dx==0&&dy<0)){ dx=-dx; dy=-dy; }
    return dx*(2*N) + (dy+N);
}
/* убить всю прямую через i и j */
static void kill_line(BS*s,int i,int j){
    int dx=(j%N)-(i%N), dy=(j/N)-(i/N);
    int g=gcd_(dx,dy); dx/=g; dy/=g;
    for(int d=-1;d<=1;d+=2){
        int x=i%N, y=i/N;
        while(1){ x+=d*dx; y+=d*dy; if(x<0||y<0||x>=N||y>=N) break; bs_clr(s,y*N+x); }
    }
    bs_clr(s,i); bs_clr(s,j);
}

int main(int argc,char**argv){
    if(argc<4){ fprintf(stderr,"usage: search2d <n> <секунд> <правило> [выборка] [семя]\n"); return 2; }
    int n=atoi(argv[1]); double budget=atof(argv[2]); int RULE=atoi(argv[3]);
    int SAMP=(argc>4)?atoi(argv[4]):8;
    rs=(argc>5)?(unsigned long long)atoll(argv[5]):88172645463325252ULL; if(!rs) rs=1;
    N=n; NN=n*n; NW=(NN+63)/64;
    if(NW>MAXW){ fprintf(stderr,"n слишком велик\n"); return 2; }
    DW=(N+1)*(2*N+1);
    DIRCNT=malloc(DW);
    int *chosen=malloc(sizeof(int)*NN), *best=malloc(sizeof(int)*NN), *lst=malloc(sizeof(int)*NN);
    int *lst2=malloc(sizeof(int)*NN);
    int bestk=0; long long restarts=0;
    struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
    BS alive,na,bestset;
    while(1){
        clock_gettime(CLOCK_MONOTONIC,&t1);
        if((t1.tv_sec-t0.tv_sec)+1e-9*(t1.tv_nsec-t0.tv_nsec)>=budget) break;
        restarts++;
        memset(&alive,0,sizeof alive);
        for(int i=0;i<NN;i++) bs_set(&alive,i);
        memset(DIRCNT,0,DW);
        int k=0;
        while(1){
            int cnt=alive_list(&alive,lst);
            if(!cnt) break;
            int pick=-1, bestlive=-1, bestnew=1<<30, bestcap=-1;
            int ст[64], сб[64];
            if(RULE==3){ for(int t=0;t<N;t++){ст[t]=0;сб[t]=0;} for(int t=0;t<k;t++){ ст[chosen[t]/N]++; сб[chosen[t]%N]++; } }
            int s=(SAMP<cnt)?SAMP:cnt;
            for(int q=0;q<s;q++){
                int cand=lst[rnd()%(unsigned long long)cnt];
                int nnew=0;
                if(RULE){ for(int t=0;t<k;t++) if(!DIRCNT[dirindex(cand,chosen[t])]) nnew++; }
                na=alive; bs_clr(&na,cand);
                for(int t=0;t<k;t++) kill_line(&na,cand,chosen[t]);
                int live=bs_pop(&na);
                int cap=0;
                if(RULE==3){
                    int жст[64],жсб[64];
                    for(int t=0;t<N;t++){жст[t]=0;жсб[t]=0;}
                    int m2=alive_list(&na,lst2);
                    for(int q2=0;q2<m2;q2++){ жст[lst2[q2]/N]++; жсб[lst2[q2]%N]++; }
                    int a1=0,b1=0;
                    int дст=ст[cand/N]+1, дсб=сб[cand%N]+1;
                    for(int r=0;r<N;r++){
                        int занято = ст[r] + (r==cand/N?1:0);
                        int мест = 2-занято; if(мест<0) мест=0;
                        a1 += (жст[r]<мест?жст[r]:мест);
                    }
                    for(int c2=0;c2<N;c2++){
                        int занято = сб[c2] + (c2==cand%N?1:0);
                        int мест = 2-занято; if(мест<0) мест=0;
                        b1 += (жсб[c2]<мест?жсб[c2]:мест);
                    }
                    cap = a1<b1?a1:b1;
                    (void)дст;(void)дсб;
                }
                int лучше=0;
                if(RULE==3) лучше = (cap>bestcap) || (cap==bestcap && live>bestlive);
                else if(RULE==0) лучше = (live>bestlive);
                else if(RULE==1) лучше = (nnew<bestnew);
                else лучше = (nnew<bestnew) || (nnew==bestnew && live>bestlive);
                if(лучше){ bestlive=live; bestnew=nnew; bestcap=cap; pick=cand; bestset=na; }
            }
            if(pick<0) break;
            for(int t=0;t<k;t++){ int d=dirindex(pick,chosen[t]); if(DIRCNT[d]<255) DIRCNT[d]++; }
            alive=bestset; chosen[k++]=pick;
        }
        if(k>bestk){ bestk=k; memcpy(best,chosen,sizeof(int)*k); }
    }
    clock_gettime(CLOCK_MONOTONIC,&t1);
    double el=(t1.tv_sec-t0.tv_sec)+1e-9*(t1.tv_nsec-t0.tv_nsec);
    printf("n=%d правило=%d лучшее=%d цель2n=%d перезапусков=%lld %.1fс\n",n,RULE,bestk,2*n,restarts,el);
    fprintf(stderr,"ТОЧКИ n=%d k=%d:",n,bestk);
    for(int t=0;t<bestk;t++) fprintf(stderr," %d %d",best[t]%N,best[t]/N);
    fprintf(stderr,"\n");
    return 0;
}
