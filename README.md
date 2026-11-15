# PEMFC Identifiability: Rank, Symmetry, and Experimental Design

[![reproduce](https://github.com/shaikhamalkawi-ux/PEMFC-Identifiability-Rank-Equivalence/actions/workflows/reproduce.yml/badge.svg)](https://github.com/shaikhamalkawi-ux/PEMFC-Identifiability-Rank-Equivalence/actions/workflows/reproduce.yml)

Reproducibility materials for:

**Experiment-Conditioned Parameter Redundancy in Seven-Parameter PEMFC Models: Exact Equivalence and Rank-Aware Experimental Design**

**Repository author: Ghassan Malkawi**

This repository reproduces the manuscript's structural-identifiability, experimental-design, possibilistic-robustness, symmetry/nullspace-geometry, information-geometry, local symmetry-breaking-order, and gauge-fixing results for the common seven-free-parameter Amphlett-type PEMFC benchmark.

## What is reproduced

1. Complete Ballard Mark V replay and exact fixed-temperature voltage/SSE invariance.
2. Exact fixed-temperature and affine-log full-Jacobian null directions.
3. Prediction-equivalent six- and five-coordinate quotient parameterizations.
4. 250 W rank/conditioning sequence: rank 5, rank 6, rank 7 with severe conditioning, and rank 7 with substantially lower conditioning.
5. Observation-count-matched 30-point four-condition comparison.
6. Lambda-range and common parameter-box scaling robustness.
7. Out-of-temperature ambiguity induced by the fixed-temperature equivalence family.
8. Possibilistic temperature-level stress test over nested alpha-cuts, including the exact 5 K support-touching threshold.
9. Parameter-symmetry and nullspace-principal-angle interpretation.
10. Fisher/E/D/A, Gram-volume, and Eckart-Young distance-to-rank-loss diagnostics.
11. Local order of symmetry breaking near the equal-temperature boundary:
    - one pressure condition per temperature level gives quadratic opening of the weakest singular direction;
    - prior same-temperature pressure diversity changes the opening to linear.
12. Prior/regularization dependence as gauge fixing:
    - the voltage likelihood is constant along the exact equivalence orbit;
    - a prior, penalty, bound, or parameter convention may select a representative without adding voltage-data information along the null direction.

## Key structural and numerical results

- Ballard full-model SSE: `0.8139117034917056`.
- Ballard exact displacement: `max |Delta V| = 0`, `Delta SSE = 0`.
- Analytic/complex-step maximum relative Jacobian discrepancy: `2.1461482414765403e-16`.
- c1 rank 5; c2 rank 5; c2+c3+c4 rank 6; c1+c2 and all-four rank 7.
- c1+c2 column-normalized `cond2 = 1.97849689e8`.
- all-four `cond2 = 451.883733868`.
- observation-count-matched all-four 30-point `cond2 = 447.223138834`.

## Symmetry-breaking order

Near the equal-temperature boundary, with published parameter-box scaling:

| Low-temperature block | first-order coefficient eta1 | fitted exponent p |
|---|---:|---:|
| c2 | 1.28e-16 | 1.99893 |
| c3 | 2.98e-16 | 2.00155 |
| c4 | 1.52e-16 | 1.99964 |
| c2+c3 | 5.12e-2 | 0.99981 |
| c2+c4 | 2.05e-2 | 1.00043 |
| c3+c4 | 4.39e-2 | 1.00043 |
| c2+c3+c4 | 5.18e-2 | 1.00004 |

Thus one pressure condition per temperature level yields `sigma_7 = O(DeltaT^2)`, while two or more low-temperature pressures yield `sigma_7 = O(|DeltaT|)`. At `DeltaT = 0.1 K`, the c1+(c2+c3+c4) weakest direction opens about `4.95e7` times more than c1+c2.

## Equal-count information result

Both designs use 30 voltage observations.

| Metric | c1+c2 | matched four-condition | improvement |
|---|---:|---:|---:|
| trace information | 4.8060e4 | 5.1313e4 | 1.0677x |
| E-information | 4.8732e-13 | 2.1425e-3 | 4.3964e9x |
| D-information geometric mean | 0.314883 | 14.0589 | 44.6481x |
| A-information | 3.4113e-12 | 1.4739e-2 | 4.3208e9x |
| normalized sigma_7 distance | 1.25445e-8 | 5.49855e-3 | 4.38325e5x |

The benefit is mainly redistribution of information into previously weak directions, not simple growth in total sensitivity.

## Gauge-fixing result

Along the exact Ballard orbit

`theta(delta) = theta0 + delta*(-T0,1,0,0,0,0,0)`,

the voltage likelihood is constant. For a quadratic penalty centered at `mu` with precision matrix `Lambda`, the selected unconstrained representative is

`delta* = -v^T Lambda (theta0-mu) / (v^T Lambda v)`,

clipped to the feasible delta interval. Different raw-coordinate and box-normalized penalties select different `(xi1,xi2)` pairs while preserving identical Ballard voltages and SSE.

## Run

```bash
python -m pip install -r requirements.txt
python scripts/reproduce_v13_all.py
```

Or run individual layers:

```bash
python scripts/reproduce_v7.py
python scripts/possibilistic_temperature_levels.py
python scripts/symmetry_nullspace_geometry.py
python scripts/information_geometry_oed.py
python scripts/symmetry_breaking_order.py
python scripts/gauge_fixing_prior_dependence.py
```

## Interpretation boundary

The fixed-temperature continuous feasible equivalence establishes non-injectivity. Multi-temperature rank 7 is a local numerical-rank result and is not claimed to prove global identifiability. The perturbation power laws are local and benchmark-specific under the declared scaling, pressure law, and reference lambda. Principal angles and information criteria use declared common scalings. Fisher/confidence interpretations are local and require the stated error assumptions. Fuzzy sets are stress-test possibility distributions, not calibrated sensor uncertainties. A physically justified external prior may add external information, but it does not make the voltage likelihood informative along an exact null direction. The exploratory nine-point greedy design is not a manuscript result.

## Data provenance

The benchmark arrays and operating conditions are traced to Bouali et al., *Scientific Reports* 16, 4980 (2026), DOI **10.1038/s41598-026-35200-6**.
