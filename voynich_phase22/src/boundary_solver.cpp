// CC BY-SA 4.0. Phase-21 model retained; only conservative segmentation changes.
#include "phase21_model.hpp"

struct BoundaryResult {Result output,baseline;vector<int> added;};
struct BoundaryModel : OpenModel {
 vector<double> p2;unordered_map<uint32_t,double> p3;
 void load_boundary(const string& folder){
  load_open(folder);p2.resize(27*27*27*27);
  ifstream binary(folder+"/boundary2.bin",ios::binary);
  binary.read((char*)p2.data(),p2.size()*sizeof(double));if(!binary)throw runtime_error("Missing boundary model");
  ifstream table(folder+"/boundary3.tsv");if(!table)throw runtime_error("Missing boundary context table");
  uint32_t key;double prob;while(table>>key>>prob)p3[key]=prob;
 }
 vector<double> probabilities(const string& text)const{
  vector<double> result(text.size()+1,0.);
  for(int gap=1;gap<(int)text.size();gap++){
   uint32_t code=0;
   for(int j=gap-3;j<gap+3;j++)code=code*27+(j<0||j>=(int)text.size()?26:text[j]-'a');
   auto it=p3.find(code);result[gap]=it==p3.end()?p2[(code/27)%(27*27*27*27)]:it->second;
   if(!(result[gap]>0&&result[gap]<1))throw runtime_error("Invalid boundary probability");
  }return result;
 }
 static vector<bool> cuts(const string& segmented,int n){
  vector<bool> result(n+1,false);result[0]=result[n]=true;int pos=0;
  for(char c:segmented){if(c==' ')result[pos]=true;else pos++;}
  if(pos!=n)throw runtime_error("Changed decoded letters");return result;
 }
 double full_boundary(const string& segmented,const vector<bool>& original,const vector<double>& probs,double weight,double threshold)const{
  auto predicted=cuts(segmented,original.size()-1);double score=full_open(segmented,1.,0.);
  for(int i=1;i<(int)original.size()-1;i++){
   if(original[i]&&!predicted[i])throw runtime_error("Removed an original boundary");
   if(predicted[i]&&!original[i]){
    if(probs[i]<threshold)throw runtime_error("Added a boundary below threshold");
    score+=weight*log(probs[i]/(1-probs[i]));
   }
  }return score;
 }
 BoundaryResult segment_boundary(const string& text,double weight,double threshold)const{
  Result baseline=segment_open(text,1.,0.);auto original=cuts(baseline.text,text.size());
  auto probs=probabilities(text);auto edges=graph(text);
  vector<int> next_cut(text.size());int next=text.size();
  for(int i=(int)text.size()-1;i>=0;i--){if(original[i+1])next=i+1;next_cut[i]=next;}
  struct State {int a,b,parent,begin,additions;bool one;double score;};
  vector<State> states{{0,0,-1,0,0,false,0}};vector<vector<int>> at(text.size()+1);at[0].push_back(0);
  vector<unordered_map<uint64_t,int>> index(text.size()+1);
  for(int pos=0;pos<(int)text.size();pos++)for(int si:at[pos]){
   State current=states[si];int context=current.b?(current.one?1:2):0;
   double unknown=.95*ws(current.a,current.b,UNKNOWN);
   for(const auto& e:edges[pos]){
    if(e.end>next_cut[pos])continue;
    bool added=!original[e.end];if(added&&probs[e.end]<threshold)continue;
    double value=current.score+(e.word==UNKNOWN?unknown:.95*ws(current.a,current.b,e.word))+.05*e.chars[context];
    if(e.word==UNKNOWN)value+=e.spelling+e.length;
    if(added)value+=weight*log(probs[e.end]/(1-probs[e.end]));
    bool one=e.end-pos==1;int additions=current.additions+int(added);
    uint64_t code=(paircode(current.b,e.word)<<1)|one;auto found=index[e.end].find(code);
    if(found==index[e.end].end()){
     int id=states.size();index[e.end][code]=id;at[e.end].push_back(id);
     states.push_back({current.b,e.word,si,pos,additions,one,value});
    }else{
     auto& old=states[found->second];
     if(value>old.score+1e-12||(abs(value-old.score)<=1e-12&&additions<old.additions)){
      old.score=value;old.parent=si;old.begin=pos;old.additions=additions;
     }
    }
   }
  }
  if(at.back().empty())throw runtime_error("No constrained path");int best=at.back()[0];
  for(int id:at.back())if(states[id].score>states[best].score+1e-12||(abs(states[id].score-states[best].score)<=1e-12&&states[id].additions<states[best].additions))best=id;
  if(states[best].score<=baseline.score+1e-9)return {baseline,baseline,{}};
  vector<string> tokens;int end=text.size();
  for(int id=best;states[id].parent>=0;id=states[id].parent){int begin=states[id].begin;tokens.push_back(text.substr(begin,end-begin));end=begin;}
  reverse(tokens.begin(),tokens.end());string joined;
  for(const auto& word:tokens){if(!joined.empty())joined+=' ';joined+=word;}
  double value=full_boundary(joined,original,probs,weight,threshold);
  if(abs(value-states[best].score)>1e-8*text.size())throw runtime_error("Constrained DP score mismatch");
  auto predicted=cuts(joined,text.size());vector<int> added;
  for(int i=1;i<(int)text.size();i++)if(predicted[i]&&!original[i])added.push_back(i);
  return {{value,joined},baseline,added};
 }
};

void emit_boundary(const BoundaryResult& result){
 cout<<"{\"corrected\":";emit(result.output);cout<<",\"baseline\":";emit(result.baseline);
 cout<<",\"added_positions\":[";for(int i=0;i<(int)result.added.size();i++){if(i)cout<<',';cout<<result.added[i];}cout<<"]}";
}
int main(int argc,char**argv){try{
 if(argc<4)throw runtime_error("Expected MODEL MODE INPUT");
 BoundaryModel model;model.load_boundary(argv[1]);cout<<setprecision(17);string mode=argv[2];
 if(mode=="batch"){
  ifstream in(argv[3]);if(!in)throw runtime_error("Missing batch input");double weight,threshold;string text;
  while(in>>weight>>threshold>>text){emit_boundary(model.segment_boundary(text,weight,threshold));cout<<'\n';}
 }else if(mode=="segment"){
  if(argc!=6)throw runtime_error("Expected weight and threshold");
  emit_boundary(model.segment_boundary(readletters(argv[3]),stod(argv[4]),stod(argv[5])));cout<<'\n';
 }else throw runtime_error("Unknown mode");
 return 0;
}catch(const exception& e){cerr<<e.what()<<'\n';return 2;}}
