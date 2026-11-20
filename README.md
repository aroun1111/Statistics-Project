# Phase 2 probability — Path C (NACC)

This is a descriptive continuation of Phase 1: recorded NACCAPOE codes, CDR measures and left/right entorhinal thickness. All probabilities describe the supplied matched dataset, not the wider population. The PDF is `reports/phase2.pdf`; LaTeX source is `reports/phase2/phase2.tex`. The label is `phase-2` (also recorded in `PHASE_LABEL`).

## Reproduce
From this directory, Python 3.10+ with pandas, numpy, scipy, matplotlib, nbformat and nbclient:

```
python -m pip install -r requirements.txt
python src/phase2_analysis.py
jupyter nbconvert --to notebook --execute --inplace notebooks/phase2_probability.ipynb
```
C1 reports the cognitive event in two distinct groupings: MRI below versus at/above the sample median, and recorded NACCAPOE categories. Task coverage tables appear in the notebook and report. The notebook contains the actual calculations, separately organized by task; `python src/build_notebook.py` recreates its unexecuted source if needed. The notebook locates the project root from the notebook directory or root. `src/phase2_analysis.py` produces `tables/*.csv` and `figures/*.png`. `python src/build_report.py` regenerates both the PDF and LaTeX source from those outputs (requires reportlab). To independently compile the LaTeX, run `cd reports/phase2 && pdflatex phase2.tex` twice; the bundled PDF is generated from the same report content with ReportLab because a TeX engine was unavailable in the execution environment.

Inputs are included unchanged from the supplied archives. They may contain sensitive research data; share only with authorization. `PROJECT_CARD.md` describes the current Phase 2 question, replacing the earlier Phase 1 card; its early mediation proposal is not implemented. See report for data provenance and limitations. The supplied adjacency matrix is not needed for this question and is not joined. Repeated historical visits and temporal matching cannot be reconstructed from these files. Do not infer biological meanings of NACCAPOE codes without the relevant NACC codebook. MOCATOTS includes 88 and values above 30 or fractional; its imputed source and undocumented codes preclude a defensible score analysis here, so CDRSUM is used instead. Outputs are descriptive; no bootstrap, tests, correlations, regressions or causal inference.
