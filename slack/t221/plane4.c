/* plane4.c — максимум точек в [n]^3 без четырёх компланарных (OEIS A280537).
 *
 * Переформулировка, делающая задачу однотипной с no-three-in-line:
 *   четыре точки компланарны  <=>  лежат в общей плоскости.
 *   Плоскость, содержащая <= 3 узла решётки, запретить ничего не может.
 *   => допустимость S  <=>  для КАЖДОЙ плоскости P с >= 4 узлами:  |S ∩ P| <= 3.
 * Это в точности форма «прямая, ёмкость 2», под которую у нас уже написан cube3.c.
 *
 * Следствие, используемое как граница ветвления: слой z=k сам является плоскостью
 * (n^2 >= 4 узлов при n >= 2), поэтому в каждом слое не более 3 точек и a(n) <= 3n.
 *
 * Режимы:
 *   plane4 n [best0]              полный перебор, доказательство оптимума
 *   ESTIMATE=k plane4 n best0     оценка размера дерева по k случайным спускам (Knuth 1975)
 *   PREFIX="z0mask z1mask" ...    (позже) распределение по префиксам
 * Первое число best0 — стартовый порог: перебор ищет строго больше best0.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 9
#define MAXC (MAXN*MAXN*MAXN)
#define W ((MAXC+63)/64)

static int N, NC;
typedef struct { uint64_t w[W]; } BS;
static inline void bs_zero(BS*b){memset(b->w,0,sizeof(b->w));}
static inline int  bs_get(const BS*b,int i){return (b->w[i>>6]>>(i&63))&1ULL;}
static inline void bs_set(BS*b,int i){b->w[i>>6]|=1ULL<<(i&63);}
static inline void bs_or(BS*a,const BS*b){for(int i=0;i<W;i++)a->w[i]|=b->w[i];}

/* ---- плоскости ---- */
static BS *pmask; static int nplanes, cap_planes;
static int **cell_pl; static int *cell_pl_n;   /* списки плоскостей через каждую ячейку */
static int *pcnt;                              /* сколько выбранных точек в плоскости */

static int gcd2(int a,int b){a=abs(a);b=abs(b);while(b){int t=a%b;a=b;b=t;}return a;}
static int gcd3(int a,int b,int c){return gcd2(gcd2(a,b),c);}

/* Плоскости перечисляются ПО ТРОЙКАМ УЗЛОВ, а не по коэффициентам.
   Причина — пойманная ошибка: нормаль есть векторное произведение разностей, её координаты
   доходят до 2(n-1)^2, и ограничение |a|,|b|,|c| <= n-1 теряло плоскости (например 6x-3y-4z=0
   при n=4).  Перебор троек не может потерять ни одной плоскости по построению. */
#define HB 22
static int *htab; static int *hkey_a,*hkey_b,*hkey_c,*hkey_d;
static int hn;
static int plane_id(int a,int b,int c,int d){
  int g=gcd3(a,b,c); a/=g;b/=g;c/=g;d/=g;
  if(a<0||(a==0&&(b<0||(b==0&&c<0)))){a=-a;b=-b;c=-c;d=-d;}
  unsigned h=((unsigned)(a*73856093)^(unsigned)(b*19349663)^(unsigned)(c*83492791)^(unsigned)(d*2654435761u));
  h&=(1u<<HB)-1;
  while(htab[h]>=0){int j=htab[h];
    if(hkey_a[j]==a&&hkey_b[j]==b&&hkey_c[j]==c&&hkey_d[j]==d) return j;
    h=(h+1)&((1u<<HB)-1);}
  htab[h]=hn; hkey_a[hn]=a;hkey_b[hn]=b;hkey_c[hn]=c;hkey_d[hn]=d; return hn++;
}
static void build_planes(void){
  int MAXP=1<<21;
  htab=malloc(sizeof(int)*(1<<HB)); for(int i=0;i<(1<<HB);i++)htab[i]=-1;
  hkey_a=malloc(sizeof(int)*MAXP);hkey_b=malloc(sizeof(int)*MAXP);
  hkey_c=malloc(sizeof(int)*MAXP);hkey_d=malloc(sizeof(int)*MAXP); hn=0;
  int *cntpts=calloc(MAXP,sizeof(int));
  int X[MAXC],Y[MAXC],Z[MAXC];
  for(int i=0;i<NC;i++){X[i]=i/(N*N);Y[i]=(i/N)%N;Z[i]=i%N;}
  /* первый проход: какие плоскости вообще возникают */
  for(int i=0;i<NC;i++)for(int j=i+1;j<NC;j++)for(int k=j+1;k<NC;k++){
    int ux=X[j]-X[i],uy=Y[j]-Y[i],uz=Z[j]-Z[i];
    int vx=X[k]-X[i],vy=Y[k]-Y[i],vz=Z[k]-Z[i];
    int a=uy*vz-uz*vy, b=uz*vx-ux*vz, c=ux*vy-uy*vx;
    if(!a&&!b&&!c) continue;                 /* три точки коллинеарны — плоскость не определена */
    int d=a*X[i]+b*Y[i]+c*Z[i];
    int id=plane_id(a,b,c,d);
    if(id<MAXP) cntpts[id]=1;
  }
  /* второй проход: маски и отбор плоскостей с >= 4 узлами */
  pmask=malloc(sizeof(BS)*hn); int cnt=0;
  int *keep=malloc(sizeof(int)*hn);
  for(int p=0;p<hn;p++){
    BS m; bs_zero(&m); int k=0;
    for(int i=0;i<NC;i++) if(hkey_a[p]*X[i]+hkey_b[p]*Y[i]+hkey_c[p]*Z[i]==hkey_d[p]){bs_set(&m,i);k++;}
    if(k>=4){ pmask[cnt]=m; keep[cnt]=p; cnt++; }
  }
  nplanes=cnt; free(keep); free(cntpts);
  cell_pl_n=calloc(NC,sizeof(int));
  for(int p=0;p<nplanes;p++)for(int i=0;i<NC;i++) if(bs_get(&pmask[p],i)) cell_pl_n[i]++;
  cell_pl=malloc(sizeof(int*)*NC);
  int *fill=calloc(NC,sizeof(int));
  for(int i=0;i<NC;i++) cell_pl[i]=malloc(sizeof(int)*cell_pl_n[i]);
  for(int p=0;p<nplanes;p++)for(int i=0;i<NC;i++) if(bs_get(&pmask[p],i)) cell_pl[i][fill[i]++]=p;
  free(fill);
  pcnt=calloc(nplanes,sizeof(int));
}

/* ---- перебор ---- */
static int best, sel[MAXC], nsel, bestsel[MAXC], nbest;
static long long nodes;
static int estimate_dives=0; static double est_total=0;
static unsigned long long rngs=88172645463325252ULL;
static inline unsigned long long rnd(void){rngs^=rngs<<13;rngs^=rngs>>7;rngs^=rngs<<17;return rngs;}

/* добавить точку i: вернуть 0, если нарушена ёмкость */
static int add_point(int i, BS *forb){
  for(int t=0;t<cell_pl_n[i];t++){
    int p=cell_pl[i][t];
    if(++pcnt[p]==3) bs_or(forb,&pmask[p]);
    else if(pcnt[p]>3){ for(int u=0;u<=t;u++) pcnt[cell_pl[i][u]]--; return 0; }
  }
  return 1;
}
static void del_point(int i){ for(int t=0;t<cell_pl_n[i];t++) pcnt[cell_pl[i][t]]--; }

/* перебор по слоям z-столбца: обходим ячейки в порядке индекса, но границу берём по слоям x */
static void dfs(int start, BS forb, int depth, double weight){
  nodes++;
  if(nsel>best){ best=nsel; nbest=nsel; memcpy(bestsel,sel,sizeof(int)*nsel); }
  /* граница: в каждом слое x=const не более 3 точек */
  int layer = start/(N*N);
  int bound = nsel + 3*(N-layer) - (nsel - 0);   /* заполняется ниже точнее */
  { int used_in_layer=0; for(int k=0;k<nsel;k++) if(sel[k]/(N*N)==layer) used_in_layer++;
    bound = nsel + (3-used_in_layer) + 3*(N-1-layer); }
  if(bound<=best) return;

  int cand[MAXC], nc=0;
  for(int i=start;i<NC;i++) if(!bs_get(&forb,i)) cand[nc++]=i;
  if(estimate_dives){                        /* оценщик Кнута: один случайный ребёнок */
    int live=0, pick=-1;
    for(int t=0;t<nc;t++){
      int i=cand[t]; BS f2=forb;
      if(!add_point(i,&f2)) continue;
      live++; if(rnd()%live==0) pick=i;
      del_point(i);
    }
    if(!live||pick<0){ return; }
    est_total += weight*live;
    BS f2=forb; add_point(pick,&f2); sel[nsel++]=pick;
    dfs(pick+1,f2,depth+1,weight*live);
    nsel--; del_point(pick);
    return;
  }
  for(int t=0;t<nc;t++){
    int i=cand[t];
    /* граница на остаток: сколько ещё можно добавить с позиции i */
    { int lay=i/(N*N), uil=0; for(int k=0;k<nsel;k++) if(sel[k]/(N*N)==lay) uil++;
      if(nsel + (3-uil) + 3*(N-1-lay) <= best) continue; }
    BS f2=forb;
    if(!add_point(i,&f2)) continue;
    sel[nsel++]=i;
    dfs(i+1,f2,depth+1,0);
    nsel--; del_point(i);
  }
}

int main(int argc,char**argv){
  N=atoi(argv[1]); NC=N*N*N;
  best = argc>2?atoi(argv[2]):0;
  const char*e=getenv("ESTIMATE"); if(e) estimate_dives=atoi(e);
  build_planes();
  fprintf(stderr,"n=%d: ячеек %d, богатых плоскостей %d\n",N,NC,nplanes);
  if(estimate_dives){
    double sum=0;
    for(int d=0;d<estimate_dives;d++){ est_total=1; BS f; bs_zero(&f); nsel=0; dfs(0,f,0,1.0); sum+=est_total; }
    printf("n=%d ESTIMATE dives=%d  среднее число узлов ~ %.4g\n",N,estimate_dives,sum/estimate_dives);
    return 0;
  }
  BS f; bs_zero(&f); nsel=0; nodes=0;
  dfs(0,f,0,0);
  printf("n=%d MAX=%d узлов=%lld\n",N,best,nodes);
  { int bad=0;
    for(int p=0;p<nbest;p++)for(int q=p+1;q<nbest;q++)for(int r=q+1;r<nbest;r++)for(int t=r+1;t<nbest;t++){
      int A=bestsel[p],B=bestsel[q],C=bestsel[r],D=bestsel[t];
      int ax=A/(N*N),ay=(A/N)%N,az=A%N;
      long ux=B/(N*N)-ax,uy=(B/N)%N-ay,uz=B%N-az;
      long vx=C/(N*N)-ax,vy=(C/N)%N-ay,vz=C%N-az;
      long wx=D/(N*N)-ax,wy=(D/N)%N-ay,wz=D%N-az;
      if(ux*(vy*wz-vz*wy)-uy*(vx*wz-vz*wx)+uz*(vx*wy-vy*wx)==0) bad++;
    }
    printf("  ПРОВЕРКА СВИДЕТЕЛЯ (все четвёрки, определители): компланарных %d %s\n",bad,bad?"— СВИДЕТЕЛЬ НЕВЕРЕН":"— чист");
    if(bad){ fprintf(stderr,"ОТКАЗ: свидетель не проходит независимую проверку\n"); return 2; }
  }
  printf("  свидетель:");
  for(int k=0;k<nbest;k++){int i=bestsel[k];printf(" (%d,%d,%d)",i/(N*N),(i/N)%N,i%N);}
  printf("\n");
  return 0;
}
