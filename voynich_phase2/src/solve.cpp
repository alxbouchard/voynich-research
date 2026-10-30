#include <algorithm>
#include <array>
#include <cmath>
#include <fstream>
#include <iostream>
#include <numeric>
#include <random>
#include <string>
#include <vector>
using namespace std;
struct Gram { array<int,4> s; int n; };
int code(array<int,4> a){return ((a[0]*26+a[1])*26+a[2])*26+a[3];}
int main(int argc,char**argv){
 if(argc<6)return 1;
 vector<double> lm(26*26*26*26);ifstream f(argv[1],ios::binary);f.read((char*)lm.data(),lm.size()*sizeof(double));if(!f)return 2;
 ifstream in(argv[2]);string line;array<long,26> freq{};vector<int> cnt(lm.size());long total=0;
 while(getline(in,line)){vector<int>s;for(char c:line)if(c>='a'&&c<='z'){s.push_back(c-'a');freq[c-'a']++;}
 for(size_t i=3;i<s.size();i++){cnt[code({s[i-3],s[i-2],s[i-1],s[i]})]++;total++;}}
 vector<Gram>g;array<vector<int>,26>index;
 for(int k=0;k<(int)cnt.size();k++)if(cnt[k]){int c=k;array<int,4>a;for(int i=3;i>=0;i--){a[i]=c%26;c/=26;}int j=g.size();g.push_back({a,cnt[k]});for(int s=0;s<26;s++)if(find(a.begin(),a.end(),s)!=a.end())index[s].push_back(j);}
 array<array<vector<int>,26>,26>affected;
 for(int a=0;a<26;a++)for(int b=a+1;b<26;b++){auto&v=affected[a][b];set_union(index[a].begin(),index[a].end(),index[b].begin(),index[b].end(),back_inserter(v));}
 auto value=[&](const Gram&x,const array<int,26>&key){return lm[code({key[x.s[0]],key[x.s[1]],key[x.s[2]],key[x.s[3]]})]*x.n;};
 auto score=[&](const array<int,26>&key){double v=0;for(auto&x:g)v+=value(x,key);return v;};
 int restarts=stoi(argv[3]),steps=stoi(argv[4]);mt19937 rng(stoul(argv[5]));uniform_real_distribution<double>unif(0,1);
 string rank="eitausnromclpdqvbfgxhzykjw"; // replaced by external unigram rank if supplied
 if(argc>6)rank=argv[6];if(rank.size()!=26){cerr<<"bad rank";return 3;}
 vector<int>order(26);iota(order.begin(),order.end(),0);sort(order.begin(),order.end(),[&](int a,int b){return freq[a]>freq[b];});
 array<int,26>base;for(int i=0;i<26;i++)base[order[i]]=rank[i]-'a';
 double best=-1e100;array<int,26>bestkey{};
 for(int run=0;run<restarts;run++){
  array<int,26>key=base;if(run)for(int j=0;j<8+run%12;j++)swap(key[rng()%26],key[rng()%26]);
  double current=score(key),localbest=current;array<int,26>localk=key;
  for(int step=0;step<steps;step++){
   int a=rng()%26,b=rng()%26;if(a==b)continue;if(a>b)swap(a,b);
   double old=0,newv=0;for(int j:affected[a][b])old+=value(g[j],key);
   swap(key[a],key[b]);for(int j:affected[a][b])newv+=value(g[j],key);
   double delta=newv-old;
   double temp=(0.002*total)*pow(0.001,(double)step/steps);
   if(delta>=0||unif(rng)<exp(delta/max(temp,1e-9)))current+=delta;else swap(key[a],key[b]);
   if(current>localbest){localbest=current;localk=key;}
  }
  // Final exact local ascent to remove annealing noise.
  key=localk;current=score(key);bool improved=true;
  while(improved){improved=false;for(int a=0;a<26;a++)for(int b=a+1;b<26;b++){
   double old=0,nv=0;for(int j:affected[a][b])old+=value(g[j],key);swap(key[a],key[b]);for(int j:affected[a][b])nv+=value(g[j],key);
   if(nv>old+1e-8){current+=nv-old;improved=true;}else swap(key[a],key[b]);
  }}
  if(current>best){best=current;bestkey=key;}
 }
 cout<<"{\"key\":\"";for(int x:bestkey)cout<<char('a'+x);cout<<"\",\"training_cross_entropy_bits\":"<<-best/total<<",\"quadgrams\":"<<total<<",\"unique_quadgrams\":"<<g.size()<<",\"restarts\":"<<restarts<<",\"steps_per_restart\":"<<steps<<"}"<<endl;
}
