# PEMFC Identifiability: Rank and Equivalence

[![reproduce](https://github.com/shaikhamalkawi-ux/PEMFC-Identifiability-Rank-Equivalence/actions/workflows/reproduce.yml/badge.svg)](https://github.com/shaikhamalkawi-ux/PEMFC-Identifiability-Rank-Equivalence/actions/workflows/reproduce.yml)

Reproducibility materials for:

**Experiment-Conditioned Parameter Redundancy in Seven-Parameter PEMFC Models: Exact Equivalence and Rank-Aware Experimental Design**

**Repository author: Ghassan Malkawi**

This repository reproduces the manuscript's structural-identifiability, experimental-design, possibilistic-robustness, and symmetry/nullspace-geometry results for the common seven-free-parameter Amphlett-type PEMFC benchmark.

## What is reproduced

1. Complete Ballard Mark V replay and exact fixed-temperature invariance.
2. Exact fixed-temperature and affine-log null directions.
3. Full seven-parameter analytic Jacobian and independent complex-step verification.
4. 250 W rank/conditioning sequence: rank 5, rank 6, rank 7 with severe conditioning, then rank 7 with substantially lower conditioning.
5. Observation-count-matched 30-point four-condition design.
6. Lambda-range and common parameter-box scaling robustness.
7. Out-of-temperature ambiguity induced by the fixed-temperature equivalence family.
8. Possibilistic temperature-level stress test over nested alpha-cuts, including the exact 5 K support-touching threshold.
9. Parameter-symmetry and nullspace-principal-angle interpretation:
   - fixed-T transformation as a one-parameter output-preserving symmetry action;
   - affine-log case as a commuting two-parameter action;
   - quotient invariants matching the reduced coordinates;
   - principal-angle diagnostics in common parameter-box coordinates.

## Key v10 geometry values at lambda = 13.23

| Design | low-T nullity | smallest principal angle | column-normalized cond2 |
|---|---:|---:|---:|
| c1+c2 | 2 | 1.69e-4 deg | 1.9785e8 |
| c1+c3 | 2 | 4.89e-4 deg | 5.2780e7 |
| c1+c4 | 2 | 2.34e-4 deg | 1.3502e8 |
| c1+c2+c3 | 1 | 0.377286 deg | 409.65 |
| all four | 1 | 0.377286 deg | 451.88 |

The principal angle is a scaling-dependent diagnostic, not a theorem determining the full condition number. All quoted angles use the same published parameter-box metric.

## Numerical-rank definition

Numerical rank uses the NumPy/LAPACK-style tolerance `tau = sigma_1 * max(m,n) * eps_machine`.

## Scaling definition

The common parameter-box scaling is `J_box = J diag(U_1-L_1, ..., U_7-L_7)`.

## Run

```bash
python -m pip install -r requirements.txt
python scripts/reproduce_all.py
python scripts/possibilistic_temperature_levels.py
python scripts/symmetry_nullspace_geometry.py
python scripts/make_figures.py
```

## Interpretation boundary

The fixed-temperature continuous feasible equivalence establishes non-injectivity. Multi-temperature rank 7 is a local numerical-rank result and is not claimed to prove global identifiability. Lie/parameter symmetries and principal angles are established mathematical tools; their use here is explanatory and benchmark-specific, not claimed as a new mathematical theory.

## Data provenance

The benchmark arrays and operating conditions are traced to Bouali et al., Scientific Reports 16, 4980 (2026), DOI **10.1038/s41598-026-35200-6**.
