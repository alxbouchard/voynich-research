// CPU cost kernel for letter-valued CSA_OptMatcher assignments.
// GPL-3.0-or-later, derived from the GED recurrence in Fabio Tamburini's
// EditDistanceWild. The empty-string GED is corrected to 1 (unless both empty).
#include <algorithm>
#include <cstdint>
#include <vector>
extern "C" void costs(const int32_t* src, int ns, int sw, const int32_t* trg,
                      int nt, int tw, const uint64_t* masks, double* out) {
  std::vector<uint64_t> w(sw); std::vector<int> prev(tw+1), cur(tw+1);
  for(int i=0;i<ns;i++) {
    int n=0;
    for(int x=0;x<sw && src[i*sw+x]>=0;x++) {
      uint64_t m=masks[src[i*sw+x]]; if(m)w[n++]=m;
    }
    for(int j=0;j<nt;j++) {
      int m=0;while(m<tw && trg[j*tw+m]>=0)m++;
      if(!n || !m){out[i*nt+j]=(n==m?0.0:1.0);continue;}
      for(int y=0;y<=m;y++)prev[y]=y;
      for(int x=1;x<=n;x++) {
        cur[0]=x;
        for(int y=1;y<=m;y++) {
          int sub=(w[x-1] & (uint64_t(1)<<trg[j*tw+y-1])) ? 0:1;
          cur[y]=std::min({prev[y]+1,cur[y-1]+1,prev[y-1]+sub});
        }
        prev.swap(cur);
      }
      out[i*nt+j]=2.0*prev[m]/(n+m+prev[m]);
    }
  }
}
