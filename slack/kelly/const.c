/* Первый момент Гая-Келли: точное число коллинеарных троек в сетке n x n,
   порог m*(n) из условия ln C(n^2,m) = T(n)*C(m,3)/C(n^2,3), и предел отношения порога к n. */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
static int g_[1<<11];
static long long gcdll(long long a,long long b){while(b){long long t=a%b;a=b;b=t;}return a;}
static double Tn(long long n){
  double t=0;
  for(long long dx=0;dx<n;dx++)
    for(long long dy=-(n-1);dy<n;dy++){
      if(dx==0&&dy<=0) continue;
      long long ay=dy<0?-dy:dy;
      long long g=gcdll(dx,ay);
      if(g>1) t+=(double)(n-dx)*(double)(n-ay)*(double)(g-1);
    }
  return t;
}
static double lnC(double N,double m){ return lgamma(N+1)-lgamma(m+1)-lgamma(N-m+1); }
int main(int c,char**v){
  for(int i=1;i<c;i++){
    long long n=atoll(v[i]); double N=(double)n*n, T=Tn(n);
    double lo=1.0*n, hi=2.5*n;
    for(int it=0;it<80;it++){
      double m=(lo+hi)/2;
      double val=lnC(N,m)-T*(m*(m-1)*(m-2))/(N*(N-1)*(N-2));
      if(val>0) lo=m; else hi=m;
    }
    printf("n=%8lld  T/n^4=%.6f  m*/n=%.7f\n",n,T/((double)n*n*n*n),lo/n);
    fflush(stdout);
  }
  return 0;
}
