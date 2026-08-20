/* plane4_gen.c — генератор CNF для A280537 на C. Замена plane4_cnf.py.
 *
 * Зачем. При n=7 перечисление 346 743 плоскостей на Python занимает 62 с, то есть 89 % времени
 * генерации, и повторяется для каждого из 816 кусков разбиения. Кеш уменьшает это до 1 с, но
 * остаются ещё ~8 с на построение и запись 2.7 млн клауз; на C всё вместе — доли секунды.
 *
 * УПРОЩЕНИЕ, снимающее самую громоздкую часть: если зафиксированы профили слоёв по ВСЕМ трём осям,
 * то суммарное число точек определено ими и равно M. Глобальный счётчик «не менее M» становится
 * излишним, и тотализатор не нужен вовсе.
 *
 *   usage: plane4_gen n out.cnf "px" "py" "pz" [--sym]
 *          профиль — n чисел через запятую; "-" означает «ось не ограничивать»
 *   Без профилей вовсе программа не имеет кардинальности и годится лишь для проверок.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int N, NC;
static int *X, *Y, *Z;
static int nv;                     /* число переменных */
static FILE *out;
static long long ncl = 0;

static void cl5(int a, int b, int c, int d, int e) {   /* до пяти литералов, 0 = нет */
    if (a) fprintf(out, "%d ", a);
    if (b) fprintf(out, "%d ", b);
    if (c) fprintf(out, "%d ", c);
    if (d) fprintf(out, "%d ", d);
    if (e) fprintf(out, "%d ", e);
    fputs("0\n", out); ncl++;
}
#define cl(a,b,c,d) cl5((a),(b),(c),(d),0)
static int newvar(void) { return ++nv; }

/* at-most-k методом Синца (2005) над массивом литералов */
static void atmost(int *lits, int m, int k) {
    if (m <= k) return;
    if (k == 3 && m <= 8) {                            /* прямая кодировка дешевле */
        for (int a = 0; a < m; a++) for (int b = a+1; b < m; b++)
            for (int c = b+1; c < m; c++) for (int d = c+1; d < m; d++)
                cl(-lits[a], -lits[b], -lits[c], -lits[d]);
        return;
    }
    int *s = malloc(sizeof(int)*(m-1)*k);
    for (int i = 0; i < (m-1)*k; i++) s[i] = newvar();
    #define S(i,j) s[(i)*k + (j)]
    cl(-lits[0], S(0,0), 0, 0);
    for (int j = 1; j < k; j++) cl(-S(0,j), 0, 0, 0);
    for (int i = 1; i < m-1; i++) {
        cl(-lits[i], S(i,0), 0, 0);
        cl(-S(i-1,0), S(i,0), 0, 0);
        for (int j = 1; j < k; j++) {
            cl(-lits[i], -S(i-1,j-1), S(i,j), 0);
            cl(-S(i-1,j), S(i,j), 0, 0);
        }
        cl(-lits[i], -S(i-1,k-1), 0, 0);
    }
    cl(-lits[m-1], -S(m-2,k-1), 0, 0);
    #undef S
    free(s);
}

static void exactly(int *lits, int m, int k) {         /* ровно k: at-most-k и at-most-(m-k) отрицаний */
    atmost(lits, m, k);
    int *neg = malloc(sizeof(int)*m);
    for (int i = 0; i < m; i++) neg[i] = -lits[i];
    atmost(neg, m, m-k);
    free(neg);
}

/* ---- плоскости: перечисление по тройкам узлов с дедупликацией ---- */
static int gcd2(int a,int b){a=abs(a);b=abs(b);while(b){int t=a%b;a=b;b=t;}return a;}
static int *ka,*kb,*kc,*kd,*htab; static int hn=0, HB;

static int plane_id(int a,int b,int c,int d){
    int g=gcd2(gcd2(a,b),c); if(!g) g=1; a/=g;b/=g;c/=g;d/=g;
    if(a<0||(a==0&&(b<0||(b==0&&c<0)))){a=-a;b=-b;c=-c;d=-d;}
    unsigned h=((unsigned)(a*73856093)^(unsigned)(b*19349663)^(unsigned)(c*83492791)^(unsigned)(d*2654435761u));
    h&=(1u<<HB)-1;
    while(htab[h]>=0){int j=htab[h]; if(ka[j]==a&&kb[j]==b&&kc[j]==c&&kd[j]==d) return j; h=(h+1)&((1u<<HB)-1);}
    htab[h]=hn; ka[hn]=a;kb[hn]=b;kc[hn]=c;kd[hn]=d; return hn++;
}

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr,"usage: %s n out.cnf px py pz [--sym]\n", argv[0]); return 1; }
    N = atoi(argv[1]); NC = N*N*N; nv = NC;
    const char *path = argv[2];
    int sym = 0; for (int i = 6; i < argc; i++) if (!strcmp(argv[i],"--sym")) sym = 1;

    X=malloc(4*NC);Y=malloc(4*NC);Z=malloc(4*NC);
    for(int i=0;i<NC;i++){X[i]=i/(N*N);Y[i]=(i/N)%N;Z[i]=i%N;}

    long long tri=(long long)NC*(NC-1)*(NC-2)/6;
    HB=1; while((1LL<<HB) < 4*(tri+16)) HB++;
    htab=malloc(sizeof(int)*(1LL<<HB)); for(long long i=0;i<(1LL<<HB);i++) htab[i]=-1;
    long long cap=tri+16;
    ka=malloc(sizeof(int)*cap);kb=malloc(sizeof(int)*cap);kc=malloc(sizeof(int)*cap);kd=malloc(sizeof(int)*cap);

    for(int i=0;i<NC;i++)for(int j=i+1;j<NC;j++)for(int k=j+1;k<NC;k++){
        int ux=X[j]-X[i],uy=Y[j]-Y[i],uz=Z[j]-Z[i];
        int vx=X[k]-X[i],vy=Y[k]-Y[i],vz=Z[k]-Z[i];
        int a=uy*vz-uz*vy,b=uz*vx-ux*vz,c=ux*vy-uy*vx;
        if(!a&&!b&&!c) continue;
        plane_id(a,b,c,a*X[i]+b*Y[i]+c*Z[i]);
    }
    fprintf(stderr,"различных плоскостей %d\n", hn);

    /* Тело пишем во временный файл, заголовок дописываем впереди в конце. Возврат в начало
       файла с ручным подсчётом смещения уже дал неверный заголовок — не повторяем. */
    char tmp[1024]; snprintf(tmp,sizeof tmp,"%s.body",path);
    out = fopen(tmp,"w");
    if(!out){ perror("fopen"); return 3; }

    int *mem = malloc(sizeof(int)*NC);
    int rich = 0;
    for(int p=0;p<hn;p++){
        int m=0;
        for(int i=0;i<NC;i++) if(ka[p]*X[i]+kb[p]*Y[i]+kc[p]*Z[i]==kd[p]) mem[m++]=i+1;
        if(m>=4){ rich++; atmost(mem,m,3); }
    }
    fprintf(stderr,"богатых плоскостей %d\n", rich);

    for (int ax = 0; ax < 3; ax++) {
        const char *spec = argv[3+ax];
        if (!strcmp(spec,"-")) continue;
        int prof[64], np=0; char buf[512]; strncpy(buf,spec,511); buf[511]=0;
        for (char *t=strtok(buf,","); t; t=strtok(NULL,",")) prof[np++]=atoi(t);
        if (np != N) { fprintf(stderr,"профиль по оси %d имеет %d чисел, ожидалось %d\n",ax,np,N); return 2; }
        for (int t = 0; t < N; t++) {
            int m=0;
            for(int i=0;i<NC;i++){ int lay = ax==0?X[i]:(ax==1?Y[i]:Z[i]); if(lay==t) mem[m++]=i+1; }
            exactly(mem,m,prof[t]);
        }
    }

    if (sym) {                                          /* лексикографическое отсечение */
        int perm[6][3]={{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}};
        int *sig=malloc(sizeof(int)*NC);
        for(int pi=0;pi<6;pi++)for(int sg=0;sg<8;sg++){
            for(int i=0;i<NC;i++){
                int co[3]={X[i],Y[i],Z[i]}, nc2[3];
                for(int k=0;k<3;k++){ int v=co[perm[pi][k]]; nc2[k]=(sg>>k&1)?N-1-v:v; }
                sig[i]=(nc2[0]*N+nc2[1])*N+nc2[2];
            }
            int id=1; for(int i=0;i<NC;i++) if(sig[i]!=i){id=0;break;}
            if(id) continue;
            int eq=0;
            for(int i=0;i<NC;i++){
                int a=i+1, b=sig[i]+1;
                if(a==b) continue;
                if(!eq) cl(-a,b,0,0); else cl(-eq,-a,b,0);
                int ne=newvar();
                if(!eq){ cl(-ne,-a,b,0); cl(-ne,a,-b,0); cl(ne,a,b,0); cl(ne,-a,-b,0); }
                else   { cl(-ne,eq,0,0); cl(-ne,-a,b,0); cl(-ne,a,-b,0);
                         cl5(ne,-eq,a,b,0); cl5(ne,-eq,-a,-b,0); }
                eq=ne;
            }
        }
        free(sig);
    }
    fclose(out);

    FILE *fin = fopen(tmp,"r"), *fout = fopen(path,"w");
    if(!fin||!fout){ perror("fopen"); return 3; }
    fprintf(fout,"c A280537 n=%d generated by plane4_gen.c\n", N);
    fprintf(fout,"p cnf %d %lld\n", nv, ncl);
    char buf[1<<16]; size_t r;
    while((r=fread(buf,1,sizeof buf,fin))>0) fwrite(buf,1,r,fout);
    fclose(fin); fclose(fout); remove(tmp);
    fprintf(stderr,"переменных %d, клауз %lld -> %s\n", nv, ncl, path);
    return 0;
}
