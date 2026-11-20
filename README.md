# Phase 2 Probability Project --- Path C (NACC UDS + MRI)

## Project overview

This project is the Phase 2 continuation of the Phase 1 research
direction. It uses the supplied National Alzheimer's Coordinating Center
(NACC) Uniform Data Set (UDS) and MRI files to describe:

-   how recorded `NACCAPOE` categories relate to recorded cognitive
    status; and
-   how left and right entorhinal average thickness relate to the
    recorded cognitive measure `CDRSUM`.

The analysis is descriptive. It defines an empirical participant-level
probability space, summarizes distributions, calculates probabilities
and moments, and examines cross-modal covariance. It does not establish
causal effects or make population-level claims.

**Phase:** `phase-2`\
**Path:** C --- linked UDS + MRI\
**Notebook:** `notebooks/phase2_probability.ipynb`\
**Main analysis script:** `src/phase2_analysis.py`\
**Report PDF:** `reports/phase2.pdf`\
**LaTeX source:** `reports/phase2/phase2.tex`

## Research question and analysis scope

The central question is:

> In the supplied matched sample, how does recorded NACCAPOE category
> relate descriptively to recorded cognitive status, and how do left and
> right entorhinal thickness co-vary with cognitive measures?

The principal variables are:

  -----------------------------------------------------------------------
  Variable                            Role in the analysis
  ----------------------------------- -----------------------------------
  `NACCAPOE`                          Recorded category; not treated as a
                                      verified genotype

  `CDRGLOB`                           Recorded global cognitive status
                                      indicator used to define an event

  `CDRSUM`                            Main quantitative cognitive measure
                                      for distribution and covariance
                                      summaries

  `MOCATOTS`                          Audited as recorded; not used as
                                      the main score because unusual
                                      values are undocumented

  `LH_ENTORHINAL_AVGTH`               Left entorhinal average thickness

  `RH_ENTORHINAL_AVGTH`               Right entorhinal average thickness

  `NACCID`                            Participant identifier used to link
                                      UDS and MRI records
  -----------------------------------------------------------------------

The notebook is organized around Shared Tasks 1--9 and Path C Tasks
C1--C5. The project does not extend into Phase 3 or later work.

## Data files

The supplied input files are stored in `data/`:

-   `data/udslong_imputed.csv` --- supplied UDS data; the file is
    already imputed.
-   `data/mriscanclean.csv` --- supplied MRI data.

The files are included as provided for this project. The analysis joins
the two files one-to-one using `NACCID`. The supplied files contain one
row per nonmissing `NACCID` in each modality, with 1,237 overlapping
IDs.

The analysis sample is then restricted to records with nonmissing left
entorhinal thickness and `CDRGLOB` in the observed set `{0, 0.5, 1, 2}`.
The sample size used for the main event calculations is therefore
determined by the analysis code rather than assumed to be the total
number of matched IDs.

**Data handling note:** These files may contain sensitive research data.
Share or redistribute them only when authorized.

## Participant-level events

For the eligible matched sample, a participant is selected uniformly
from the supplied participant records.

-   `A`: recorded `CDRGLOB > 0`.
-   `B`: left entorhinal thickness is strictly below the median in the
    eligible analysis sample.
-   `X`: recorded `CDRSUM`.

Values tied at the median are assigned to `not B`. The median threshold
is specific to this supplied sample; it is not a clinical cutoff.

The project reports the marginal, joint, and conditional probabilities
for these events, as well as the empirical comparison relevant to
independence. It also reports cognitive status across two groupings for
Path C Task C1: the MRI-based below-median versus at-or-above-median
groups, and the recorded `NACCAPOE` categories.

## Repository structure

``` text
phase2_project/
├── PHASE_LABEL
├── PROJECT_CARD.md
├── README.md
├── requirements.txt
├── data/
│   ├── mriscanclean.csv
│   └── udslong_imputed.csv
├── figures/
│   ├── binomial.png
│   ├── distributions.png
│   ├── qq.png
│   └── scatter.png
├── notebooks/
│   └── phase2_probability.ipynb
├── reports/
│   ├── phase2.pdf
│   └── phase2/
│       ├── phase2.pdf
│       └── phase2.tex
├── src/
│   ├── build_notebook.py
│   ├── build_report.py
│   └── phase2_analysis.py
└── tables/
    ├── apoe_groups.csv
    ├── binomial_model.csv
    ├── joint_counts.csv
    ├── missing.csv
    ├── moments.csv
    ├── mri_groups.csv
    └── results.csv
```

## Requirements

-   Python 3.10 or later is recommended.
-   Python packages are listed in `requirements.txt`.
-   Jupyter is required to execute the notebook.
-   Report generation with `src/build_report.py` requires ReportLab.
-   Compiling the LaTeX source separately requires a working LaTeX
    installation with `pdflatex`.

Install the Python dependencies from the project root:

``` bash
python -m pip install -r requirements.txt
```

## Reproducing the analysis

Run all commands from the project root directory.

### 1. Rebuild the analysis tables and figures

``` bash
python src/phase2_analysis.py
```

This script reads the two CSV input files and writes the derived tables
to `tables/` and figures to `figures/`.

### 2. Execute the notebook

``` bash
jupyter nbconvert --to notebook --execute --inplace notebooks/phase2_probability.ipynb
```

This executes the notebook and saves the resulting cell outputs in
place. To regenerate the notebook source structure before execution,
use:

``` bash
python src/build_notebook.py
```

The notebook builder recreates the notebook source; execute the notebook
afterward if you need fresh outputs.

### 3. Build the report PDF and LaTeX source

``` bash
python src/build_report.py
```

The report builder uses the generated tables and figures. It writes the
ReportLab PDF to `reports/phase2/phase2.pdf`, copies that PDF to
`reports/phase2.pdf`, and writes the LaTeX source to
`reports/phase2/phase2.tex`.

The two PDF paths produced by this script are copies of the same
ReportLab-generated PDF.

### 4. Optionally compile the LaTeX source independently

From the project root:

``` bash
cd reports/phase2
pdflatex -interaction=nonstopmode -halt-on-error phase2.tex
pdflatex -interaction=nonstopmode -halt-on-error phase2.tex
```

This creates a PDF from the LaTeX source in `reports/phase2/phase2.pdf`,
replacing the ReportLab PDF at that path. The LaTeX-generated PDF may
differ in pagination and layout from the ReportLab-generated PDF at
`reports/phase2.pdf`. If both versions are retained, they should be
identified as separate renderings rather than described as identical. To
restore the canonical ReportLab outputs, rerun
`python src/build_report.py` from the project root.

## Outputs

### Tables

The analysis writes:

-   `tables/results.csv` --- principal sample counts, probabilities,
    thresholds, covariance values, and related results.
-   `tables/joint_counts.csv` --- joint event counts.
-   `tables/mri_groups.csv` --- cognitive event summaries by MRI
    thickness grouping.
-   `tables/apoe_groups.csv` --- cognitive event summaries by recorded
    `NACCAPOE` category.
-   `tables/moments.csv` --- empirical means, variances, quantiles,
    ranges, and Tukey outlier counts.
-   `tables/missing.csv` --- missing-value counts for the core variables
    in the joined analysis data.
-   `tables/binomial_model.csv` --- probabilities for the illustrative
    binomial model.

### Figures

The analysis writes:

-   `figures/binomial.png` --- hypothetical binomial count model.
-   `figures/distributions.png` --- observed distributions of `CDRSUM`
    and left entorhinal thickness.
-   `figures/qq.png` --- normal Q--Q plot for left entorhinal thickness.
-   `figures/scatter.png` --- bilateral entorhinal thickness plotted
    against `CDRSUM`.

## Statistical interpretation

The probability calculations describe the empirical distribution of the
eligible records in the supplied matched dataset. They should not be
interpreted as estimates for the general population.

The binomial calculation is explicitly hypothetical: it models
independent draws with replacement using the observed empirical event
probability. It is not a claim that the actual sample was generated by
independent repeated draws. Sampling distinct participants without
replacement would instead have a finite-population sampling structure.

Covariance is calculated using the population-form empirical denominator
`n` on available pairs. It is a scale-dependent descriptive measure; it
is not a correlation coefficient, regression model, significance test,
or causal effect.

The distribution summaries describe the observed values. They do not
automatically validate a normal model, and outlier flags are descriptive
indicators rather than instructions to delete observations.

## Data and methodological limitations

Interpret the results in light of the following limitations:

1.  **Imputed UDS input:** `udslong_imputed.csv` is already imputed. The
    project does not perform a new imputation, and the original
    missingness mechanism and imputation details are not established by
    the supplied file alone.
2.  **Undocumented codes:** `NACCAPOE` is treated as a recorded category
    only. No genotype or allele interpretation---including for code
    `9`---is assigned without an authoritative NACC codebook.
3.  **Unusual `MOCATOTS` values:** The supplied values include `88`,
    values above 30, and fractional values. Without the relevant
    codebook and imputation documentation, these values cannot be safely
    interpreted as ordinary test scores. `CDRSUM` is therefore used as
    the principal quantitative cognitive measure.
4.  **Visit and scan timing:** Matching `NACCID` values do not establish
    that UDS and MRI records were collected at the same visit or
    contemporaneously. Historical visit counts and temporal alignment
    cannot be reconstructed from these files.
5.  **Independence:** One supplied row per participant does not prove
    statistical independence between participants.
6.  **MRI selection:** The MRI-selected sample may not represent the
    wider NACC population. The supplied files do not provide a suitable
    UDS-only comparison group for evaluating MRI selection.
7.  **Sample-specific threshold:** The left-thickness median is
    calculated from the eligible analysis sample. It is not a validated
    clinical threshold.
8.  **Descriptive scope:** The analyses do not establish causality,
    temporal prediction, or clinical diagnostic performance.

The results should be revisited if authoritative codebooks, original
missingness information, imputation metadata, or reliable visit/scan
dates become available.

## Project status

This repository is scoped to **Phase 2, Path C**. The notebook and
report organize the work under Shared Tasks 1--9 and Path C Tasks
C1--C5. The presence of these sections is not, by itself, a
certification of compliance with every detail of an external assignment
rubric; the official rubric should be checked directly before
submission.

No Phase 3--5 analyses are included.
