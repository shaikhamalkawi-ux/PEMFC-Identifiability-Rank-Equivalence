# PEMFC Identifiability: Rank and Equivalence

[![reproduce](https://github.com/shaikhamalkawi-ux/PEMFC-Identifiability-Rank-Equivalence/actions/workflows/reproduce.yml/badge.svg)](https://github.com/shaikhamalkawi-ux/PEMFC-Identifiability-Rank-Equivalence/actions/workflows/reproduce.yml)

Reproducibility materials for the manuscript:

**Exact Experiment-Conditioned Parameter Redundancy in the Seven-Parameter PEMFC Benchmark**

**Repository author: Ghassan Malkawi**

This repository reproduces the paper's core mathematical/numerical checks for the common seven-free-parameter Amphlett-type PEMFC benchmark.

## What is reproduced

1. **Exact fixed-temperature invariance**
   `(xi1, xi2) -> (xi1 - T0*delta, xi2 + delta)`, which leaves the activation term and therefore the complete predicted voltage unchanged when all other parameters are held fixed.

2. **Feasible equivalence intervals under box constraints**
   `D=[(xi1-U1)/T0,(xi1-L1)/T0] intersect [L2-xi2,U2-xi2]`.

3. **Full seven-parameter Jacobian structure**
   for the air-fed 250 W implementation used in the benchmark audit.

4. **Column-normalized singular-value/rank audit**
   for one fixed condition, same-temperature pressure diversity, the published two-temperature extraction set, and all four operating conditions.

5. **Rank-first, conditioning-second design result**
   showing that structural rank restoration and practical conditioning are distinct experimental-design requirements.

## Expected numerical results

Using the reference point `lambda = 13.23` for the membrane-resistance sensitivity column:

| Design | Numerical rank | Smallest normalized singular value | Normalized condition number |
|---|---:|---:|---:|
| c1 only | 5 | ~8e-18 | structurally singular |
| c2 only | 5 | ~5e-18 | structurally singular |
| c2+c3+c4 (same T) | 6 | ~2e-16 | structurally singular |
| c1+c2 | 7 | ~1.25e-8 | ~1.98e8 |
| c1+c2+c3+c4 | 7 | ~5.49e-3 | ~4.52e2 |

The exact rank-deficiency statements follow analytically from null directions; floating-point singular values are diagnostic reproductions, not the proof.

## Run

```bash
python -m pip install -r requirements.txt
python scripts/reproduce_all.py
```

Python 3.10+ is recommended.

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

## Repository status

Research reproducibility repository for the current manuscript version. The mathematical identities are exact; reported SVD values are floating-point diagnostics and may differ in the last digits across BLAS/LAPACK implementations.
