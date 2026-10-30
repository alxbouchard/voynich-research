// CC BY-SA 4.0. Combined scoring follows Hauer, Hayward & Kondrak (2014).
// New implementation: bijective annealing initializer, then exact or greedy
// segmentation during key refinement. Not a reproduction of their MCTS.
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <random>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
using Key = array<int,26>;
constexpr double WL[] = {.129793302623898,.226872659329747,.643334038046355};
constexpr double CL[] = {.0950848948641174,.229797965264228,.675117139871655};
constexpr double X=.05;
uint64_t paircode(int a,int b){return (uint64_t(a)<<32)|uint32_t(b);}
uint64_t triplecode(int a,int b,int c){return (uint64_t(a)<<42)|(uint64_t(b)<<21)|c;}
string keytext(const Key& k){string s;for(int x:k)s+=char('a'+x);return s;}
string readletters(const string& file){ifstream f(file);if(!f)throw runtime_error("Missing input");string s,t;while(f>>t)s+=t;for(char c:s)if(c<'a'||c>'z')throw runtime_error("Nonalphabetic input");if(s.empty())throw runtime_error("Empty input");return s;}
struct Trie {array<int,26> next;int word=0;Trie(){next.fill(-1);}};
struct Result {double score;string text;};
struct Edge {int end,word;array<double,3> chars;};
struct Model {
 vector<string> words{""};vector<double> w1{0},ch1,ch2,ch3,quad,freq;
 unordered_map<uint64_t,double> w2,w3;vector<Trie> trie{Trie()};
 void load(const string& dir){
  ifstream w(dir+"/words.tsv");string s;double p;while(w>>s>>p){int id=words.size();words.push_back(s);w1.push_back(p);int node=0;for(char c:s){int a=c-'a';if(a<0||a>=26)throw runtime_error("Invalid dictionary");if(trie[node].next[a]<0){int fresh=trie.size();trie[node].next[a]=fresh;trie.emplace_back();}node=trie[node].next[a];}trie[node].word=id;}
  if(words.size()<27||words.size()>=(1<<21))throw runtime_error("Invalid vocabulary size");
  int a,b,c;ifstream bi(dir+"/bigrams.tsv"),tri(dir+"/trigrams.tsv");while(bi>>a>>b>>p)w2[paircode(a,b)]=p;while(tri>>a>>b>>c>>p)w3[triplecode(a,b,c)]=p;
  auto binary=[&](const string& name,int n){vector<double> v(n);ifstream f(dir+"/"+name,ios::binary);f.read((char*)v.data(),n*sizeof(double));if(!f)throw runtime_error("Missing/truncated model "+name);return v;};
  ch1=binary("char1.bin",27);ch2=binary("char2.bin",27*27);ch3=binary("char3.bin",27*27*27);quad=binary("quad.bin",26*26*26*26);freq=binary("freq.bin",26);
 }
 double cs(int a,int b,int c)const {double p=CL[0]*ch1[c];if(b>=0)p+=CL[1]*ch2[b*27+c];if(a>=0)p+=CL[2]*ch3[(a*27+b)*27+c];return log(p);}
 double ws(int a,int b,int c)const {double p=WL[0]*w1[c];auto bi=w2.find(paircode(b,c));if(b&&bi!=w2.end())p+=WL[1]*bi->second;auto tri=w3.find(triplecode(a,b,c));if(a&&tri!=w3.end())p+=WL[2]*tri->second;return log(p);}
 double char_add(const string& text,int begin,int end,int context)const {
  int a=-1,b=-1;double sum=0;
  auto add=[&](int c){sum+=cs(a,b,c);a=b;b=c;};
  if(context){b=text[begin-1]-'a';if(begin>=2)a=context==1?26:text[begin-2]-'a';add(26);}
  for(int i=begin;i<end;i++)add(text[i]-'a');return sum;
 }
 vector<vector<Edge>> edges(const string& text)const {
  vector<vector<Edge>> out(text.size()+1);
  for(int i=0;i<(int)text.size();i++){int node=0;for(int j=i;j<(int)text.size();j++){node=trie[node].next[text[j]-'a'];if(node<0)break;int id=trie[node].word;if(id){Edge e{j+1,id,{}};e.chars[0]=char_add(text,i,j+1,0);if(i){e.chars[1]=char_add(text,i,j+1,1);e.chars[2]=char_add(text,i,j+1,2);}out[i].push_back(e);}}if(out[i].empty())throw runtime_error("Missing single-letter fallback");}
  return out;
 }
 double full(const vector<int>& tokens)const {
  int a=0,b=0,ca=-1,cb=-1;double word=0,chars=0;bool first=true;
  auto add=[&](int c){chars+=cs(ca,cb,c);ca=cb;cb=c;};
  for(int id:tokens){word+=ws(a,b,id);a=b;b=id;if(!first)add(26);first=false;for(char c:words[id])add(c-'a');}
  return (1-X)*word+X*chars;
 }
 Result segment(const string& text,bool exact,bool trace=true)const {
  auto graph=edges(text);vector<int> tokens;
  if(!exact){
   function<void(int,int)> visit=[&](int lo,int hi){if(lo==hi)return;int bestlen=-1,start=-1,word=0;
    for(int i=lo;i<hi;i++)for(const auto& e:graph[i])if(e.end<=hi&&e.end-i>bestlen){bestlen=e.end-i;start=i;word=e.word;}
    if(start<0)throw runtime_error("No greedy path");visit(lo,start);tokens.push_back(word);visit(start+bestlen,hi);
   };visit(0,text.size());
  }else{
   struct State {int a,b,parent;double score;};
   vector<State> states{{0,0,-1,0}};vector<vector<int>> at(text.size()+1);at[0].push_back(0);
   vector<unordered_map<uint64_t,int>> index(text.size()+1);
   for(int pos=0;pos<(int)text.size();pos++)for(int si:at[pos]){
    // Copy before push_back can invalidate references to states.
    State current=states[si];int context=current.b?(words[current.b].size()==1?1:2):0;
    for(const auto& e:graph[pos]){double value=current.score+(1-X)*ws(current.a,current.b,e.word)+X*e.chars[context];uint64_t code=paircode(current.b,e.word);auto found=index[e.end].find(code);
     if(found==index[e.end].end()){int id=states.size();index[e.end][code]=id;at[e.end].push_back(id);states.push_back({current.b,e.word,si,value});}
     else if(value>states[found->second].score){auto& old=states[found->second];old.score=value;old.parent=si;}
    }
   }
   if(at.back().empty())throw runtime_error("No exact path");int best=at.back()[0];for(int id:at.back())if(states[id].score>states[best].score)best=id;
   if(!trace)return {states[best].score,""};
   for(int id=best;states[id].parent>=0;id=states[id].parent)tokens.push_back(states[id].b);reverse(tokens.begin(),tokens.end());
   if(abs(full(tokens)-states[best].score)>1e-8*text.size())throw runtime_error("DP/rescore mismatch");
  }
  string joined;for(int id:tokens){if(!joined.empty())joined+=' ';joined+=words[id];}return {full(tokens),joined};
 }
};
string decode(const string& text,const Key& key){string s=text;for(char& c:s)c='a'+key[c-'a'];return s;}
void emit(const Result& r){cout<<"{\"score\":"<<r.score<<",\"segmentation\":\""<<r.text<<"\"}";}
int main(int argc,char**argv){try{
 if(argc<5)throw runtime_error("Expected MODEL MODE INPUT PARAMETERS");cout<<setprecision(17);Model m;m.load(argv[1]);string mode=argv[2],cipher=readletters(argv[3]);
 if(mode=="segment"){emit(m.segment(cipher,string(argv[4])=="exact"));cout<<'\n';return 0;}
 if(mode=="init"){
  if(argc!=7)throw runtime_error("init expects seed restarts steps");mt19937 rng(stoul(argv[4]));int restarts=stoi(argv[5]),steps=stoi(argv[6]);uniform_real_distribution<double> u(0,1);
  array<int,26> counts{};for(char c:cipher)counts[c-'a']++;Key order,plain;iota(order.begin(),order.end(),0);iota(plain.begin(),plain.end(),0);
  stable_sort(order.begin(),order.end(),[&](int a,int b){return counts[a]>counts[b];});stable_sort(plain.begin(),plain.end(),[&](int a,int b){return m.freq[a]>m.freq[b];});
  vector<array<int,4>> grams;for(int i=3;i<(int)cipher.size();i++)grams.push_back({cipher[i-3]-'a',cipher[i-2]-'a',cipher[i-1]-'a',cipher[i]-'a'});
  array<array<vector<int>,26>,26> affected;
  for(int a=0;a<26;a++)for(int b=a+1;b<26;b++)for(int i=0;i<(int)grams.size();i++){auto g=grams[i];if(find(g.begin(),g.end(),a)!=g.end()||find(g.begin(),g.end(),b)!=g.end())affected[a][b].push_back(i);}
  auto term=[&](const array<int,4>& g,const Key& k){return m.quad[((k[g[0]]*26+k[g[1]])*26+k[g[2]])*26+k[g[3]]];};
  auto full=[&](const Key& k){double s=0;for(const auto& g:grams)s+=term(g,k);return s;};
  vector<pair<double,Key>> outcomes;
  for(int r=0;r<restarts;r++){
   Key key;for(int i=0;i<26;i++)key[order[i]]=plain[i];if(r)shuffle(key.begin(),key.end(),rng);
   double current=full(key),best=current;Key bestkey=key;
   auto swap_delta=[&](int a,int b){double before=0,after=0;for(int i:affected[a][b])before+=term(grams[i],key);swap(key[a],key[b]);for(int i:affected[a][b])after+=term(grams[i],key);return after-before;};
   for(int step=0;step<steps;step++){int a=rng()%26,b=rng()%26;if(a==b)continue;if(a>b)swap(a,b);double delta=swap_delta(a,b);double temp=.02*cipher.size()*pow(.0001,double(step)/steps);if(delta>=0||u(rng)<exp(delta/temp))current+=delta;else swap(key[a],key[b]);if(current>best){best=current;bestkey=key;}}
   key=bestkey;current=full(key);for(int pass=0;pass<8;pass++){bool changed=false;for(int a=0;a<26;a++)for(int b=a+1;b<26;b++){double d=swap_delta(a,b);if(d>1e-9){current+=d;changed=true;}else swap(key[a],key[b]);}if(!changed)break;}
   outcomes.push_back({full(key),key});
  }
  stable_sort(outcomes.begin(),outcomes.end(),[](auto&a,auto&b){return a.first>b.first;});cout<<"{\"restarts\":[";for(int i=0;i<(int)outcomes.size();i++){if(i)cout<<',';cout<<"{\"score\":"<<outcomes[i].first<<",\"key\":\""<<keytext(outcomes[i].second)<<"\"}";}cout<<"]}\n";return 0;
 }
 if(mode=="exact"||mode=="greedy"){
  if(argc!=6)throw runtime_error("refine expects key-list passes");ifstream keys(argv[4]);if(!keys)throw runtime_error("Missing starting keys");int passes=stoi(argv[5]);bool exact=mode=="exact";string s;double global=-INFINITY;Key globalkey{};vector<double> final;long evaluations=0;
  auto score=[&](const Key& k){evaluations++;return m.segment(decode(cipher,k),exact,false).score;};
  while(keys>>s){if(s.size()!=26)throw runtime_error("Invalid key length");Key key;array<bool,26> seen{};for(int i=0;i<26;i++){key[i]=s[i]-'a';if(key[i]<0||key[i]>=26||seen[key[i]])throw runtime_error("Key is not a permutation");seen[key[i]]=true;}
   double current=score(key);for(int pass=0;pass<passes;pass++){Key bestkey=key;double best=current;for(int a=0;a<26;a++)for(int b=a+1;b<26;b++){swap(key[a],key[b]);double value=score(key);if(value>best+1e-9){best=value;bestkey=key;}swap(key[a],key[b]);}if(best<=current+1e-9)break;key=bestkey;current=best;}
   final.push_back(current);if(current>global){global=current;globalkey=key;}
  }
  if(final.empty())throw runtime_error("No initial keys");cout<<"{\"key\":\""<<keytext(globalkey)<<"\",\"evaluations\":"<<evaluations<<",\"final_start_scores\":[";for(int i=0;i<(int)final.size();i++){if(i)cout<<',';cout<<final[i];}cout<<"],\"fit\":";emit(m.segment(decode(cipher,globalkey),exact));cout<<"}\n";return 0;
 }
 throw runtime_error("Unknown mode");
}catch(const exception& e){cerr<<e.what()<<'\n';return 2;}}
