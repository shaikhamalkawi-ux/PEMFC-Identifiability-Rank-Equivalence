# PEMFC Identifiability: Rank and Equivalence

[![reproduce](https://github.com/shaikhamalkawi-ux/PEMFC-Identifiability-Rank-Equivalence/actions/workflows/reproduce.yml/badge.svg)](https://github.com/shaikhamalkawi-ux/PEMFC-Identifiability-Rank-Equivalence/actions/workflows/reproduce.yml)

Reproducibility materials for the manuscript:

**Experiment-Conditioned Parameter Redundancy in Seven-Parameter PEMFC Models: Exact Equivalence and Rank-Aware Experimental Design**

**Repository author: Ghassan Malkawi**

This repository reproduces the manuscript's structural-identifiability and experimental-design results for the common seven-free-parameter Amphlett-type PEMFC benchmark.

## What is reproduced

1. **Complete Ballard Mark V replay and exact fixed-temperature invariance**
   - full Nernst, activation, membrane/ohmic, and concentration model;
   - reproduced THRO SSE: `0.8139117034917056` versus published rounded `0.813911703`;
   - `(xi1,xi2) -> (xi1-T0*delta,xi2+delta)` gives `max |Delta V|=0` and `Delta SSE=0` in the evaluated arithmetic.

2. **Exact null directions**
   - the universal fixed-temperature xi1/xi2 direction;
   - the second fixed-pressure / affine-log oxygen-law direction.

3. **Full seven-parameter analytic Jacobian**
   - independently verified by complex-step differentiation;
   - current maximum relative column discrepancy is approximately `2.15e-16`.

4. **Rank and conditioning of the 250 W benchmark**
   - c1: rank 5;
   - c2: rank 5;
   - c2+c3+c4 at one temperature: rank 6;
   - c1+c2: local rank 7, `cond2 ~ 1.98e8`;
   - all four conditions: local rank 7, `cond2 ~ 4.52e2`.

5. **Equal-budget design check**
   A deterministic 30-observation design distributed across all four conditions remains rank 7 and gives `cond2 ~ 447.22`, compared with `~1.98e8` for the 30-observation c1+c2 design.

6. **Robustness checks**
   - deterministic 501-point sweep over the published `lambda in [10,24]` range;
   - primary unit-column normalization and common published parameter-box scaling;
   - the orders-of-magnitude conditioning separation between c1+c2 and the more diverse designs persists.

7. **Out-of-temperature ambiguity**
   Equivalent fixed-temperature parameter representatives can diverge when extrapolated to another temperature. For `delta=3e-4` and a 10 K change, the induced difference is 3 mV/cell, or 0.105 V for the 35-cell Ballard stack.

## Interpretation boundary

The fixed-temperature finite transformation establishes non-injectivity along a feasible equivalence class. By contrast, rank 7 at a multi-temperature evaluation point establishes only full local numerical rank; it does not prove global identifiability. Condition number is a scale-dependent anisotropy measure, not a monotone measure of total information.

## Run

```bash
python -m pip install -r requirements.txt
python scripts/reproduce_all.py
python scripts/make_figures.py
```

Python 3.10+ is recommended. The automated workflow runs on Python 3.10, 3.11, and 3.12.

## Data provenance

The current vectors, operating conditions, published parameter bounds, and benchmark parameter values come from:

Y. Bouali, K. Imarazene, B. Alamri, and E. M. Berkouk,
"Optimization of proton exchange membrane fuel cell design parameters using Tianji's horse racing optimization,"
*Scientific Reports*, 16, 4980 (2026).
DOI: **10.1038/s41598-026-35200-6**

The repository stores only the minimal numerical arrays needed for the rank/invariance reproduction. See `data/README.md` for provenance and scope.

## Scope

The contribution is an **experiment-conditioned rank/nullspace and equivalence-class characterization** and its benchmark/design consequences. It does not claim that PEMFC identifiability, coefficient grouping, or separable regression are new topics.
