from pathlib import Path
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from xml.sax.saxutils import escape
R=Path(__file__).resolve().parents[1]; t=R/'tables'; f=R/'figures'; out=R/'reports/phase2'; out.mkdir(parents=True,exist_ok=True)
r=pd.read_csv(t/'results.csv',index_col=0)['value']; moments=pd.read_csv(t/'moments.csv'); groups=pd.read_csv(t/'apoe_groups.csv'); missing=pd.read_csv(t/'missing.csv')
sections=[]
def text(title,body): sections.append(('text',title,body))
def image(name,caption): sections.append(('image',name,caption))
def coverage(title, rows): sections.append(('table', title, rows))
coverage('Task coverage', [('Shared 1', 'Sample space, events and variables'), ('Shared 2', 'Marginal and joint probabilities'), ('Shared 3', 'Conditional probabilities'), ('Shared 4', 'Empirical independence'), ('Shared 5', 'Binomial model'), ('Shared 6', 'Histogram and Q-Q plot'), ('Shared 7', 'Empirical moments'), ('Shared 8', 'Paired covariance'), ('Shared 9', 'Empirical Bayes identity'), ('C1', 'MRI and recorded NACCAPOE groupings'), ('C2', 'Cognitive and MRI distributions'), ('C3', 'Cross-modal probabilities'), ('C4', 'Scatterplots and covariance'), ('C5', 'Participant and visit rule')])
text('Study and participant-level frame','Phase 2, Path C. Question: how do recorded NACCAPOE categories relate to recorded cognitive status, and how do left and right entorhinal thickness relate to CDRSUM? These are empirical descriptions, not causal effects or population estimates. Source: supplied udslong_imputed.csv and mriscanclean.csv. UDS is already imputed; no new imputation was performed. The supplied NACC codebook was absent; no biological interpretation is assigned to NACCAPOE categories, including code 9.')
text('C5: IDs, matching and observation rule',f"UDS: {int(r['UDS rows'])} rows and {int(r['UDS unique IDs'])} unique nonmissing IDs; MRI: {int(r['MRI rows'])} rows and {int(r['MRI unique IDs'])} unique IDs. UDS-only {int(r['UDS-only IDs'])}, MRI-only {int(r['MRI-only IDs'])}, one-to-one matched {int(r['joined rows before eligibility'])}. Analysis includes {int(r['analysis N'])} rows with nonmissing left thickness and CDRGLOB in observed values 0, 0.5, 1, 2. Each participant contributes the only supplied row; no index visit can be selected chronologically. A unique row is not evidence of independence between people, a single historical visit, or contemporaneous UDS and MRI. No reliable visit/scan timing is supplied; historical visit counts and lag are unknown.")
text('Data quality and eligible outcomes','Missing counts after joining for the six core variables: '+', '.join(f"{x.variable}: {x.missing_n} ({x.missing_percent:.1f}%)" for x in missing.itertuples())+'. Zero blank cells do not imply original complete data because the UDS input was imputed. MOCATOTS has 88, other values above 30, and fractional values; without codebook and imputation metadata we cannot interpret or clean these, so use CDRSUM rather than assume they are valid scores. CDRGLOB > 0 is a recorded-value event, not a new diagnosis. Units and clinical cutoffs are not asserted without supplied documentation.')
text('1-4 and C1, C3: events and empirical probabilities',f"Choose a participant uniformly from the {int(r['analysis N'])} eligible matched rows. A = recorded CDRGLOB > 0; B = left thickness strictly below the observed median {r['LH median threshold']:.3f}; X = recorded CDRSUM. A and B are binary indicators of the selected participant; X is the participant’s quantitative recorded clinical score and left thickness is a continuous-valued MRI measure. These choices support the probability table and paired cognitive-imaging description. Ties at the median belong to not-B. A: {int(r['A count'])}/{int(r['analysis N'])} = {r['P(A)']:.4f}; B: {int(r['B count'])}/{int(r['analysis N'])} = {r['P(B)']:.4f}; joint A and B: {int(r['A and B count'])}/{int(r['analysis N'])} = {r['P(A and B)']:.4f}. P(A|B) = {int(r['A and B count'])}/{int(r['B count'])} = {r['P(A | B)']:.4f}; P(A|not B) = {int(r['A count']-r['A and B count'])}/{int(r['analysis N']-r['B count'])} = {r['P(A | not B)']:.4f}. The groups differ descriptively. Under empirical independence P(A)P(B) = {r['P(A)P(B)']:.4f}, unlike joint {r['P(A and B)']:.4f}; exact independence is not compatible with these empirical proportions, without a formal test or inference.")
text('C1: two groupings', 'The MRI grouping compares below-median versus at-or-above-median left thickness; counts, denominators and conditional probabilities appear above. The second grouping uses recorded NACCAPOE categories below. Both use the same eligible sample; differences are descriptive, not causal or tests.')
text('NACCAPOE and cognitive status','For each recorded code, count A / group size (proportion): '+ '; '.join(f'{x.NACCAPOE:g}: {int(x.sum)}/{int(x.count)} ({x.mean:.3f})' for x in groups.itertuples())+'. Code 9 is included as a raw recorded category, not assumed to be a genotype; small groups are unstable descriptions. These are not e4 carrier comparisons.')
text('5: discrete random variable and binomial model',f"A is Bernoulli in the empirical distribution with p = {r['P(A)']:.4f}. For a hypothetical count K in 10 independent, identically distributed draws with replacement, K ~ Binomial(10,p); P(K >= 4) = {r['P(binomial >= 4)']:.4f}, E(K)=10p={10*r['P(A)']:.3f}, Var(K)=10p(1-p)={10*r['P(A)']*(1-r['P(A)']):.3f}. This is a probability model, not resampling or a confidence interval. For 10 distinct participants sampled without replacement the exact finite-population count is hypergeometric, not binomial; similar probabilities require a small sampling fraction and comparable independent draws. Selection, center effects and repeated histories may also undermine independence or equal probabilities.")
image('binomial.png','Illustrative model probabilities, not observed group counts.')
text('6-7 and C2: empirical distributions and moments','Moments use denominator n (the empirical probability distribution); outliers are counts outside Q1 - 1.5 IQR and Q3 + 1.5 IQR, not errors to delete. '+ ' '.join(f"{x.variable}: n={x.n}, mean={x.mean:.3f}, variance={x.variance_ddof0:.3f}, median={x.median:.3f}, range {x.min:.3f} to {x.max:.3f}, Tukey flags={x.tukey_outliers}." for x in moments.itertuples())+' CDRSUM is strongly concentrated at zero and right-skewed, so a normal approximation is poor. Left thickness has a roughly central mound but a lower tail and deviations in the Q-Q plot; a normal model is at best approximate, especially in the tails. The variance describes squared dispersion around the empirical mean, not uncertainty in that mean.')
image('distributions.png','Observed cognitive and imaging distributions.')
image('qq.png','Left thickness normal Q-Q plot and fitted mean/SD reference line.')
text('8 and C4: covariance across modalities',f"Population-form empirical covariance uses 1/n on available pairs: cov(left thickness, CDRSUM) = {r['Cov(LH,CDRSUM)']:.4f}; cov(right thickness, CDRSUM) = {r['Cov(RH,CDRSUM)']:.4f}. Both paired denominators are {int(r['LH paired N'])} (left) and {int(r['RH paired N'])} (right). Negative signs indicate that larger thickness values tend to co-occur with lower CDRSUM within this file; the scatter is heterogeneous and covariance depends on measurement scales. No correlation, significance test, regression or causal conclusion is made.")
image('scatter.png','Bilateral thickness and recorded CDRSUM; one point per participant.')
text('9: Bayes identity',f"Treat B as the observed information and A as the event of interest. P(B|A) = {int(r['A and B count'])}/{int(r['A count'])} = {r['P(B | A)']:.4f}; P(A|B) = P(B|A) P(A) / P(B) = {r['P(A | B)']:.4f}. This is a rearrangement of the same observed table, not a validated diagnostic test, external prior, or temporal prediction.")
text('Limitations and next steps','MRI inclusion cannot be compared with non-MRI participants because all supplied UDS IDs match MRI. Selection into the supplied cohort is unknown. Imputed and special values may influence results; codebook and original missingness are unavailable. Obtain authoritative coding and visit/scan timing before interpreting genotype or clinical status, and before later inference. The median cutoff is sample-defined, not clinical. No Phase 3-5 analyses were performed.')
# Organize the report by the assignment's individual shared and Path C tasks.
original = sections
lookup = {title: body for typ, title, body in original if typ == 'text'}
images = {title: body for typ, title, body in original if typ == 'image'}
sections = []
coverage('Task coverage', [(f'Shared {i}', 'Addressed', f'Shared Task {i}', f'Shared Task {i}') for i in range(1, 10)] + [(f'C{i}', 'Addressed', f'C{i}', f'Path C Task C{i}') for i in range(1, 6)])
text('Study and participant-level frame', lookup['Study and participant-level frame'])
text('Data quality and eligible outcomes', lookup['Data quality and eligible outcomes'])
events = lookup['1-4 and C1, C3: events and empirical probabilities']
a, rest = events.split(' A: ', 1)
b, rest = rest.split(' P(A|B)', 1)
c, d = rest.split(' Under empirical independence ', 1)
text('Shared Task 1: Sample space and random variables', a)
text('Shared Task 2: Marginal probabilities', 'A: ' + b)
text('Shared Task 3: Joint and conditional probabilities', 'P(A|B)' + c)
text('Shared Task 4: Empirical independence', 'Under empirical independence ' + d)
text('Shared Task 5: Discrete distribution', lookup['5: discrete random variable and binomial model'])
image('binomial.png', images['binomial.png'])
dist = lookup['6-7 and C2: empirical distributions and moments']
mom, shape = dist.split(' CDRSUM is strongly', 1)
shape, interpretation = shape.split(' The variance describes', 1)
text('Shared Task 6: Continuous distribution and normal approximation', 'CDRSUM is strongly' + shape + ' See the histogram and normal Q-Q plot below; the reference line uses the empirical mean and standard deviation.')
image('distributions.png', images['distributions.png'])
image('qq.png', images['qq.png'])
text('Shared Task 7: Empirical expectation and variance', mom + ' The variance describes' + interpretation)
text('Shared Task 8: Covariance', lookup['8 and C4: covariance across modalities'])
image('scatter.png', images['scatter.png'])
text('Shared Task 9: Bayes identity', lookup['9: Bayes identity'])
text('Path C Task C1: Cognitive status in MRI and NACCAPOE groups', lookup['C1: two groupings'] + ' ' + lookup['NACCAPOE and cognitive status'])
text('Path C Task C2: Clinical and MRI distributions', 'The numeric summaries and Tukey flags are reported in Shared Task 7; histograms and shape discussion appear in Shared Task 6. These describe the supplied eligible sample.')
text('Path C Task C3: Clinical and imaging events', 'The cross-modal joint and conditional probabilities are given in Shared Tasks 2 and 3; the MRI threshold is the sample median, not a clinical cutoff. The comparison is descriptive and does not establish temporal order.')
text('Path C Task C4: Bilateral covariance', 'The complete-pair covariance values and bilateral scatterplots are reported in Shared Task 8. These are scale-dependent descriptive summaries, not causal effects.')
text('Path C Task C5: IDs, matching and observation rule', lookup['C5: IDs, matching and observation rule'])
text('Limitations and next steps', lookup['Limitations and next steps'])
styles=getSampleStyleSheet(); story=[Paragraph('Phase 2: Probability and distributions — NACC',styles['Title']),Paragraph('Mahdi Aroun | phase-2',styles['Normal']),Spacer(1,12)]
for typ,title,body in sections:
 if typ=='text': story.extend([Paragraph(escape(title),styles['Heading2']),Paragraph(escape(body),styles['BodyText']),Spacer(1,8)])
 elif typ=='table':
  rows=[['Task','Status','Notebook','Report']]+[[Paragraph(escape(str(v)),styles['BodyText']) for v in row] for row in body]
  table=Table(rows,colWidths=[65,65,145,165],repeatRows=1,hAlign='LEFT'); table.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.4,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('FONTSIZE',(0,0),(-1,-1),9)]))
  story.extend([Paragraph(escape(title),styles['Heading2']),table,Spacer(1,10)])
 else: story.extend([Image(str(f/title),width=6.1*inch,height=(3.05 if title in ['scatter.png','distributions.png'] else 3.7)*inch,kind='proportional'),Paragraph(escape(body),styles['Italic']),Spacer(1,10)])
SimpleDocTemplate(str(out/'phase2.pdf'),pagesize=(612,792),rightMargin=45,leftMargin=45,topMargin=45,bottomMargin=45).build(story)
(R/'reports/phase2.pdf').write_bytes((out/'phase2.pdf').read_bytes())
def esc(s):
 return ''.join({'\\':r'\textbackslash{}','_':r'\_','%':r'\%','&':r'\&','#':r'\#','$':r'\$','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','≥':r'$\geq$','—':'--','–':'--','’':"'"}.get(c,c) for c in str(s))
latex=[r'\documentclass[11pt]{article}',r'\usepackage[utf8]{inputenc}',r'\usepackage[T1]{fontenc}',r'\usepackage{graphicx}',r'\usepackage[margin=1in]{geometry}',r'\title{Phase 2: Probability and distributions -- NACC}',r'\author{Mahdi Aroun}',r'\date{phase-2}',r'\begin{document}',r'\maketitle']
for typ,title,body in sections:
 if typ=='text': latex.extend([r'\section*{'+esc(title)+'}',esc(body)])
 elif typ=='table':
  latex.extend([r'\section*{'+esc(title)+'}', r'\begin{tabular}{p{0.13\linewidth}p{0.14\linewidth}p{0.29\linewidth}p{0.29\linewidth}}', r'\textbf{Task} & \textbf{Status} & \textbf{Notebook} & \textbf{Report} \\', r'\hline'] + [' & '.join(esc(v) for v in row)+r' \\' for row in body] + [r'\end{tabular}'])
 else: latex.extend([r'\begin{figure}[htbp]\centering',r'\includegraphics[width=.88\linewidth]{../../figures/'+title+'}',r'\caption{'+esc(body)+'}',r'\end{figure}'])
latex.append(r'\end{document}');(out/'phase2.tex').write_text('\n\n'.join(latex),encoding='utf-8')
