# v10 reproduction targets

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

## Claim boundary

Principal angles are computed under the declared common parameter-box metric and are used as geometric diagnostics. They do not by themselves determine the full condition number.
