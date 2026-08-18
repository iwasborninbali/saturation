/* vp_lines.c — vertical-pair model (k=-1): enumerate all collinear triples of the doubled point set (both copies of every class),
   output E and the sparse coefficient list of the quadratic form T(eps) = E + eps^T C eps.
   Conventions = slack/vp_quadratic.py: class a in F_p^*, hyperbola hyp=+1: base (X(a), Y(1/a)), column X(a) + r_a p; hyp=-1: base
   (X(a), Y(-1/a)), column X(a) + (1-r_a) p; both rows y, y+p present. eps_a = (-1)^{r_a}. Required sign of a point: (-1)^c where c = r_a (column X+cp for hyp=+1, X+(1-c)p for hyp=-1).
   A collinear triple with n distinct variables (consistent signs) contributes 1/2^n to E and s_a s_b/2^n to the coefficient of eps_a eps_b.
   usage: vp_lines p > out.txt   (lines: "E value" then "a b coef" for a<b, coef of eps_a eps_b; also "odd" diagnostics)
   O(n^2 log n) with n = 8(p-1): per point, sort directions to the higher-indexed points. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
static ll gcdl(ll a, ll b){ if(a<0)a=-a; if(b<0)b=-b; while(b){ll t=a%b;a=b;b=t;} return a; }
typedef struct { ll dx, dy; int j; } Dir;
static int cmpdir(const void*A,const void*B){ const Dir*a=A,*b=B; if(a->dx!=b->dx) return a->dx<b->dx?-1:1; if(a->dy!=b->dy) return a->dy<b->dy?-1:1; return a->j-b->j; }
static ll modinv(ll a, ll p){ ll t=0,nt=1,r=p,nr=a%p; while(nr){ ll q=r/nr, tmp; tmp=t-q*nt;t=nt;nt=tmp; tmp=r-q*nr;r=nr;nr=tmp;} if(t<0)t+=p; return t; }
int main(int argc,char**argv){
  ll p=atoll(argv[1]); ll h=(p-1)/2; int n=8*(int)(p-1);
  ll *px=malloc(n*sizeof(ll)), *py=malloc(n*sizeof(ll)); int *pa=malloc(n*sizeof(int)), *ps=malloc(n*sizeof(int));
  int idx=0;
  for(ll a=1;a<p;a++){ ll ia=modinv(a,p); ll Xa = a<=h? a : a-p;
    for(int hyp=1;hyp>=-1;hyp-=2){ ll v = hyp==1? ia : (p-ia)%p; ll Yv = v? v : p; /* Y(u): u if u!=0 else p, u in [0,p) */
      for(int c=0;c<2;c++) for(int s=0;s<2;s++){ px[idx]=Xa + (hyp==1? c:1-c)*p; py[idx]=Yv + s*p; pa[idx]=(int)a; ps[idx]=(c?-1:1); idx++; } } }
  /* coefficient accumulation in a hash: key (a,b) a<b -> double; also E */
  int m=(int)(p-1); double E=0; 
  /* dense (p-1)^2 doubles: p=4001 -> 16M*8=128MB ok */
  double *C=calloc((size_t)m*m,sizeof(double)); double odd=0;
  Dir *dirs=malloc(n*sizeof(Dir));
  for(int i=0;i<n;i++){ int cnt=0;
    for(int j=i+1;j<n;j++){ ll dx=px[j]-px[i], dy=py[j]-py[i]; ll g=gcdl(dx,dy); dx/=g; dy/=g; if(dx<0||(dx==0&&dy<0)){dx=-dx;dy=-dy;} dirs[cnt].dx=dx;dirs[cnt].dy=dy;dirs[cnt].j=j;cnt++; }
    qsort(dirs,cnt,sizeof(Dir),cmpdir);
    int k=0; while(k<cnt){ int l=k; while(l<cnt && dirs[l].dx==dirs[k].dx && dirs[l].dy==dirs[k].dy) l++;
      int g=l-k; if(g>=2){ /* points i, dirs[k..l-1].j collinear; enumerate pairs among the g others: triple (i, j1, j2) — each triple counted once (i is min index) */
        for(int u=k;u<l;u++) for(int v=u+1;v<l;v++){ int t[3]={i,dirs[u].j,dirs[v].j};
          /* distinct variables with consistent signs */
          int va[3],vs[3],nv=0,bad=0;
          for(int q=0;q<3;q++){ int a=pa[t[q]], s=ps[t[q]]; int f=-1; for(int r=0;r<nv;r++) if(va[r]==a) f=r;
            if(f<0){va[nv]=a;vs[nv]=s;nv++;} else if(vs[f]!=s) bad=1; }
          if(bad) continue;
          double w=1.0/(1<<nv); E+=w;
          for(int q=0;q<nv;q++) for(int r=q+1;r<nv;r++){ int a=va[q],b=va[r]; double val=vs[q]*vs[r]*w; if(a>b){int tt=a;a=b;b=tt;} C[(size_t)(a-1)*m+(b-1)]+=val; }
          if(nv%2==1){ /* odd monomials: linear (nv=1: eps_a) or cubic (nv=3) — should cancel globally */
            for(int q=0;q<nv;q++) odd+=vs[q]*w; }
        } }
      k=l; } }
  printf("E %.6f\nodd_lin_sum %.6f\n",E,odd);
  for(int a=0;a<m;a++) for(int b=a+1;b<m;b++) if(C[(size_t)a*m+b]!=0.0) printf("%d %d %.6f\n",a+1,b+1,C[(size_t)a*m+b]);
  return 0; }
