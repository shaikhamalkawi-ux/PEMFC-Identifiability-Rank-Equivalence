# v11 reproduction targets

## Locked core results

- Ballard full-model SSE: **0.8139117034917056**; published rounded value **0.813911703**.
- Ballard transformed pair at delta = 3e-4: **(-1.18894672, 0.003996006654)**.
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

The c1+c2 design is locally full rank but has almost tangent condition-specific nullspaces. Same-temperature pressure diversity collapses the low-temperature nullity from 2 to 1; temperature diversity then separates the remaining universal fixed-temperature direction.

## v11 Fisher / OED / rank-distance interpretation

At equal observation count (30 versus 30):

| Metric | c1+c2 | matched 30 | matched/c1+c2 |
|---|---:|---:|---:|
| box-scaled trace information | 48060.3819 | 51313.1559 | 1.067681 |
| E-information | 4.873228e-13 | 2.142465e-3 | 4.396398e9 |
| D-information geometric mean | 0.31488297 | 14.05892323 | 44.648091 |
| A-information | 3.411260e-12 | 1.473949e-2 | 4.320834e9 |
| normalized Gram determinant | 3.454056e-24 | 7.822967e-13 | 2.264864e11 |
| normalized sigma_7 rank distance | 1.254448e-8 | 5.498555e-3 | 4.383247e5 |

The matched design adds only **6.8%** total box-scaled sensitivity but increases the weakest-direction information by **4.40e9**. Its normalized sensitivity matrix is about **4.38e5** times farther from rank loss in spectral norm.

Adding c4 to c1+c2+c3 slightly worsens the primary column-normalized condition number (409.65 -> 451.88) while increasing box-scaled E-information by **22.5%**, D-information by **23.7%**, A-information by **22.2%**, and the information trace by **33.0%**. This verifies that condition number is not a monotone measure of total information.

## Claim boundary

Principal angles and information criteria are computed under declared common scalings and are local diagnostics. Fisher/confidence-region interpretations assume the usual local linearization and independent homoscedastic Gaussian voltage errors. The deterministic matched 30-point design is not claimed to be globally optimal among all possible 30-point designs.
