#include <algorithm>
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>
using namespace std;
int main(int argc,char**argv){
 if(argc!=4)return 2;int base=stoi(argv[2]),steps=stoi(argv[3]);vector<vector<int>> lines;ifstream in(argv[1]);string line;
 while(getline(in,line)){istringstream s(line);vector<int> a;int x;while(s>>x)a.push_back(x);if(a.size()>1)lines.push_back(a);}
 int size=base+steps;cout<<"[";bool first=true;
 for(int k=0;k<steps;k++){
  vector<long long> count(size*size,0);for(auto&a:lines)for(size_t i=1;i<a.size();i++)count[a[i-1]*size+a[i]]++;
  auto it=max_element(count.begin(),count.end());if(*it<2)break;int index=it-count.begin(),left=index/size,right=index%size,newid=base+k;
  if(!first)cout<<",";first=false;cout<<"["<<left<<","<<right<<","<<newid<<","<<*it<<"]";
  for(auto&a:lines){vector<int>b;b.reserve(a.size());for(size_t i=0;i<a.size();){if(i+1<a.size()&&a[i]==left&&a[i+1]==right){b.push_back(newid);i+=2;}else b.push_back(a[i++]);}a.swap(b);}
 }
 cout<<"]\n";return 0;
}
