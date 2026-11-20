# Project card — phase-2, Path C (NACC UDS + MRI)

**Research question.** In the supplied matched sample, how does recorded NACCAPOE category relate descriptively to recorded cognitive status, and how do left and right entorhinal thickness co-vary with cognitive measures? Phase 1 established the file structure and focused this question. Phase 2 defines a participant-level empirical probability space and describes distributions; it does not test hypotheses or estimate causal effects.

**Inputs and unit.** `data/udslong_imputed.csv` is already imputed; `data/mriscanclean.csv` contains MRI measures. Both have one supplied row per nonmissing NACCID, and all 1,237 IDs overlap. Join one-to-one on NACCID. Historical visit counts and temporal alignment are unknown. Unique IDs do not guarantee statistical independence or imply that records were contemporaneous.

**Variables.** NACCAPOE is a recorded category, not a verified genotype. CDRGLOB and CDRSUM are recorded cognitive indicators; MOCATOTS is audited as recorded, but its fractional and out-of-range values lack documentation. Left/right entorhinal average thickness are imaging variables. Do not interpret undocumented codes (including NACCAPOE 9), or treat blank-cell absence as proof that the original data were complete.

**Events.** On participants with nonmissing left thickness and CDRGLOB in the observed set {0, 0.5, 1, 2}, choose a participant uniformly. A = recorded CDRGLOB > 0; B = left thickness strictly below the eligible-sample median, with ties in not-B. C1 reports A across B versus not-B and separately across raw NACCAPOE categories, with group denominators. Threshold is sample-specific and not a clinical cutoff. CDRSUM is the principal numeric cognitive variable; covariance is on available pairs with denominator n.

**Deliverables.** The notebook explicitly covers shared tasks 1–9 and Path C tasks C1–C5; scripts reproduce tables, figures, PDF and LaTeX. Binomial calculations use hypothetical independent draws with replacement. No Phase 3–5 tests, correlations, regressions, sensitivity analyses or causal claims.

**Limitations.** MRI selection limits generalizability; codebook, original missingness and temporal alignment are unavailable. Obtain those materials before assigning code meanings or proceeding to later-phase analysis.
