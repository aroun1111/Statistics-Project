from pathlib import Path
import math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tables'; FIG = ROOT / 'figures'
OUT.mkdir(exist_ok=True); FIG.mkdir(exist_ok=True)
u = pd.read_csv(ROOT/'data/udslong_imputed.csv')
m = pd.read_csv(ROOT/'data/mriscanclean.csv')
assert u.NACCID.notna().all() and m.NACCID.notna().all()
assert u.NACCID.is_unique and m.NACCID.is_unique, 'Review participant selection before joining'
d = u.merge(m, on='NACCID', validate='one_to_one', suffixes=('_uds','_mri'))
cols=['NACCAPOE','CDRGLOB','CDRSUM','MOCATOTS','LH_ENTORHINAL_AVGTH','RH_ENTORHINAL_AVGTH']
assert all(c in d for c in cols)
# No recoding of undocumented codes. Clinical example uses exact observed CDRGLOB values.
d=d.dropna(subset=['CDRGLOB','LH_ENTORHINAL_AVGTH']).copy()
d=d[d.CDRGLOB.isin([0,0.5,1,2])].copy()
n=len(d); threshold=d.LH_ENTORHINAL_AVGTH.median()
A=d.CDRGLOB.gt(0); B=d.LH_ENTORHINAL_AVGTH.lt(threshold)
a=int(A.sum()); b=int(B.sum()); ab=int((A&B).sum())
ct=pd.crosstab(B.rename('LH below median'),A.rename('CDRGLOB > 0'))
ct.to_csv(OUT/'joint_counts.csv')
mri_groups=d.assign(event=A, MRI_group=np.where(B,'below median','at or above median')).groupby('MRI_group').event.agg(['sum','count','mean'])
mri_groups.to_csv(OUT/'mri_groups.csv')
groups=d.assign(event=A).groupby('NACCAPOE',dropna=False).event.agg(['sum','count','mean']); groups.to_csv(OUT/'apoe_groups.csv')
summary=[]
for c in ['CDRSUM','LH_ENTORHINAL_AVGTH','RH_ENTORHINAL_AVGTH']:
 s=d[c].dropna(); q1,q3=s.quantile([.25,.75]); iqr=q3-q1
 summary.append(dict(variable=c,n=len(s),mean=s.mean(),variance_ddof0=s.var(ddof=0),median=s.median(),q1=q1,q3=q3,min=s.min(),max=s.max(),tukey_outliers=int(((s<q1-1.5*iqr)|(s>q3+1.5*iqr)).sum())))
pd.DataFrame(summary).to_csv(OUT/'moments.csv',index=False)
pd.DataFrame([{'variable':c,'missing_n':int(d[c].isna().sum()),'missing_percent':100*d[c].isna().mean()} for c in cols]).to_csv(OUT/'missing.csv',index=False)
cov={c:float(np.cov(d[[c,'CDRSUM']].dropna().to_numpy().T,ddof=0)[0,1]) for c in ['LH_ENTORHINAL_AVGTH','RH_ENTORHINAL_AVGTH']}
fig,ax=plt.subplots(1,2,figsize=(10,4))
for j,c in enumerate(['CDRSUM','LH_ENTORHINAL_AVGTH']): ax[j].hist(d[c].dropna(),bins=25,color='#427e9d',edgecolor='white');ax[j].set(title=c,xlabel='Recorded value',ylabel='Count')
fig.tight_layout();fig.savefig(FIG/'distributions.png',dpi=150);plt.close(fig)
x=np.sort(d.LH_ENTORHINAL_AVGTH.dropna()); z=norm.ppf((np.arange(len(x))+.5)/len(x));fig,ax=plt.subplots(figsize=(5,4));ax.scatter(z,x,s=6,alpha=.5);ax.plot(z,x.mean()+x.std(ddof=0)*z,color='red');ax.set(xlabel='Standard normal quantile',ylabel='Left thickness',title='Normal Q-Q plot');fig.tight_layout();fig.savefig(FIG/'qq.png',dpi=150);plt.close(fig)
fig,ax=plt.subplots(1,2,figsize=(10,4))
for j,c in enumerate(['LH_ENTORHINAL_AVGTH','RH_ENTORHINAL_AVGTH']): ax[j].scatter(d[c],d.CDRSUM,s=8,alpha=.3);ax[j].set(xlabel=c,ylabel='CDRSUM',title=f'Empirical covariance = {cov[c]:.3f}')
fig.tight_layout();fig.savefig(FIG/'scatter.png',dpi=150);plt.close(fig)
p=a/n; k=10
probs=[math.comb(k,i)*p**i*(1-p)**(k-i) for i in range(k+1)]
pd.DataFrame({'k':range(k+1),'probability':probs}).to_csv(OUT/'binomial_model.csv',index=False)
fig,ax=plt.subplots(figsize=(6,3));ax.bar(range(k+1),probs,color='#427e9d');ax.set(xlabel='Count among 10 hypothetical independent participants',ylabel='Model probability',title='Illustrative binomial model');fig.tight_layout();fig.savefig(FIG/'binomial.png',dpi=150);plt.close(fig)
paired={c:len(d[[c,'CDRSUM']].dropna()) for c in ['LH_ENTORHINAL_AVGTH','RH_ENTORHINAL_AVGTH']}
results={'UDS rows':len(u),'MRI rows':len(m),'UDS unique IDs':u.NACCID.nunique(),'MRI unique IDs':m.NACCID.nunique(),'UDS-only IDs':len(set(u.NACCID)-set(m.NACCID)),'MRI-only IDs':len(set(m.NACCID)-set(u.NACCID)),'joined rows before eligibility':len(u.merge(m,on='NACCID',validate='one_to_one')),'analysis N':n,'LH median threshold':threshold,'A count':a,'B count':b,'A and B count':ab,'P(A)':a/n,'P(B)':b/n,'P(A and B)':ab/n,'P(A)P(B)':a*b/n**2,'P(A | B)':ab/b,'P(A | not B)':(a-ab)/(n-b),'P(B | A)':ab/a,'Cov(LH,CDRSUM)':cov['LH_ENTORHINAL_AVGTH'],'Cov(RH,CDRSUM)':cov['RH_ENTORHINAL_AVGTH'],'LH paired N':paired['LH_ENTORHINAL_AVGTH'],'RH paired N':paired['RH_ENTORHINAL_AVGTH'],'P(binomial >= 4)':sum(probs[4:])}
pd.Series(results,name='value').to_csv(OUT/'results.csv',header=True)
if __name__=='__main__':
 print(pd.Series(results).to_string());print('\nAPOE observed codes (no genotype interpretation):\n',groups);print('\nMoments:\n',pd.DataFrame(summary).to_string(index=False))
