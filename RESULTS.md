# v13 reproduction targets

## Locked core results

- Ballard full-model SSE: **0.8139117034917056**; published rounded value **0.813911703**.
- Ballard transformed pair at delta = 3e-4: **(-1.18894672, 0.003696006654)**.
- max |Delta V| = **0** and Delta SSE = **0** in evaluated double precision.
- analytic vs complex-step maximum relative Jacobian discrepancy: **2.1461482414765403e-16**.
- c1 rank 5; c2 rank 5; c2+c3+c4 rank 6; c1+c2 rank 7; all-four rank 7.
- c1+c2 column-normalized cond2 = **1.97849689e8**.
- all-four column-normalized cond2 = **451.883733868**.
- observation-count-matched all-four 30-point cond2 = **447.223138834**.

## Possibilistic temperature-level robustness

For triangular high/low temperature-level supports with half-width h = 4.9 K:

- all sampled c1+c2 and matched-four realizations remain local rank 7;
- at alpha = 0, c1+c2 cond2 range is about **6.90e7 to 4.04e11**;
- matched-four range is about **229.5 to 2.12e4**;
- conservative best-two / worst-four separation is about **3.26e3**;
- at h = 5 K, rank-6 realizations first become admissible at the support-touching boundary.

## Symmetry/nullspace geometry

Using common parameter-box scaling:

| Design | low-T rank | low-T nullity | theta_min (deg) | box cond2 | column cond2 |
|---|---:|---:|---:|---:|---:|
| c1+c2 | 5 | 2 | 1.69e-4 | 2.976e8 | 1.9785e8 |
| c1+c3 | 5 | 2 | 4.89e-4 | 1.015e8 | 5.278e7 |
| c1+c4 | 5 | 2 | 2.34e-4 | 2.134e8 | 1.350e8 |
| c1+c2+c3 | 6 | 1 | 0.377286 | 4.388e3 | 409.65 |
| c1+c2+c4 | 6 | 1 | 0.377286 | 4.374e3 | 852.39 |
| c1+c3+c4 | 6 | 1 | 0.377286 | 4.431e3 | 438.05 |
| all four | 6 | 1 | 0.377286 | 4.570e3 | 451.88 |

## Fisher / OED / rank-distance interpretation

At equal observation count (30 versus 30):

| Metric | c1+c2 | matched 30 | matched/c1+c2 |
|---|---:|---:|---:|
| box-scaled trace information | 48060.3819 | 51313.1559 | 1.067681 |
| E-information | 4.873228e-13 | 2.142465e-3 | 4.396398e9 |
| D-information geometric mean | 0.31488297 | 14.05892323 | 44.648091 |
| A-information | 3.411260e-12 | 1.473949e-2 | 4.320834e9 |
| normalized Gram determinant | 3.454056e-24 | 7.822967e-13 | 2.264864e11 |
| normalized sigma_7 rank distance | 1.254448e-8 | 5.498555e-3 | 4.383247e5 |

## v13 symmetry-breaking-order result

| Low-temperature pressure subset | eta1 | fitted exponent p | sigma_min at 0.1 K |
|---|---:|---:|---:|
| c2 | 1.2837e-16 | 1.998926 | 1.0457e-10 |
| c3 | 2.9836e-16 | 2.001547 | 1.7103e-10 |
| c4 | 1.5238e-16 | 1.999643 | 1.1064e-10 |
| c2+c3 | 5.1230e-2 | 0.999806 | 5.1240e-3 |
| c2+c4 | 2.0501e-2 | 1.000429 | 2.0505e-3 |
| c3+c4 | 4.3925e-2 | 1.000427 | 4.3934e-3 |
| c2+c3+c4 | 5.1784e-2 | 1.000036 | 5.1800e-3 |

One pressure condition per temperature level gives quadratic opening of the weakest singular direction; two or more low-temperature pressures give linear opening. At DeltaT = 0.1 K the c1+(c2+c3+c4) opening is about **4.95e7** times the c1+c2 opening.

## v13 gauge-fixing / prior-dependence result

The exact Ballard orbit has feasible delta interval

**[-6.788534110787171e-4, 3.313215160349855e-4]**.

| Rule | delta | xi1 | xi2 |
|---|---:|---:|---:|
| published THRO representative | 0 | -1.08604672 | 0.003696006654 |
| raw-coordinate L2 toward zero | -6.7885341108e-4 | -0.8532 | 0.003017153243 |
| raw-coordinate L2 toward box midpoint | -1.7377038672e-4 | -1.026443477 | 0.003522236268 |
| box-normalized L2 toward box midpoint | -2.0507664679e-4 | -1.015705430 | 0.003490930007 |

For every row, **max |Delta V| = 0** and **Delta SSE = 0** in evaluated double precision.

## Unified closure

- `python scripts/reproduce_v13_all.py`: **PASS**.
- All 37 bibliography entries are cited; no missing or unused keys remain.
- The exploratory nine-point greedy D-optimal design is not a manuscript result and is held for future cost/noise-aware validation.

## Claim boundary

Principal angles, perturbation coefficients, and information criteria are local diagnostics under declared scalings. Fisher/confidence interpretations assume the stated local Gaussian-error model. The symmetry-breaking power laws are local near the equal-temperature boundary and are not asserted as exact global laws. Gauge fixing describes representative selection along an exact likelihood-flat orbit; a physically justified external prior may still add genuine external information.
