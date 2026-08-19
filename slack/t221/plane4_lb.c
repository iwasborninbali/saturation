/* plane4_lb.c — стохастический поиск конфигураций без четырёх компланарных (нижние границы A280537).
 * Метод: случайный жадный набор + «разрушь и почини», как в cube3_lb.c для коллинеарности.
 * Проверка встроена: найденное проверяется перебором ВСЕХ четвёрок определителями,
 * и без прохождения этой проверки ничего не печатается.
 * usage: plane4_lb n target seconds [seed]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static int N,NC,*X,*Y,*Z;
static unsigned long long rs=88172645463325252ULL;
static unsigned long long rnd(void){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs;}

static int coplanar(int a,int b,int c,int d){
  long ux=X[b]-X[a],uy=Y[b]-Y[a],uz=Z[b]-Z[a];
  long vx=X[c]-X[a],vy=Y[c]-Y[a],vz=Z[c]-Z[a];
  long wx=X[d]-X[a],wy=Y[d]-Y[a],wz=Z[d]-Z[a];
  return ux*(vy*wz-vz*wy)-uy*(vx*wz-vz*wx)+uz*(vx*wy-vy*wx)==0;
}
/* можно ли добавить p к набору s[0..k-1] */
static int ok_add(int*s,int k,int p){
  for(int i=0;i<k;i++)for(int j=i+1;j<k;j++)for(int l=j+1;l<k;l++)
    if(coplanar(s[i],s[j],s[l],p)) return 0;
  return 1;
}
int main(int argc,char**argv){
  N=atoi(argv[1]); int target=atoi(argv[2]); int secs=atoi(argv[3]);
  if(argc>4) rs=atoll(argv[4])*2654435761ULL+88172645463325252ULL;
  NC=N*N*N; X=malloc(4*NC);Y=malloc(4*NC);Z=malloc(4*NC);
  for(int i=0;i<NC;i++){X[i]=i/(N*N);Y[i]=(i/N)%N;Z[i]=i%N;}
  int *s=malloc(4*NC),*best=malloc(4*NC),bk=0,k=0;
  int *perm=malloc(4*NC);
  time_t t0=time(NULL); long long iters=0;
  while(time(NULL)-t0<secs){
    iters++;
    /* разрушение: оставить случайное подмножество текущего лучшего */
    k=0;
    if(bk>3){ int keep=bk-1-(int)(rnd()%3); if(keep<0)keep=0;
      for(int i=0;i<bk;i++) perm[i]=best[i];
      for(int i=bk-1;i>0;i--){int j=rnd()%(i+1);int t=perm[i];perm[i]=perm[j];perm[j]=t;}
      for(int i=0;i<keep;i++) s[k++]=perm[i];
    }
    /* починка: жадно добавлять в случайном порядке */
    for(int i=0;i<NC;i++) perm[i]=i;
    for(int i=NC-1;i>0;i--){int j=rnd()%(i+1);int t=perm[i];perm[i]=perm[j];perm[j]=t;}
    for(int i=0;i<NC;i++){ int p=perm[i]; int dup=0;
      for(int q=0;q<k;q++) if(s[q]==p){dup=1;break;}
      if(dup) continue;
      if(ok_add(s,k,p)) s[k++]=p;
    }
    if(k>bk){ bk=k; memcpy(best,s,4*k);
      fprintf(stderr,"  %d точек (итерация %lld)\n",bk,iters);
      if(bk>=target) break; }
  }
  /* независимая проверка перед печатью */
  int bad=0;
  for(int i=0;i<bk;i++)for(int j=i+1;j<bk;j++)for(int l=j+1;l<bk;l++)for(int m=l+1;m<bk;m++)
    if(coplanar(best[i],best[j],best[l],best[m])) bad++;
  printf("n=%d: НАЙДЕНО %d точек, компланарных четвёрок %d %s\n",N,bk,bad,bad?"— НЕВЕРНО":"— чисто");
  if(!bad){ printf("  "); for(int i=0;i<bk;i++) printf("(%d,%d,%d) ",X[best[i]],Y[best[i]],Z[best[i]]); printf("\n"); }
  return 0;
}
