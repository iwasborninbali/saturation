/* verify_family.c — INDEPENDENT enumerator for the "orbits of a base group + prescribed half-turn pairs" families,
 * written from scratch to validate the solver's sym=2+PAIRS (even n, two-loop) and sym=9 (odd n) modes.
 * Configuration = union of whole base-group orbits together with the given half-turn pairs; 2n points;
 * two per row and per column; no three collinear (checked incrementally by forbidden-cell masks).
 * usage: verify_family n base pairspec      base: 4 = quarter turn (C4), 2 = half turn
 *        pairspec like "1,1;4,31"  (each entry c is one cell; its half-turn image is added automatically) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64;
static int n,m,np_pairs;
static u64 forb[40][64];
static int px[128],py[128],np;
static int rowc[64],colc[64];
static long long sols,nodes;
static int orb[4096][4], norb;
static int gcd_(int a,int b){while(b){int t=a%b;a=b;b=t;}return a<0?-a:a;}
static void mark_line(int L,int x1,int y1,int x2,int y2){
    int dx=x2-x1,dy=y2-y1,g=gcd_(dx,dy); if(!g)return; dx/=g; dy/=g;
    int x=x1,y=y1; while(x>=0&&x<n&&y>=0&&y<n){forb[L][x]|=1ULL<<y;x-=dx;y-=dy;}
    x=x1+dx;y=y1+dy; while(x>=0&&x<n&&y>=0&&y<n){forb[L][x]|=1ULL<<y;x+=dx;y+=dy;}
}
static int place(int L,int x,int y){
    if(forb[L][x]>>y&1ULL) return 0;
    for(int i=0;i<np;i++) mark_line(L,px[i],py[i],x,y);
    px[np]=x;py[np]=y;np++; return 1;
}
static int need_orbits;
static char usedorb[4096];
static int touches[64][4096], ntouch[64];
static void rec(int r,int start,int lvl){
    nodes++;
    if(r==n){ sols++; return; }
    if(rowc[r]==2){ rec(r+1,0,lvl); return; }
    for(int i=start;i<ntouch[r];i++){
        int o=touches[r][i];
        if(usedorb[o]) continue;
        int sr[4],sc[4],ok=1;
        for(int t=0;t<4;t++){int x=orb[o][t]/n,y=orb[o][t]%n; sr[t]=x; sc[t]=y; if(++rowc[x]>2||++colc[y]>2) ok=0;}
        if(ok){
            int savednp=np; memcpy(forb[lvl+1],forb[lvl],sizeof(u64)*n);
            int good=1;
            for(int t=0;t<4&&good;t++) good=place(lvl+1,orb[o][t]/n,orb[o][t]%n);
            if(good){ usedorb[o]=1; rec(r,i+1,lvl+1); usedorb[o]=0; }
            np=savednp;
        }
        for(int t=0;t<4;t++){rowc[sr[t]]--; colc[sc[t]]--;}
    }
}
int main(int argc,char**argv){
    if(argc<4){fprintf(stderr,"usage: verify_family n base pairspec\n");return 64;}
    n=atoi(argv[1]); int base=atoi(argv[2]); m=n-1;
    int pc[16],npc=0; { char buf[512]; strncpy(buf,argv[3],511); buf[511]=0;
      for(char*tok=strtok(buf,";");tok;tok=strtok(0,";")){int x,y; if(sscanf(tok,"%d,%d",&x,&y)==2){pc[npc++]=x*n+y; pc[npc++]=(m-x)*n+(m-y);} } }
    char used[4096]; memset(used,0,sizeof(used));
    for(int i=0;i<npc;i++) used[pc[i]]=2;
    /* build orbits of the base group */
    for(int c=0;c<n*n;c++){
        if(used[c]) continue;
        int o[8],k=0,z=c; 
        for(int t=0;t<4;t++){ o[k++]=z; int x=z/n,y=z%n; z = (base==4)? (y*n+(m-x)) : ((m-x)*n+(m-y)); if(z==c) break; }
        int bad=0; for(int t=0;t<k;t++) if(used[o[t]]) bad=1;
        if(bad||k!=4){ for(int t=0;t<k;t++) used[o[t]]=1; continue; }
        for(int t=0;t<k;t++) used[o[t]]=1;
        for(int t=0;t<4;t++) orb[norb][t]=o[t];
        norb++;
    }
    memset(forb,0,sizeof(forb)); memset(rowc,0,sizeof(rowc)); memset(colc,0,sizeof(colc)); np=0;
    for(int i=0;i<npc;i++){ int x=pc[i]/n,y=pc[i]%n; rowc[x]++; colc[y]++; if(!place(0,x,y)){printf("n=%d pairs invalid\n",n); return 0;} }
    need_orbits=(2*n-npc)/4;
    if((2*n-npc)%4){ printf("n=%d base=%d: %d points cannot be filled by size-4 orbits\n",n,base,2*n-npc); return 0; }
    for(int o=0;o<norb;o++) for(int t=0;t<4;t++){int r=orb[o][t]/n; int dup=0; for(int j=0;j<ntouch[r];j++) if(touches[r][j]==o) dup=1; if(!dup) touches[r][ntouch[r]++]=o;}
    rec(0,0,0);
    printf("n=%d base=%d pairs=%s: orbits=%d need=%d INDEPENDENT solutions=%lld nodes=%lld\n",n,base,argv[3],norb,need_orbits,sols,nodes);
    return 0;
}
