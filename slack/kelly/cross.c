/* Где ln(предсказано) при m=2n переходит через ноль. Сканирование, НЕ двоичный поиск:
   функция немонотонна (растёт, потом падает), и двоичный поиск на ней даёт границу диапазона. */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
static long long gcdll(long long a,long long b){while(b){long long t=a%b;a=b;b=t;}return a;}
static double Tn(long long n){
  double t=0;
  for(long long dx=0;dx<n;dx++)
    for(long long dy=-(n-1);dy<n;dy++){
      if(dx==0&&dy<=0) continue;
      long long ay=dy<0?-dy:dy, g=gcdll(dx,ay);
      if(g>1) t+=(double)(n-dx)*(double)(n-ay)*(double)(g-1);
    }
  return t;
}
static double lnC(double N,double m){return lgamma(N+1)-lgamma(m+1)-lgamma(N-m+1);}
static double val(long long n){
  double N=(double)n*n,m=2.0*n,T=Tn(n);
  return lnC(N,m)-T*(m*(m-1)*(m-2))/(N*(N-1)*(N-2));
}
int main(int c,char**v){
  long long hi=c>1?atoll(v[1]):700;
  double prev=val(5); long long mx=5; double mxv=prev; int printed=0;
  for(long long n=6;n<=hi;n++){
    double x=val(n);
    if(x>mxv){mxv=x;mx=n;}
    if(prev>=0&&x<0){printf("ПЕРЕХОД: последнее n с положительным = %lld  (val=%.4f -> %.4f)\n",n-1,prev,x);printed=1;}
    prev=x;
  }
  printf("максимум при n=%lld (val=%.2f); значение при n=%lld: %.3f\n",mx,mxv,hi,prev);
  if(!printed) printf("перехода до n=%lld НЕТ\n",hi);
  return 0;
}
