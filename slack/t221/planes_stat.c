/* размер CNF-кодировки: сколько плоскостей какого размера и во что это выливается */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc,char**argv){int N=atoi(argv[1]);int NC=N*N*N;
  int *X=malloc(4*NC),*Y=malloc(4*NC),*Z=malloc(4*NC);
  for(int i=0;i<NC;i++){X[i]=i/(N*N);Y[i]=(i/N)%N;Z[i]=i%N;}
  long long tri=(long long)NC*(NC-1)*(NC-2)/6; int HB=1; while((1LL<<HB)<4*(tri+16))HB++;
  int *ht=malloc(4LL<<HB); for(long long i=0;i<(1LL<<HB);i++)ht[i]=-1;
  int cap=1<<20,hn=0,*ka=malloc(4*cap),*kb=malloc(4*cap),*kc=malloc(4*cap),*kd=malloc(4*cap);
  int g,a,b,c,d;
  #define GC(x,y) ({int A=abs(x),B=abs(y);while(B){int t=A%B;A=B;B=t;}A;})
  for(int i=0;i<NC;i++)for(int j=i+1;j<NC;j++)for(int k=j+1;k<NC;k++){
    int ux=X[j]-X[i],uy=Y[j]-Y[i],uz=Z[j]-Z[i],vx=X[k]-X[i],vy=Y[k]-Y[i],vz=Z[k]-Z[i];
    a=uy*vz-uz*vy;b=uz*vx-ux*vz;c=ux*vy-uy*vx; if(!a&&!b&&!c)continue;
    d=a*X[i]+b*Y[i]+c*Z[i]; g=GC(GC(a,b),c); a/=g;b/=g;c/=g;d/=g;
    if(a<0||(a==0&&(b<0||(b==0&&c<0)))){a=-a;b=-b;c=-c;d=-d;}
    unsigned h=((unsigned)(a*73856093)^(unsigned)(b*19349663)^(unsigned)(c*83492791)^(unsigned)(d*2654435761u));
    h&=(1u<<HB)-1;
    while(ht[h]>=0){int q=ht[h];if(ka[q]==a&&kb[q]==b&&kc[q]==c&&kd[q]==d)goto done;h=(h+1)&((1u<<HB)-1);}
    if(hn==cap){cap*=2;ka=realloc(ka,4*cap);kb=realloc(kb,4*cap);kc=realloc(kc,4*cap);kd=realloc(kd,4*cap);}
    ht[h]=hn;ka[hn]=a;kb[hn]=b;kc[hn]=c;kd[hn]=d;hn++;
    done:;
  }
  long long hist[200]={0}; long long rich=0, sumk=0, direct=0;
  for(int p=0;p<hn;p++){int k=0;
    for(int i=0;i<NC;i++) if(ka[p]*X[i]+kb[p]*Y[i]+kc[p]*Z[i]==kd[p])k++;
    if(k>=4){rich++;sumk+=k;if(k<200)hist[k]++;
      long long C=(long long)k*(k-1)*(k-2)*(k-3)/24; direct+=C;}
  }
  printf("n=%d: различных плоскостей %d, богатых %lld, суммарно инцидентностей %lld\n",N,hn,rich,sumk);
  printf("  число ВСЕХ компланарных четвёрок (прямая кодировка) = %lld\n",direct);
  printf("  распределение по размеру:"); for(int k=4;k<200;k++) if(hist[k]) printf(" %d:%lld",k,hist[k]);
  printf("\n");
  long long mixed=0, aux=0;
  for(int p=0;p<hn;p++){int k=0;
    for(int i=0;i<NC;i++) if(ka[p]*X[i]+kb[p]*Y[i]+kc[p]*Z[i]==kd[p])k++;
    if(k>=4){ if(k<=8) mixed += (long long)k*(k-1)*(k-2)*(k-3)/24; else { mixed += 4LL*k; aux += 4LL*k; } }}
  printf("  СМЕШАННАЯ кодировка (прямая при k<=8, счётчик при k>8): клауз ~%lld, доп.переменных ~%lld\n",mixed,aux);
  return 0;}
