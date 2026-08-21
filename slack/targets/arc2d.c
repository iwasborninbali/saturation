/* arc2d.c — ИСЧЕРПЫВАЮЩИЙ максимум «дуги по модулю p» в двумерии:
 * набор в F_p^2 без трёх коллинеарных ПО МОДУЛЮ p.
 *
 * ЗАЧЕМ. Тройка коллинеарна над Z => её определитель ноль над Z => ноль по модулю p.
 * Значит «нет трёх коллинеарных mod p» ВЛЕЧЁТ «нет трёх коллинеарных в сетке»: модульное
 * условие СТРОЖЕ. Всякая конструкция, чья правильность заверяется по модулю, годится в
 * сетке даром — и ровно поэтому ограничена тем, что возможно по модулю.
 * В трёхмерии мы доказали потолок p+1 исчерпывающе при p=5 (129 337 161 узлов). Здесь —
 * симметричная половина: тот же вопрос в двумерии. Ожидание: p+1 при истине 2p.
 *
 * СБОРКА: cc -O3 -march=native -o arc2d arc2d.c ; ЗАПУСК: ./arc2d <p> [секунд]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#define MAXW 4                       /* 256 точек: p <= 15 */
typedef struct { unsigned long long w[MAXW]; } BS;
static int P,N,NW; static int chosen[64];
static BS *LIN; static long long nodes=0; static int best=0;
static double LIMIT; static struct timespec T0; static int stopped=0;
static inline int bget(const BS*a,int i){return (a->w[i>>6]>>(i&63))&1ULL;}
static inline void bset(BS*a,int i){a->w[i>>6]|=1ULL<<(i&63);}
static inline void bclr(BS*a,int i){a->w[i>>6]&=~(1ULL<<(i&63));}
static inline int bpop(const BS*a){int s=0;for(int t=0;t<NW;t++)s+=__builtin_popcountll(a->w[t]);return s;}
static double el(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);
    return (t.tv_sec-T0.tv_sec)+1e-9*(t.tv_nsec-T0.tv_nsec);}
static void dfs(int start,int k,BS alive){
    nodes++;
    if((nodes&0xFFFFF)==0 && el()>LIMIT) stopped=1;
    if(stopped) return;
    if(k>best) best=k;
    if(k+bpop(&alive)<=best) return;
    for(int c=start;c<N;c++){
        if(!bget(&alive,c)) continue;
        BS na=alive;
        for(int t=0;t<=c;t++) bclr(&na,t);
        for(int t=0;t<k;t++){ BS*m=&LIN[(size_t)chosen[t]*N+c];
            for(int w=0;w<NW;w++) na.w[w] &= ~m->w[w]; }
        chosen[k]=c; dfs(c+1,k+1,na); if(stopped) return;
    }
}
int main(int argc,char**argv){
    P=atoi(argv[1]); LIMIT=(argc>2)?atof(argv[2]):1e18;
    N=P*P; NW=(N+63)/64;
    if(NW>MAXW){fprintf(stderr,"p слишком велико\n");return 2;}
    LIN=calloc((size_t)N*N,sizeof(BS));
    for(int i=0;i<N;i++)for(int j=0;j<N;j++){
        if(i==j) continue;
        int x1=i%P,y1=i/P,x2=j%P,y2=j/P;
        BS m; memset(&m,0,sizeof m);
        for(int k=0;k<N;k++){int x3=k%P,y3=k/P;
            if((((x2-x1)*(y3-y1)-(y2-y1)*(x3-x1))%P+P)%P==0) bset(&m,k);}
        LIN[(size_t)i*N+j]=m;
    }
    clock_gettime(CLOCK_MONOTONIC,&T0);
    BS all; memset(&all,0,sizeof all); for(int i=0;i<N;i++) bset(&all,i);
    dfs(0,0,all);
    printf("p=%2d: %s максимум %2d (p+1 = %2d), узлов %lld, %.2fс   [истина в сетке 2p = %d]\n",
           P, stopped?"ОБОРВАНО —":"ИСЧЕРПАНО —", best, P+1, nodes, el(), 2*P);
    return 0;
}
