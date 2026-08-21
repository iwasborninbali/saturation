/* death2d.c — исчерпывающий счётчик для задачи о трёх точках на прямой (2D), по формуле смерти.
 *
 * ИДЕЯ. Две точки убивают прямую: третьей на ней не быть. Клетка ЖИВА, пока через неё не прошла
 * ни одна мёртвая прямая. Вопрос «сколько точек влезет» становится вопросом «когда кончается
 * место для рождения».
 *
 * УСТРОЙСТВО ОБХОДА — ПО СТРОКАМ, А НЕ ПО КЛЕТКАМ. При цели 2n запас ёмкости РАВЕН НУЛЮ:
 * n строк по две точки дают ровно 2n, значит КАЖДАЯ строка несёт РОВНО две, и каждый столбец
 * тоже. Поэтому перебирать надо ПАРЫ В СТРОКЕ: глубина n вместо 2n, ветвление C(n,2) вместо n^2.
 * Первая моя редакция шла по клеткам и была в 40-80 раз хуже по узлам нашего же прежнего
 * перечислителя (n=11: 2.29 млрд против 28.7 млн) — при том что отсечение по смерти в ней было.
 * Отсечение не спасает неверный порядок обхода: это тот же урок, что мы получили на трёхмерии,
 * где дробление по свежему слою закрывало 1 ребёнка из 64 вместо 57.
 *
 * ОТСЕЧЕНИЯ:
 *   1) СМЕРТЬ: размещено k, живых a  =>  больше k+a точек не будет никогда.
 *   2) ЁМКОСТЬ СТОЛБЦОВ: каждый столбец несёт ровно две; оставшиеся строки обязаны положить
 *      2*(n-r) точек в столбцы, где ещё есть место. Если места меньше — ветка мертва.
 *
 * ЧТО СЧИТАЕТ: полное число размещений 2n точек на сетке n на n без трёх на прямой, БЕЗ учёта
 * симметрий — то есть в точности A000755. Эталон:
 *     n:   2  3   4   5   6    7    8    9    10    11    12
 *     a(n):1  2  11  32  50  132  380  368  1135  1120  4348
 * Инструмент, не воспроизводящий эти одиннадцать, негоден.
 *
 * СБОРКА: cc -O3 -march=native -o death2d death2d.c
 * ЗАПУСК: ./death2d <n>
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXW 8                      /* 8 слов по 64 бита = 512 клеток, то есть n <= 22 */
typedef struct { unsigned long long w[MAXW]; } BS;

static int N, NN, NW;
static BS *killp;                   /* killp[i*NN+j] — маска клеток на прямой через i и j */
static unsigned long long NODES, COUNT;
static int colcnt[32];

static inline void bs_zero(BS *a){ for (int t=0;t<NW;t++) a->w[t]=0ULL; }
static inline void bs_set(BS *a,int i){ a->w[i>>6] |= 1ULL<<(i&63); }
static inline int  bs_get(const BS *a,int i){ return (a->w[i>>6]>>(i&63))&1ULL; }
static inline void bs_andnot(BS *a,const BS *b){ for(int t=0;t<NW;t++) a->w[t] &= ~b->w[t]; }
static inline int  bs_pop(const BS *a){ int s=0; for(int t=0;t<NW;t++) s+=__builtin_popcountll(a->w[t]); return s; }

/* сколько живых клеток в строке r */
static inline int alive_in_row(const BS *a,int r){
    int c=0; for(int y=0;y<N;y++) if (bs_get(a, r*N+y)) c++;
    return c;
}

static int DIRCHK = 0;   /* сколько последних точек проверять по направлениям */
static int chosen[64], nchosen;

/* НАПРАВЛЕНИЯ: смерть, перенесённая из клеток в направления (мысль хозяина).
 * У каждой уже рождённой точки A все остальные обязаны лежать в РАЗНЫХ направлениях —
 * иначе три на прямой. Несколько живых клеток могут лежать на ОДНОМ луче из A, и взять
 * из них можно только одну. Значит
 *      осталось взять  <=  число живых НАПРАВЛЕНИЙ из A
 * и эта оценка строго не хуже счёта живых клеток: луч схлопывается в единицу.
 * dirid[a*NN+q] — номер примитивного направления из a в q. */
static int *dirid;
static int NDIR;
static unsigned long long dseen[16];   /* до 1024 направлений */

static int dir_bound(const BS *alive, int a){
    for (int t=0;t<16;t++) dseen[t]=0ULL;
    int cnt=0;
    const int *row = dirid + (size_t)a*NN;
    for(int t=0;t<NW;t++){
        unsigned long long w = alive->w[t];
        while(w){
            int b=__builtin_ctzll(w); w&=w-1;
            int d = row[(t<<6)+b];
            if (!((dseen[d>>6]>>(d&63))&1ULL)){ dseen[d>>6]|=1ULL<<(d&63); cnt++; }
        }
    }
    return cnt;
}

static void rec(BS alive, int row){
    NODES++;
    if (row == N){ COUNT++; return; }
    int need = 2*(N-row);
    /* ОТСЕЧЕНИЕ ПО СМЕРТИ: живых меньше, чем осталось положить */
    if (bs_pop(&alive) < need) return;
    /* ЁМКОСТЬ СТОЛБЦОВ: суммарное свободное место в столбцах должно покрыть остаток */
    int room=0;
    for(int c=0;c<N;c++){ int r2 = 2-colcnt[c]; if (r2>0) room += r2; }
    if (room < need) return;
    /* каждая оставшаяся строка обязана нести ДВЕ: если в какой-то живых меньше двух — отбой */
    for(int r=row;r<N;r++) if (alive_in_row(&alive,r) < 2) return;
    /* СМЕРТЬ В НАПРАВЛЕНИЯХ. Из последних рождённых точек считаем число РАЗЛИЧНЫХ живых
     * направлений: больше него взять нельзя, потому что две точки на одном луче из A
     * дали бы три на прямой вместе с A. Оценка не хуже счёта клеток и часто строго лучше. */
    for(int t=nchosen-1; t>=0 && t>=nchosen-DIRCHK; t--)
        if (dir_bound(&alive, chosen[t]) < need) return;
    /* ОТСЕЧЕНИЕ ПО ПОЛНОТЕ СТОЛБЦОВ — ИЗМЕРЕНО И ОТВЕРГНУТО.
     * При цели 2n столбец обязан набрать ровно две, и проверка «живых в столбце меньше,
     * чем ему нужно» сокращала узлы на 36% (361 -> 230 млн при n=11). Но каждый узел
     * замедлялся на 44%, и по времени выходил чистый проигрыш: 49.2с -> 56.3с.
     * Ограничение проверки последними пятью строками не спасло (59.7с): большинство узлов
     * и так лежит у конца дерева, так что «включать только там, где кусается» здесь не
     * работает — кусается везде, где мы и считаем.
     * Оставлено выключенным. Записано, чтобы не возвращаться: отсечение, сокращающее узлы,
     * может проигрывать по времени, и решает это ЗАМЕР, а не убедительность довода. */

    for(int c1=0;c1<N;c1++){
        int i = row*N + c1;
        if (!bs_get(&alive,i)) continue;
        if (colcnt[c1] >= 2) continue;
        for(int c2=c1+1;c2<N;c2++){
            int j = row*N + c2;
            if (!bs_get(&alive,j)) continue;
            if (colcnt[c2] >= 2) continue;
            BS na = alive;
            /* строка исчерпана: убираем её целиком */
            for(int y=0;y<N;y++) na.w[(row*N+y)>>6] &= ~(1ULL<<((row*N+y)&63));
            for(int t=0;t<nchosen;t++){
                bs_andnot(&na,&killp[(size_t)i*NN + chosen[t]]);
                bs_andnot(&na,&killp[(size_t)j*NN + chosen[t]]);
            }
            bs_andnot(&na,&killp[(size_t)i*NN + j]);
            chosen[nchosen++]=i; chosen[nchosen++]=j;
            colcnt[c1]++; colcnt[c2]++;
            rec(na,row+1);
            colcnt[c1]--; colcnt[c2]--;
            nchosen-=2;
        }
    }
}

int main(int argc,char**argv){
    if (argc<2){ fprintf(stderr,"usage: death2d <n>\n"); return 2; }
    N = atoi(argv[1]); NN = N*N; NW = (NN+63)/64;
    if (argc>2) DIRCHK = atoi(argv[2]);
    if (NW>MAXW){ fprintf(stderr,"n слишком велико: нужно %d слов, есть %d\n",NW,MAXW); return 2; }

    killp = calloc((size_t)NN*NN,sizeof(BS));
    if(!killp){ fprintf(stderr,"нет памяти\n"); return 2; }
    for(int i=0;i<NN;i++){
        int xi=i/N, yi=i%N;
        for(int j=i+1;j<NN;j++){
            int xj=j/N, yj=j%N;
            BS m; bs_zero(&m);
            for(int k=0;k<NN;k++){
                if(k==i||k==j) continue;
                int xk=k/N, yk=k%N;
                if ((long long)(xj-xi)*(yk-yi) - (long long)(yj-yi)*(xk-xi) == 0) bs_set(&m,k);
            }
            killp[(size_t)i*NN+j]=m; killp[(size_t)j*NN+i]=m;
        }
    }
    /* нумерация примитивных направлений */
    {
        int *map = calloc((size_t)(2*N+1)*(2*N+1), sizeof(int));
        for (size_t t=0;t<(size_t)(2*N+1)*(2*N+1);t++) map[t] = -1;
        dirid = malloc((size_t)NN*NN*sizeof(int));
        NDIR = 0;
        for(int a=0;a<NN;a++){
            int ax=a/N, ay=a%N;
            for(int q=0;q<NN;q++){
                int dx=q/N-ax, dy=q%N-ay;
                if (dx==0 && dy==0){ dirid[(size_t)a*NN+q]=0; continue; }
                int g=dx<0?-dx:dx, h=dy<0?-dy:dy;
                while(h){ int r2=g%h; g=h; h=r2; }
                if(g==0) g=1;
                int px=dx/g, py=dy/g;
                int key=(px+N)*(2*N+1)+(py+N);
                if (map[key]<0) map[key]=NDIR++;
                dirid[(size_t)a*NN+q]=map[key];
            }
        }
        free(map);
        if (NDIR > 1024){ fprintf(stderr,"направлений %d — больше 1024\n",NDIR); return 2; }
    }
    BS all; bs_zero(&all);
    for(int i=0;i<NN;i++) bs_set(&all,i);
    memset(colcnt,0,sizeof colcnt);
    nchosen=0; NODES=0; COUNT=0;

    struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
    rec(all,0);
    clock_gettime(CLOCK_MONOTONIC,&t1);
    double el=(t1.tv_sec-t0.tv_sec)+1e-9*(t1.tv_nsec-t0.tv_nsec);
    printf("n=%d M=%d: решений %llu, узлов %llu, %.2fс (%.0f узлов/с)\n",
           N, 2*N, COUNT, NODES, el, el>0? NODES/el : 0.0);
    free(killp);
    return 0;
}
