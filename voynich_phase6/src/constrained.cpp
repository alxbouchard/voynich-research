// Phase 6: hard greedy-segmentation feasibility on fitting adjacency only.
#include <algorithm>
#include <array>
#include <cassert>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <random>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
struct Gram {array<int,4> s;int n;};
int idx(array<int,4> a){return ((a[0]*32+a[1])*32+a[2])*32+a[3];}
int main(int argc,char**argv){
 if(argc!=10)return 1;
 array<string,32> vocab;ifstream vin(argv[9]);for(auto&v:vocab)vin>>v;if(!vin)return 6;
 bool forbidden[32][32]{};vector<int>safe;for(int i=0;i<32;i++)if(vocab[i].size()==2)safe.push_back(i);
 for(int a=0;a<32;a++)for(int b=0;b<32;b++)if(vocab[a].size()==1 && vocab[b].size()==1)for(int z:safe)if(vocab[a]+vocab[b]==vocab[z])forbidden[a][b]=true;
 if(safe.empty())return 7;
 vector<double>lm(32*32*32*32);ifstream f(argv[1],ios::binary);f.read((char*)lm.data(),lm.size()*sizeof(double));if(!f)return 2;
 array<double,32>q{};ifstream qin(argv[2]);for(auto&x:q)qin>>x;
 if(!qin)return 3;
 ifstream input(argv[3]);vector<vector<int>>lines;string line;int K=0;long N=0,T=0;
 while(getline(input,line)){istringstream ss(line);vector<int>v;int x;while(ss>>x){if(x<0||x>=64)return 4;v.push_back(x);K=max(K,x+1);}if(v.size()>=4){N+=v.size();T+=v.size()-3;lines.push_back(v);}}
 if(T==0)return 5;
 vector<long>freq(K);unordered_map<int,int>counts;vector<vector<long>>adj(K,vector<long>(K));
 for(auto&v:lines)for(size_t i=1;i<v.size();i++)adj[v[i-1]][v[i]]++;
 auto feasible=[&](const vector<int>&key){for(int a=0;a<K;a++)for(int b=0;b<K;b++)if(adj[a][b]&&forbidden[key[a]][key[b]])return false;return true;};
 long rejected_for_grammar=0;
 for(auto&v:lines){for(int x:v)freq[x]++;for(size_t i=3;i<v.size();i++)counts[((v[i-3]*64+v[i-2])*64+v[i-1])*64+v[i]]++;}
 vector<pair<int,int>>sorted(counts.begin(),counts.end());sort(sorted.begin(),sorted.end());
 vector<Gram>grams;vector<vector<int>>index(K);
 for(auto [c,n]:sorted){array<int,4>a;for(int i=3;i>=0;i--){a[i]=c%64;c/=64;}int j=grams.size();grams.push_back({a,n});for(int x=0;x<K;x++)if(find(a.begin(),a.end(),x)!=a.end())index[x].push_back(j);}
 vector<vector<vector<int>>>affected(K,vector<vector<int>>(K));
 for(int a=0;a<K;a++)for(int b=0;b<K;b++)set_union(index[a].begin(),index[a].end(),index[b].begin(),index[b].end(),back_inserter(affected[a][b]));
 int restarts=stoi(argv[4]),steps=stoi(argv[5]);mt19937 rng(stoul(argv[6]));double lambda=stod(argv[7]);double temp0=stod(argv[8]);
 uniform_real_distribution<double>u(0,1);discrete_distribution<int>letter(q.begin(),q.end());
 auto value=[&](int j,const vector<int>&key){auto&g=grams[j];return g.n*lm[idx({key[g.s[0]],key[g.s[1]],key[g.s[2]],key[g.s[3]]})];};
 auto pen=[&](long c,int a){return c?c*log2(c/(N*q[a])):0.;};
 auto full=[&](const vector<int>&key){double s=0;array<long,32>c{};for(int j=0;j<(int)grams.size();j++)s+=value(j,key);for(int x=0;x<K;x++)c[key[x]]+=freq[x];for(int a=0;a<32;a++)s-=lambda*pen(c[a],a);return s;};
 double best=-1e100;vector<int>bestkey;vector<double>run_scores;
 for(int run=0;run<restarts;run++){
  vector<int>key(K),order(K);iota(order.begin(),order.end(),0);
  sort(order.begin(),order.end(),[&](int a,int b){return freq[a]>freq[b];});
  if(run)shuffle(order.begin(),order.end(),rng);
  array<long,32>out{};
  for(int x:order){int chosen=0;double largest=-1e100;for(int a=0;a<32;a++){double deficit=N*q[a]-out[a];if(deficit>largest){largest=deficit;chosen=a;}}key[x]=chosen;out[chosen]+=freq[x];}
  for(int a=0;a<K;a++)for(int b=0;b<K;b++)if(adj[a][b]&&forbidden[key[a]][key[b]])key[a]=safe[rng()%safe.size()];
  assert(feasible(key));out={};for(int x=0;x<K;x++)out[key[x]]+=freq[x];
  double current=full(key),localbest=current;vector<int>localkey=key;
  auto proposal=[&](int x,int y,int a,double temp,bool greedy){
   int oldx=key[x],oldy=y>=0?key[y]:-1;int target=y>=0?oldy:a;
   if(target==oldx)return false;
   key[x]=target;if(y>=0)key[y]=oldx;bool valid=true;
   for(int z=0;z<K;z++){if((adj[x][z]&&forbidden[key[x]][key[z]])||(adj[z][x]&&forbidden[key[z]][key[x]]))valid=false;
    if(y>=0&&((adj[y][z]&&forbidden[key[y]][key[z]])||(adj[z][y]&&forbidden[key[z]][key[y]])))valid=false;}
   key[x]=oldx;if(y>=0)key[y]=oldy;
   if(!valid){rejected_for_grammar++;return false;}
   auto&indices=y>=0?affected[x][y]:index[x];double before=0,after=0;
   for(int j:indices)before+=value(j,key);
   long cx=out[oldx],ct=out[target];double oldpen=pen(cx,oldx)+pen(ct,target);
   key[x]=target;out[oldx]-=freq[x];out[target]+=freq[x];
   if(y>=0){key[y]=oldx;out[target]-=freq[y];out[oldx]+=freq[y];}
   for(int j:indices)after+=value(j,key);
   double delta=after-before-lambda*(pen(out[oldx],oldx)+pen(out[target],target)-oldpen);
   bool accept=delta>1e-8||(!greedy&&u(rng)<exp(delta/max(temp,1e-12)));
   if(accept)current+=delta;
   else {key[x]=oldx;if(y>=0)key[y]=oldy;out[oldx]=cx;out[target]=ct;}
   return accept;
  };
  for(int step=0;step<steps;step++){
   int x=rng()%K;
   double temp=temp0*N*pow(0.001,(double)step/steps);
   if(u(rng)<.35){int y=rng()%K;if(x!=y)proposal(x,y,0,temp,false);}
   else proposal(x,-1,rng()%32,temp,false);
   if(current>localbest){localbest=current;localkey=key;}
   if(step%20000==0)assert(abs(current-full(key))<1e-6*N);
  }
  key=localkey;out={};for(int x=0;x<K;x++)out[key[x]]+=freq[x];current=full(key);
  for(int pass=0;pass<8;pass++){bool changed=false;for(int x=0;x<K;x++)for(int a=0;a<32;a++)changed=proposal(x,-1,a,0,true)||changed;for(int x=0;x<K;x++)for(int y=x+1;y<K;y++)changed=proposal(x,y,0,0,true)||changed;if(!changed)break;}
  assert(abs(current-full(key))<1e-6*N);assert(feasible(key));run_scores.push_back(current);
  if(current>best){best=current;bestkey=key;}
 }
 assert(feasible(bestkey));
 cout<<setprecision(15)<<"{\"training_feasible\":true,\"grammar_rejected_proposals\":"<<rejected_for_grammar<<",\"key\":[";for(size_t i=0;i<bestkey.size();i++){if(i)cout<<",";cout<<bestkey[i];}
 cout<<"],\"training_objective\":"<<best<<",\"symbols\":"<<K<<",\"training_chars\":"<<N<<",\"quadgrams\":"<<T<<",\"restarts\":"<<restarts<<",\"steps\":"<<steps<<",\"lambda\":"<<lambda<<",\"restart_objectives\":[";
 for(size_t i=0;i<run_scores.size();i++){if(i)cout<<',';cout<<run_scores[i];}cout<<"]}"<<endl;
}
