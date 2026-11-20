from pathlib import Path
import nbformat as n
p=Path(__file__).resolve().parents[1]
b=n.v4.new_notebook(); cells=[]
def md(s): cells.append(n.v4.new_markdown_cell(s))
def code(s): cells.append(n.v4.new_code_cell(s))
md('# Phase 2 — Path C: probability and distributions\nReproducible continuation of Phase 1; all probabilities refer to the supplied, imputed, matched participant file, not a target population. Calculations below are explicit. Run from the repository root or notebooks directory.')
code('''from pathlib import Path
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
from IPython.display import display
root = Path.cwd()
if not (root / 'data').exists(): root = root.parent
u = pd.read_csv(root/'data/udslong_imputed.csv')
m = pd.read_csv(root/'data/mriscanclean.csv')
assert u.NACCID.notna().all() and m.NACCID.notna().all()
assert u.NACCID.is_unique and m.NACCID.is_unique
d0 = u.merge(m, on='NACCID', validate='one_to_one', suffixes=('_uds','_mri'))
d = d0.dropna(subset=['CDRGLOB','LH_ENTORHINAL_AVGTH']).copy()
d = d[d.CDRGLOB.isin([0, .5, 1, 2])].copy()
n = len(d)
assert n > 0
print('Joined:',len(d0),'Eligible:',n)
''')
md('## Shared Task 1 — Sample space and random variables\nSelect one eligible matched participant uniformly: Ω is the 1,237 eligible NACCIDs and each observation has mass 1/n. A means that participant has recorded CDRGLOB > 0; B means their left entorhinal thickness is strictly below the eligible-sample median. A and B are binary indicators (0 or 1), appropriate for joint and conditional frequencies; B is a sample-defined imaging grouping, not a clinical cutoff. X is that same participant’s recorded CDRSUM, a quantitative clinical score used to describe its empirical distribution and covariance with thickness. Left thickness is a quantitative, continuous-valued MRI measurement; NACCAPOE is a recorded categorical code, not a validated genotype. The finite empirical distribution is not a population model. Eligibility restricts CDRGLOB to observed values in this file, not codebook validation. Median ties are in not-B.')
code('''threshold = d.LH_ENTORHINAL_AVGTH.median()
A = d.CDRGLOB > 0
B = d.LH_ENTORHINAL_AVGTH < threshold
X = d.CDRSUM
print('n =', n, 'threshold =', threshold, 'CDRGLOB values:', sorted(d.CDRGLOB.unique()))''')
md('## Shared Task 2 — Marginal probabilities\nFrequency divided by the number of eligible participants.')
code("print('P(A) =', A.sum(), '/', n, '=', A.mean()); print('P(B) =', B.sum(), '/', n, '=', B.mean())")
md('## Shared Task 3 — Joint and conditional probabilities\nP(A∩B) uses n; conditional probabilities use the conditioning-event count. Both conditioning events are nonempty.')
code('''joint = int((A & B).sum()); a = int(A.sum()); b = int(B.sum())
assert a and b and n-b
print(pd.crosstab(B.rename('B'), A.rename('A'), margins=True))
print('P(A∩B) =', joint, '/', n, '=', joint/n)
print('P(A|B) =', joint, '/', b, '=', joint/b)
print('P(A|not B) =', a-joint, '/', n-b, '=', (a-joint)/(n-b))''')
md('## Shared Task 4 — Empirical independence\nCompare the joint probability with the product of the marginals. This is an exact statement about the empirical distribution, not a hypothesis test or a causal claim.')
code("print('joint =', joint/n, '; product =', (a/n)*(b/n), '; difference =', joint/n-(a/n)*(b/n))")
md('## Shared Task 5 — Discrete distribution\nFor K, the number of A events in 10 hypothetical independent draws **with replacement** from the empirical distribution, K ~ Binomial(10,p), p = P(A). This is not an observed grouping of 10 people. For distinct participants sampled without replacement the finite-population distribution is hypergeometric. Independence and common event probability are model assumptions, not guaranteed by unique IDs.')
code('''p = a/n
pmf = pd.Series({k: math.comb(10,k)*p**k*(1-p)**(10-k) for k in range(11)}, name='probability')
print('E(K)=',10*p,'Var(K)=',10*p*(1-p),'P(K≥4)=',pmf.loc[4:].sum())
display(pmf.to_frame()); pmf.plot.bar(title='Hypothetical binomial count', xlabel='K', ylabel='Probability'); plt.show()''')
md('## Shared Task 6 — Distribution shape\nHistogram and normal Q–Q plot describe observed left thickness. Visual departures, especially tails, limit a normal approximation. CDRSUM has substantial mass at zero and is not well represented by a normal distribution.')
code('''fig, ax = plt.subplots(1,3,figsize=(12,3))
ax[0].hist(d.CDRSUM.dropna(),bins=25); ax[0].set_title('CDRSUM')
x = np.sort(d.LH_ENTORHINAL_AVGTH.dropna().to_numpy())
ax[1].hist(x,bins=25); ax[1].set_title('Left thickness')
z = norm.ppf((np.arange(len(x))+.5)/len(x))
ax[2].scatter(z,x,s=5); ax[2].plot(z,x.mean()+x.std()*z,color='red'); ax[2].set_title('Normal Q–Q')
plt.tight_layout(); plt.show()''')
md('## Shared Task 7 — Empirical expectation and variance\nFor observed values xᵢ, E(X)=Σxᵢ/n and Var(X)=Σ(xᵢ−E(X))²/n. Drop explicit missing values per variable; no undocumented code is recoded. These are empirical-distribution moments, not standard errors.')
code('''for name in ['CDRSUM','LH_ENTORHINAL_AVGTH','RH_ENTORHINAL_AVGTH']:
    x = d[name].dropna().to_numpy(); mu = sum(x)/len(x)
    print(name, 'n =',len(x),'E =',mu,'Var =',sum((x-mu)**2)/len(x))''')
md('## Shared Task 8 — Covariance\nOn complete pairs, Cov(X,Y)=mean((X−mean X)(Y−mean Y)); denominator is the number of pairs. Sign describes co-variation, units are scale-dependent. No correlation or regression is computed.')
code('''for side in ['LH','RH']:
    pair = d[[side+'_ENTORHINAL_AVGTH','CDRSUM']].dropna()
    x,y = pair.iloc[:,0],pair.iloc[:,1]
    print(side, 'paired n =',len(pair), 'covariance =',((x-x.mean())*(y-y.mean())).mean())''')
md('## Shared Task 9 — Bayes identity\nWith A as the event of interest and B as the observed information, use P(A|B)=P(B|A)P(A)/P(B). This rearranges the same table; it is not an external prior or validated clinical prediction.')
code("print('P(B|A) =',joint,'/',a,'=',joint/a); print('Bayes =',(joint/a)*(a/n)/(b/n),'direct =',joint/b); assert np.isclose((joint/a)*(a/n)/(b/n),joint/b)")
md('## C1 — Cognitive status in two groupings\nFirst group participants by MRI-derived B versus not-B (median ties in not-B); then independently group by recorded NACCAPOE code. For each grouping report A counts, denominators and proportions. No NACCAPOE code, including 9, is assigned genotype meaning; small groups are unstable. These are descriptive within the same eligible matched sample, not causal or inferential comparisons.')
code("display(d.assign(A=A, MRI_group=np.where(B, 'below median', 'at or above median')).groupby('MRI_group').A.agg(['sum','count','mean']))")
code("groups = d.assign(A=A).groupby('NACCAPOE',dropna=False).A.agg(['sum','count','mean']); display(groups)")
md('## C2 — Cognitive and imaging distributions\nShow quantiles and Tukey flags; flags are not automatic exclusions. MOCATOTS is examined as recorded, but its extreme and fractional values cannot be resolved without a codebook and imputation metadata; it is not substituted for a validated score.')
code('''for col in ['CDRGLOB','CDRSUM','MOCATOTS','LH_ENTORHINAL_AVGTH','RH_ENTORHINAL_AVGTH']:
    s=d[col].dropna(); q1,q3=s.quantile([.25,.75]); flags=((s<q1-1.5*(q3-q1)) | (s>q3+1.5*(q3-q1))).sum()
    print(col, 'n',len(s),'median',s.median(),'range', (s.min(),s.max()), 'Tukey flags',flags)
print('MOCATOTS > 30:', (d.MOCATOTS>30).sum(), '; fractional:', ((d.MOCATOTS%1!=0)&d.MOCATOTS.notna()).sum(), '; 88:', (d.MOCATOTS==88).sum())''')
md('## C3 — Empirical clinical/imaging events\nThe median threshold is internal to this sample, not a clinical cutoff. Comparison is descriptive and cannot establish temporal ordering.')
code("print('Below-median group:',joint,'/',b,'=',joint/b); print('Other group:',a-joint,'/',n-b,'=',(a-joint)/(n-b))")
md('## C4 — Bilateral imaging and CDRSUM\nScatterplots and covariance only: negative covariance indicates larger thickness tends to co-occur with lower recorded CDRSUM in these paired data, not causation.')
code('''fig,axes=plt.subplots(1,2,figsize=(10,4))
for ax,side in zip(axes,['LH','RH']):
    pair=d[[side+'_ENTORHINAL_AVGTH','CDRSUM']].dropna(); x=pair.iloc[:,0]; y=pair.iloc[:,1]
    ax.scatter(x,y,s=8,alpha=.3); ax.set(xlabel=side+' thickness',ylabel='CDRSUM',title='n=%d, covariance=%.4f'%(len(pair),((x-x.mean())*(y-y.mean())).mean()))
plt.tight_layout(); plt.show()''')
md('## C5 — Participant IDs and repeated observations\nInspect both inputs before joining. One supplied row per ID is the analysis unit; this does not prove participant independence, exclude historical visits, or establish temporal alignment of MRI and UDS. No chronology-based index visit can be selected from the supplied documentation.')
code('''for name, frame in [('UDS imputed',u),('MRI',m)]:
    print(name, 'rows',len(frame),'missing IDs',frame.NACCID.isna().sum(),'unique IDs',frame.NACCID.nunique(),'duplicate rows',frame.NACCID.duplicated().sum())
print('UDS-only',len(set(u.NACCID)-set(m.NACCID)),'MRI-only',len(set(m.NACCID)-set(u.NACCID)),'matched',len(d0))
assert d0.NACCID.is_unique''')
md('## Task coverage\n| Task | Status | Notebook location | Report location |\n|---|---|---|---|\n' + '\n'.join(f'| Shared {i} | Addressed | Shared Task {i} | Shared Task {i} |' for i in range(1,10)) + '\n' + '\n'.join(f'| C{i} | Addressed | C{i} | Path C Task C{i} |' for i in range(1,6)))
md('## Scope and limitations\nUDS was already imputed; original missingness is unknown. No authoritative codebook or reliable visit/scan timing was supplied. MRI-selected participants need not represent the wider population. No Phase 3–5 testing, inference, correlation, regression, or sensitivity analysis is performed. Results are noncausal.')
b.cells=cells;b.metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'}}
n.write(b,p/'notebooks/phase2_probability.ipynb')
