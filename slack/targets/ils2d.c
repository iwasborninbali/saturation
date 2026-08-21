/* ils2d.c — ЧИСТЫЙ ПЕРЕЗАПУСК против ЛОКАЛЬНОГО ХОДА, при равном времени.
 *
 * ЗАЧЕМ. Мы вывели из рассеянности максимумов, что локальное улучшение работать не может.
 * Напарник привёл числа против: в его пространстве орбит локальный ход (выбить j, дорастить)
 * бьёт чистый перезапуск, делая при этом в четыре тысячи раз МЕНЬШЕ заполнений.
 * Его объяснение: выигрывает не направленность, а ЦЕНА попытки — доращивание от ядра
 * дешевле, чем от пустоты, а у него ход кладёт орбиту и проверка стоит O(k^3).
 * ПРЕДСКАЗАНИЕ ДЛЯ МОЕГО ПРОСТРАНСТВА: ход кладёт ОДНУ клетку, стоимость шага почти
 * не зависит от размера ядра, значит заполнений в секунду должно быть ПОРОВНУ,
 * и локальный ход не должен давать ничего.
 * Меряем НЕ ИСХОД, А ЧИСЛО ЗАПОЛНЕНИЙ В СЕКУНДУ — это и различает две гипотезы.
 *
 * СБОРКА: cc -O3 -march=native -o ils2d ils2d.c
 * ЗАПУСК: ./ils2d <n> <секунд> <режим 0=перезапуск 1=локальный> <выбито j> [выборка] [семя]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#define MAXW 64
typedef struct { unsigned long long w[MAXW]; } BS;
static int N,NN,NW;
static inline void bs_set(BS*a,int i){ a->w[i>>6]|=1ULL<<(i&63); }
static inline void bs_clr(BS*a,int i){ a->w[i>>6]&=~(1ULL<<(i&63)); }
static inline int  bs_pop(const BS*a){int s=0;for(int t=0;t<NW;t++)s+=__builtin_popcountll(a->w[t]);return s;}
static unsigned long long rs;
static inline unsigned long long rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
static int alive_list(const BS*a,int*o){int c=0;for(int t=0;t<NW;t++){unsigned long long w=a->w[t];
    while(w){int b=__builtin_ctzll(w);w&=w-1;o[c++]=(t<<6)+b;}}return c;}
static int gcd_(int a,int b){a=a<0?-a:a;b=b<0?-b:b;while(b){int t=a%b;a=b;b=t;}return a?a:1;}
static void kill_line(BS*s,int i,int j){
    int dx=(j%N)-(i%N), dy=(j/N)-(i/N);
    int g=gcd_(dx,dy); dx/=g; dy/=g;
    for(int d=-1;d<=1;d+=2){
        int x=i%N,y=i/N;
        while(1){ x+=d*dx; y+=d*dy; if(x<0||y<0||x>=N||y>=N) break; bs_clr(s,y*N+x); }
    }
    bs_clr(s,i); bs_clr(s,j);
}
/* пересобрать живое множество по списку выбранных */
static void rebuild(BS*alive,const int*ch,int k){
    memset(alive,0,sizeof(BS));
    for(int i=0;i<NN;i++) bs_set(alive,i);
    for(int a=0;a<k;a++){ bs_clr(alive,ch[a]);
        for(int b=a+1;b<k;b++) kill_line(alive,ch[a],ch[b]); }
    for(int a=0;a<k;a++) bs_clr(alive,ch[a]);
}
int main(int argc,char**argv){
    if(argc<5){ fprintf(stderr,"usage: ils2d <n> <секунд> <режим> <j> [выборка] [семя]\n"); return 2; }
    int n=atoi(argv[1]); double budget=atof(argv[2]); int MODE=atoi(argv[3]); int J=atoi(argv[4]);
    int SAMP=(argc>5)?atoi(argv[5]):8;
    rs=(argc>6)?(unsigned long long)atoll(argv[6]):88172645463325252ULL; if(!rs) rs=1;
    N=n; NN=n*n; NW=(NN+63)/64;
    int *ch=malloc(sizeof(int)*NN), *best=malloc(sizeof(int)*NN), *lst=malloc(sizeof(int)*NN);
    int bestk=0; long long заполнений=0;
    struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
    BS alive,na,bs2;
    int k=0;
    while(1){
        clock_gettime(CLOCK_MONOTONIC,&t1);
        if((t1.tv_sec-t0.tv_sec)+1e-9*(t1.tv_nsec-t0.tv_nsec)>=budget) break;
        if(MODE==0 || bestk==0){ k=0; memset(&alive,0,sizeof alive);
            for(int i=0;i<NN;i++) bs_set(&alive,i); }
        else {                                   /* локальный ход: взять лучшее, выбить J */
            k=bestk; memcpy(ch,best,sizeof(int)*k);
            for(int t=0;t<J && k>0;t++){ int p=rnd()%(unsigned long long)k; ch[p]=ch[--k]; }
            rebuild(&alive,ch,k);
        }
        while(1){
            int cnt=alive_list(&alive,lst);
            if(!cnt) break;
            int pick=-1,bl=-1; int s=(SAMP<cnt)?SAMP:cnt;
            for(int q=0;q<s;q++){
                int c=lst[rnd()%(unsigned long long)cnt];
                na=alive; bs_clr(&na,c);
                for(int t=0;t<k;t++) kill_line(&na,c,ch[t]);
                int lv=bs_pop(&na);
                if(lv>bl){ bl=lv; pick=c; bs2=na; }
            }
            if(pick<0) break;
            alive=bs2; ch[k++]=pick;
        }
        заполнений++;
        if(k>bestk){ bestk=k; memcpy(best,ch,sizeof(int)*k); }
    }
    clock_gettime(CLOCK_MONOTONIC,&t1);
    double el=(t1.tv_sec-t0.tv_sec)+1e-9*(t1.tv_nsec-t0.tv_nsec);
    printf("n=%d режим=%s j=%d: лучшее=%d, заполнений=%lld (%.0f/с), цель2n=%d, %.1fс\n",
           n, MODE?"локальный":"перезапуск", J, bestk, заполнений, заполнений/el, 2*n, el);
    return 0;
}
