/* dump_configs2d.c — выгрузить ВСЕ правильные расстановки заданных размеров.
 * ЗАЧЕМ: чтобы искать отличительный признак, нужен полный материал, а не выборка:
 * признак, найденный на выборке, может оказаться признаком выборки.
 * СБОРКА: cc -O3 -o dump_configs2d dump_configs2d.c ; ЗАПУСК: ./dump_configs2d <n> <k_min>
 */
#include <stdio.h>
#include <stdlib.h>
static int n,N,KMIN;
static unsigned long long *LINE;
static int chosen[80];
static void dfs(int start,int k,unsigned long long dead){
    if(k>=KMIN){ printf("%d",k); for(int t=0;t<k;t++) printf(" %d",chosen[t]); printf("\n"); }
    for(int c=start;c<N;c++){
        if((dead>>c)&1ULL) continue;
        unsigned long long nd=dead|(1ULL<<c);
        for(int t=0;t<k;t++) nd|=LINE[(size_t)c*N+chosen[t]];
        chosen[k]=c; dfs(c+1,k+1,nd);
    }
}
int main(int argc,char**argv){
    n=atoi(argv[1]); N=n*n; KMIN=atoi(argv[2]);
    if(N>64){fprintf(stderr,"n>8\n");return 2;}
    LINE=malloc((size_t)N*N*sizeof(unsigned long long));
    for(int i=0;i<N;i++)for(int j=0;j<N;j++){
        unsigned long long m=0;
        if(i!=j){int xi=i%n,yi=i/n,xj=j%n,yj=j/n;
            for(int k=0;k<N;k++){int xk=k%n,yk=k/n;
                if((long long)(xj-xi)*(yk-yi)-(long long)(yj-yi)*(xk-xi)==0) m|=1ULL<<k;}}
        LINE[(size_t)i*N+j]=m;
    }
    dfs(0,0,0ULL); return 0;
}
