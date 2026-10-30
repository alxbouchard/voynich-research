"""CPU adaptation of CSA_OptMatcher, letter-valued mappings only.

Same k-permutation representation, coupled acceptance law, and grouped lexicon
assignment objective. Changes: copy proposals, retain best visited state, seed
all randomness, calculate min-over-expansions with exact dynamic programming,
correct empty/nonempty GED, support external alphabets. GPL-3.0-or-later.
"""
import ctypes, hashlib, itertools, json, math, random, time
from pathlib import Path
import numpy as np
from scipy.optimize import linear_sum_assignment
ROOT=Path(__file__).resolve().parent.parent
LIB=ctypes.CDLL(str(ROOT/'tmp/libcost.so'))
I=np.ctypeslib.ndpointer(dtype=np.int32,flags='C_CONTIGUOUS')
U=np.ctypeslib.ndpointer(dtype=np.uint64,flags='C_CONTIGUOUS')
D=np.ctypeslib.ndpointer(dtype=np.float64,flags='C_CONTIGUOUS')
LIB.costs.argtypes=[I,ctypes.c_int,ctypes.c_int,I,ctypes.c_int,ctypes.c_int,U,D]
def pack(words, alphabet):
 idx={s:i for i,s in enumerate(alphabet)}
 a=np.full((len(words),max(map(len,words),default=1)),-1,dtype=np.int32)
 for i,w in enumerate(words):a[i,:len(w)]=[idx[s] for s in w]
 return a
def distance_matrix(words,known,alphabet,target_alphabet,masks):
 a=pack(words,alphabet);b=pack(known,target_alphabet)
 out=np.empty((len(words),len(known)),dtype=np.float64)
 LIB.costs(a,len(a),a.shape[1],b,len(b),b.shape[1],np.array(masks,dtype=np.uint64),out)
 return out
class Problem:
 def __init__(self, source, target, N=1,M=1,penalty=4,alphabet=None,target_alphabet=None):
  self.source=source;self.target=target
  self.lC=alphabet or sorted(set(''.join(w for g in source for w in g)))
  self.kC=target_alphabet or sorted(set(''.join(w for g in target for w in g)))
  self.llC=len(self.lC);self.lkC=len(self.kC);self.N=N;self.M=M;self.penalty=penalty
  assert N*self.llC>=self.lkC and self.lkC<64
  self.size=N*self.llC;self.offset=self.size-self.lkC
  self.a=pack([w for g in source for w in g],self.lC)
  self.b=pack([w for g in target for w in g],self.kC)
  self.starts_a=np.cumsum([0]+[len(g) for g in source[:-1]])
  self.starts_b=np.cumsum([0]+[len(g) for g in target[:-1]])
  self.matrix=np.empty((len(self.a),len(self.b)),dtype=np.float64)
  self.evaluations=0;self.best=(float('inf'),None)
 def masks(self,state):
  masks=[0]*self.llC
  for i in range(self.M):
   for j,v in enumerate(state[i*self.size+self.offset:(i+1)*self.size]):
    masks[v%self.llC]|=1<<j
  return masks
 def evaluate(self,state,details=False):
  masks=self.masks(state)
  LIB.costs(self.a,len(self.a),self.a.shape[1],self.b,len(self.b),self.b.shape[1],np.array(masks,dtype=np.uint64),self.matrix)
  grouped=np.minimum.reduceat(np.minimum.reduceat(self.matrix,self.starts_a,axis=0),self.starts_b,axis=1)
  rows,cols=linear_sum_assignment(grouped)
  nulls=sum(m==0 for m in masks)
  ambiguous=sum(m.bit_count()>1 for m in masks) if self.M>1 else 0
  cost=float(grouped[rows,cols].sum())+self.penalty*(nulls+ambiguous)
  self.evaluations+=1
  if cost<self.best[0]:self.best=(cost,list(state))
  return (cost,grouped,rows,cols) if details else cost
 def initial(self,rng):
  s=[]
  for _ in range(self.M):
   a=list(range(self.size));rng.shuffle(a);s+=a
  return s
 def move(self,state,rng,tgen,qa=False):
  state=list(state) # avoid mutation of the current accepted state
  for _ in range(max(int(len(state)*tgen),1) if qa else 1):
   offset=rng.randrange(self.M)*self.size
   a=offset+rng.randrange(self.size);b=offset+rng.randrange(self.offset,self.size)
   state[a],state[b]=state[b],state[a]
  return state
 def assignment(self,state):
  return {s:[c for j,c in enumerate(self.kC) if m>>j&1] for s,m in zip(self.lC,self.masks(state))}
def anneal(p,seed=20261028,steps=5000,annealers=8,progress=None):
 rng=random.Random(seed);states=[p.initial(rng) for _ in range(annealers)]
 energies=[p.evaluate(s) for s in states];tgen=1.;tacc=200.;interval=max(math.ceil(len(states[0])/annealers),5)
 target_var=.99*(annealers-1)/annealers**2;trace=[];start=time.monotonic()
 for k in range(1,steps+1):
  maximum=max(energies);x=[math.exp((e-maximum)/tacc) for e in energies];gamma=sum(x)
  for i in range(annealers):
   candidate=p.move(states[i],rng,tgen,rng.random()<.1);e=p.evaluate(candidate)
   if e<energies[i] or rng.random()<x[i]/gamma:states[i]=candidate;energies[i]=e
  if k%interval==0:
   tgen*=.999
   var=(annealers*sum(y*y for y in x)/gamma**2-1)/annealers**2
   tacc*=.95 if var<target_var else 1.05
  if k%1000==0 or k==steps:
   point={'step':k,'best_energy':p.best[0],'seconds':time.monotonic()-start};trace.append(point)
   if progress:progress(point)
 best,state=p.best;energy,grouped,rows,cols=p.evaluate(state,True)
 assert abs(best-energy)<1e-9
 return {'seed':seed,'steps':steps,'annealers':annealers,'energy':energy,'state':state,
   'mapping':p.assignment(state),'evaluations':p.evaluations,'trace':trace,'seconds':time.monotonic()-start,
   'matches':[{'source':p.source[i],'target':p.target[j],'cost':float(grouped[i,j])} for i,j in zip(rows,cols)]}
