"""Reproduces the tables and figure in the paper.
Run from the repository root:  python code/analyse.py
Input: data/labels.csv. Output: results/*.csv and results/fig_outcomes.(pdf|png)."""
import json, numpy as np, pandas as pd
from scipy import stats
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import os
os.makedirs('results',exist_ok=True)
M=pd.read_csv('data/labels.csv')
MOD={'Llama-3.1-8B-Instruct':'Llama 3.1 8B','Qwen2.5-7B-Instruct':'Qwen2.5 7B','gpt-oss-120b':'gpt-oss-120b'}
STR=['naive','role_based','constraint_based','evidence_based','algorithmic']
SN={'naive':'Naive','role_based':'Role-based','constraint_based':'Constraint','evidence_based':'Evidence','algorithmic':'Premise verif.'}
M['model']=M.model.map(MOD); L='final_label'
def wilson(k,n,z=1.96):
    if n==0: return (np.nan,np.nan)
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return c-h,c+h
rows=[]
for mo in MOD.values():
  for s in STR:
    d=M[(M.model==mo)&(M.strategy==s)]; n=len(d)
    C=(d[L]=='Correct').sum(); H=(d[L]=='Hallucinated').sum(); A=(d[L]=='Abstained').sum()
    ctl=d[d.trap_type=='control']; 
    rows.append(dict(model=mo,strategy=SN[s],N=n,C=C,H=H,A=A,
      H_rate=H/n,H_lo=wilson(H,n)[0],H_hi=wilson(H,n)[1],A_rate=A/n,A_lo=wilson(A,n)[0],A_hi=wilson(A,n)[1],
      C_rate=C/n,H_answered=H/(C+H) if C+H else np.nan,Ha_lo=wilson(H,C+H)[0],Ha_hi=wilson(H,C+H)[1],
      ctl_n=len(ctl),ctl_abst=(ctl[L]=='Abstained').sum(),ctl_hall=(ctl[L]=='Hallucinated').sum(),
      mixed=int(d.mixed.sum()),cit=int(d.citation_issue.sum()),trunc=int((d.finish_reason=='length').sum())))
T=pd.DataFrame(rows); T.to_csv('results/table_main.csv',index=False)
# paired tests vs naive
def stuart_maxwell(a,b,cats=('Correct','Hallucinated','Abstained')):
    t=pd.crosstab(pd.Categorical(a,cats),pd.Categorical(b,cats),dropna=False).values.astype(float)
    k=len(cats); dvec=(t.sum(1)-t.sum(0))[:k-1]
    S=np.zeros((k-1,k-1))
    for i in range(k-1):
      for j in range(k-1):
        S[i,j]= (t[i].sum()+t[:,i].sum()-2*t[i,i]) if i==j else -(t[i,j]+t[j,i])
    try: chi=float(dvec@np.linalg.solve(S,dvec))
    except np.linalg.LinAlgError: chi=float(dvec@np.linalg.pinv(S)@dvec)
    return chi, float(stats.chi2.sf(chi,k-1))
tests=[]
for mo in MOD.values():
  base=M[(M.model==mo)&(M.strategy=='naive')].set_index('question_id')[L]
  for s in STR[1:]:
    x=M[(M.model==mo)&(M.strategy==s)].set_index('question_id')[L]
    q=base.index.intersection(x.index); a=base[q]; bb=x[q]
    b10=int(((a=='Hallucinated')&(bb!='Hallucinated')).sum()); b01=int(((a!='Hallucinated')&(bb=='Hallucinated')).sum())
    nd=b10+b01
    if nd==0: p=1.0; how='-'
    elif nd<25: p=float(stats.binomtest(min(b10,b01),nd,0.5).pvalue); how='exact'
    else: chi=(abs(b10-b01)-1)**2/nd; p=float(stats.chi2.sf(chi,1)); how='chi2cc'
    sm,psm=stuart_maxwell(a,bb)
    tests.append(dict(model=mo,strategy=SN[s],pairs=len(q),naiveH_only=b10,stratH_only=b01,mcnemar=how,p_mcnemar=p,SM_chi2=sm,p_SM=psm))
R=pd.DataFrame(tests)
def holm(p):
    p=np.asarray(p); o=np.argsort(p); m=len(p); adj=np.empty(m); run=0
    for r,i in enumerate(o): run=max(run,(m-r)*p[i]); adj[i]=min(1,run)
    return adj
R['p_mcnemar_holm']=holm(R.p_mcnemar); R['p_SM_holm']=holm(R.p_SM)
R.to_csv('results/table_tests.csv',index=False)
# trap type breakdown (H count / n) pooled over models
tt=M.groupby(['trap_type','strategy'])[L].apply(lambda s:(s=='Hallucinated').sum()).unstack()[STR].rename(columns=SN)
tn=M.groupby(['trap_type','strategy'])[L].size().unstack()[STR].rename(columns=SN)
ta=M.groupby(['trap_type','strategy'])[L].apply(lambda s:(s=='Abstained').sum()).unstack()[STR].rename(columns=SN)
tt.to_csv('results/trap_H.csv'); tn.to_csv('results/trap_n.csv'); ta.to_csv('results/trap_A.csv')
dm=M.groupby(['domain','strategy'])[L].apply(lambda s:(s=='Hallucinated').sum()).unstack()[STR].rename(columns=SN); dm.to_csv('results/domain_H.csv')
# figure: stacked bars per model/strategy
fig,axs=plt.subplots(1,3,figsize=(10,3.1),sharey=True)
for ax,mo in zip(axs,MOD.values()):
    d=T[T.model==mo]; x=np.arange(len(d))
    c=d.C/d.N*100; h=d.H/d.N*100; a=d.A/d.N*100
    ax.bar(x,c,color='#4c9a6a',label='Correct'); ax.bar(x,h,bottom=c,color='#c8553d',label='Hallucinated'); ax.bar(x,a,bottom=c+h,color='#b8b8b8',label='Abstained')
    ax.set_xticks(x); ax.set_xticklabels(d.strategy,rotation=35,ha='right',fontsize=8); ax.set_title(mo,fontsize=9)
axs[0].set_ylabel('% of responses'); axs[2].legend(fontsize=7,loc='lower right'); fig.tight_layout(); fig.savefig('results/fig_outcomes.pdf'); fig.savefig('results/fig_outcomes.png',dpi=160)
pd.set_option('display.width',250)
print(T[['model','strategy','N','C','H','A','H_rate','H_lo','H_hi','H_answered','ctl_n','ctl_abst','ctl_hall','mixed','cit','trunc']].round(3).to_string())
print(R.round(4).to_string()); print(tt); print(ta); print(tn.iloc[:,0]); print(dm)
