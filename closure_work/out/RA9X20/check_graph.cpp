// Independent exhaustive 24-vertex control verifier. No producer imports.
#include <array>
#include <iostream>
#include <algorithm>
#include <cstdint>
using namespace std;
array<uint32_t,24> adj{};
int minimum12=1000;
long long sets12=0;
void subsets(int next,int count,uint32_t chosen,int edges){
 if(count==12){sets12++;minimum12=min(minimum12,edges);return;}
 for(int v=next;v<=24-(12-count);v++)subsets(v+1,count+1,chosen|(1u<<v),edges+__builtin_popcount(adj[v]&chosen));
}
int alpha(uint32_t left){
 if(!left)return 0;
 int v=__builtin_ctz(left);left&=~(1u<<v);
 return max(alpha(left),1+alpha(left&~adj[v]));
}
int main(){
 array<unsigned,15> mask;for(auto &m:mask)if(!(cin>>m))return 2;
 auto edge=[](int u,int v){adj[u]|=1u<<v;adj[v]|=1u<<u;};
 for(int x=0;x<15;x++){
  for(int i=0;i<9;i++)if(mask[x]&(1u<<i))edge(i,x+9);
  for(int y=0;y<x;y++)if(!(mask[x]&mask[y]))edge(x+9,y+9);
 }
 bool triangle=false;int nonmax=0,degree=0;
 for(int u=0;u<24;u++){
  degree=max(degree,__builtin_popcount(adj[u]));
  for(int v=u+1;v<24;v++){
   if(adj[u]&(1u<<v)){if(adj[u]&adj[v])triangle=true;}
   else if(!(adj[u]&adj[v]))nonmax++;
  }
 }
 subsets(0,0,0,0);
 cout<<"{\"triangle_free\":"<<(triangle?"false":"true")<<",\"max_degree\":"<<degree<<",\"alpha\":"<<alpha((1u<<24)-1)<<",\"nonmaximal_pairs\":"<<nonmax<<",\"min_edges_12\":"<<minimum12<<",\"twelve_sets_checked\":"<<sets12<<"}\n";
}
