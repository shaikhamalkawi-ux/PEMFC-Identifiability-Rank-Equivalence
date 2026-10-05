# PEMFC Identifiability: Rank and Equivalence

[![reproduce](https://github.com/shaikhamalkawi-ux/PEMFC-Identifiability-Rank-Equivalence/actions/workflows/reproduce.yml/badge.svg)](https://github.com/shaikhamalkawi-ux/PEMFC-Identifiability-Rank-Equivalence/actions/workflows/reproduce.yml)

Reproducibility materials for the manuscript:

**When Seven PEMFC Parameters Are Not Seven Identifiable Quantities: Exact Redundancy and Rank-Aware Experimental Design**

**Repository author: Ghassan Malkawi**

This repository reproduces the manuscript's core mathematical and numerical results for the common seven-free-parameter Amphlett-type PEMFC benchmark.

## What is reproduced

1. **Exact fixed-temperature invariance**
   `(xi1, xi2) -> (xi1 - T0*delta, xi2 + delta)`, which leaves predicted voltage unchanged when all other fitted parameters are fixed.

2. **Feasible equivalence intervals under box constraints**
   `D=[(xi1-U1)/T0,(xi1-L1)/T0] intersect [L2-xi2,U2-xi2]`.

3. **Full seven-parameter analytic Jacobian**
   for the air-fed 250 W implementation.

4. **Independent complex-step derivative verification**
   of all seven analytic Jacobian columns.

5. **Column-normalized singular-value/rank analysis**
   for one fixed condition, same-temperature pressure diversity, the published two-temperature extraction set, and all four operating conditions.

6. **Manuscript figure regeneration**
   from the same numerical implementation.

Editable LaTeX for the manuscript's core equations is provided in `paper/core_equations.tex`.

## Expected numerical results

Using the reference point `lambda = 13.23` for the membrane-resistance sensitivity column:

| Design | Numerical rank | Smallest normalized singular value | Normalized condition number |
|---|---:|---:|---:|
| c1 only | 5 | machine zero, O(1e-17), platform dependent | structurally singular |
| c2 only | 5 | machine zero, O(1e-17), platform dependent | structurally singular |
| c2+c3+c4 (same T) | 6 | machine zero, O(1e-16), platform dependent | structurally singular |
| c1+c2 | 7 | ~1.254e-8 | ~1.98e8 |
| c1+c2+c3+c4 | 7 | ~5.494e-3 | ~4.52e2 |

The current complex-step run gives a maximum relative column discrepancy of approximately `2.15e-16`. Exact rank-deficiency statements follow analytically from null directions. For structurally singular designs, the tiny floating-point singular values vary across NumPy/LAPACK environments and are therefore treated as machine-zero diagnostics rather than locked numerical targets. The full-rank condition numbers above are stable across the automated Python 3.10, 3.11, and 3.12 checks.

## Run

```bash
python -m pip install -r requirements.txt
python scripts/reproduce_all.py
python scripts/make_figures.py
```

Python 3.10+ is recommended. The automated workflow runs on Python 3.10, 3.11, and 3.12.

## Data provenance

The current vectors and operating conditions used here come from the public benchmark repository:

**Yacine-Bouali/Benchmark-Data-for-PEMFC-Parameter-Extraction**

associated with:

Y. Bouali, K. Imarazene, B. Alamri, and E. M. Berkouk,  
"Optimization of proton exchange membrane fuel cell design parameters using Tianji's horse racing optimization,"  
*Scientific Reports*, 16, 4980 (2026).  
DOI: **10.1038/s41598-026-35200-6**

This repository stores only the minimal numerical arrays needed for the rank/invariance reproduction. See `data/README.md` for provenance and scope.

## Scope

This code supports the paper's narrow claim: an **experiment-conditioned rank/nullspace and equivalence-class characterization** for the seven-free-parameter benchmark. It does **not** claim that PEMFC identifiability, coefficient grouping, or separable regression are new topics.

## Associated paper

**When Seven PEMFC Parameters Are Not Seven Identifiable Quantities: Exact Redundancy and Rank-Aware Experimental Design**

Submission-candidate manuscript files are maintained separately from this reproducibility repository. The repository authorship record remains in `AUTHORS.md` and `CITATION.cff`.
