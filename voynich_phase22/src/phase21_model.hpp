// CC BY-SA 4.0. Reuses phase-20 scoring helpers; original combined model:
// Hauer, Hayward & Kondrak (2014). New bounded open-vocabulary dynamic program.
#define main phase20_unused_main
#include "../../voynich_phase20/src/joint_solver.cpp"
#undef main
#include <sstream>

constexpr int UNKNOWN=1;
constexpr int MAX_UNKNOWN=24;
struct OpenEdge {int end,word;array<double,3> chars;double spelling,length;};
struct OpenModel : Model {
 vector<double> spelling,length;
 unordered_map<string,int> word_ids;
 void load_open(const string& dir){
  words={""};w1={0};w2.clear();w3.clear();trie={Trie()};
  ifstream input(dir+"/words.tsv");string s;double p;
  while(input>>s>>p){
   int id=words.size();words.push_back(s);w1.push_back(p);word_ids[s]=id;
   if(id==UNKNOWN){if(s!="<unk>")throw runtime_error("Expected unknown class first");continue;}
   if(s.size()>MAX_UNKNOWN)throw runtime_error("Dictionary word exceeds frozen length limit");
   int node=0;
   for(char c:s){int a=c-'a';if(a<0||a>=26)throw runtime_error("Invalid dictionary");
    if(trie[node].next[a]<0){int fresh=trie.size();trie[node].next[a]=fresh;trie.emplace_back();}
    node=trie[node].next[a];
   }trie[node].word=id;
  }
  if(words.size()<3||words.size()>=(1<<21))throw runtime_error("Invalid model");
  int a,b,c;ifstream bi(dir+"/bigrams.tsv"),tri(dir+"/trigrams.tsv");
  while(bi>>a>>b>>p)w2[paircode(a,b)]=p;
  while(tri>>a>>b>>c>>p)w3[triplecode(a,b,c)]=p;
  auto binary=[&](const string& name,int n){vector<double> v(n);ifstream f(dir+"/"+name,ios::binary);f.read((char*)v.data(),n*sizeof(double));if(!f)throw runtime_error("Missing model "+name);return v;};
  ch1=binary("char1.bin",27);ch2=binary("char2.bin",27*27);ch3=binary("char3.bin",27*27*27);
  spelling=binary("spelling.bin",28*28*28*27);length=binary("length.bin",MAX_UNKNOWN);
 }
 double spell(int a,int b,int c,int next)const{return spelling[((a*28+b)*28+c)*27+next];}
 double spell_word(const string& word)const{
  int a=27,b=27,c=27;double total=0;
  for(char ch:word){int d=ch-'a';total+=spell(a,b,c,d);a=b;b=c;c=d;}
  return total+spell(a,b,c,26);
 }
 vector<vector<OpenEdge>> graph(const string& text)const{
  vector<vector<OpenEdge>> result(text.size()+1);
  for(int i=0;i<(int)text.size();i++){
   int node=0,a=27,b=27,c=27;double sp=0;
   for(int j=i;j<(int)text.size()&&j<i+MAX_UNKNOWN;j++){
    int d=text[j]-'a';sp+=spell(a,b,c,d);a=b;b=c;c=d;
    if(node>=0)node=trie[node].next[d];
    int id=node>=0&&trie[node].word?trie[node].word:UNKNOWN;
    OpenEdge edge{j+1,id,{},sp+spell(a,b,c,26),length[j-i]};
    edge.chars[0]=char_add(text,i,j+1,0);
    if(i){edge.chars[1]=char_add(text,i,j+1,1);edge.chars[2]=char_add(text,i,j+1,2);}
    result[i].push_back(edge);
   }
  }return result;
 }
 double full_open(const string& segmented,double beta,double penalty)const{
  istringstream in(segmented);string word;int a=0,b=0,ca=-1,cb=-1;double lex=0,chars=0,emission=0;bool first=true;
  auto add=[&](int c){chars+=cs(ca,cb,c);ca=cb;cb=c;};
  while(in>>word){auto found=word_ids.find(word);int id=found==word_ids.end()?UNKNOWN:found->second;
   lex+=ws(a,b,id);a=b;b=id;
   if(id==UNKNOWN){if(word.size()>MAX_UNKNOWN)throw runtime_error("Unknown word too long");emission+=beta*spell_word(word)+length[word.size()-1]-penalty;}
   if(!first)add(26);first=false;for(char c:word)add(c-'a');
  }return (1-X)*lex+X*chars+emission;
 }
 Result segment_open(const string& text,double beta,double penalty,bool trace=true)const{
  auto edges=graph(text);
  struct State {int a,b,parent,begin;bool one;double score;};
  vector<State> states{{0,0,-1,0,false,0}};vector<vector<int>> at(text.size()+1);at[0].push_back(0);
  vector<unordered_map<uint64_t,int>> index(text.size()+1);
  for(int pos=0;pos<(int)text.size();pos++)for(int si:at[pos]){
   State current=states[si];int context=current.b?(current.one?1:2):0;
   double unknown_word_score=(1-X)*ws(current.a,current.b,UNKNOWN);
   for(const auto& e:edges[pos]){
    double word=e.word==UNKNOWN?unknown_word_score:(1-X)*ws(current.a,current.b,e.word);
    double value=current.score+word+X*e.chars[context];
    if(e.word==UNKNOWN)value+=beta*e.spelling+e.length-penalty;
    bool one=e.end-pos==1;
    // The previous span length is essential: two unknown surfaces can share
    // a word-class ID but leave different character histories at a boundary.
    uint64_t code=(paircode(current.b,e.word)<<1)|one;
    auto found=index[e.end].find(code);
    if(found==index[e.end].end()){
     int id=states.size();index[e.end][code]=id;at[e.end].push_back(id);
     states.push_back({current.b,e.word,si,pos,one,value});
    }else if(value>states[found->second].score){
     auto& old=states[found->second];old.score=value;old.parent=si;old.begin=pos;
    }
   }
  }
  if(at.back().empty())throw runtime_error("No segmentation");
  int best=at.back()[0];for(int id:at.back())if(states[id].score>states[best].score)best=id;
  if(!trace)return {states[best].score,""};
  vector<string> tokens;int end=text.size();
  for(int id=best;states[id].parent>=0;id=states[id].parent){int begin=states[id].begin;tokens.push_back(text.substr(begin,end-begin));end=begin;}
  reverse(tokens.begin(),tokens.end());string joined;
  for(const string& word:tokens){if(!joined.empty())joined+=' ';joined+=word;}
  if(abs(full_open(joined,beta,penalty)-states[best].score)>1e-8*text.size())throw runtime_error("DP/rescore mismatch");
  return {states[best].score,joined};
 }
};

