# Locked v6 reproduction targets

## Complete Ballard Mark V replay

Using the published Ballard benchmark convention and THRO parameter vector:

- reproduced SSE: **0.8139117034917056**
- published rounded SSE: **0.813911703**
- feasible delta interval: approximately **[-6.788534e-4, 3.313215e-4]**
- chosen delta: **3e-4**
- transformed pair: **(-1.18894672, 0.003996006654)**
- max |Delta V|: **0**
- Delta SSE: **0**

The fixed-temperature invariance is algebraic; the complete-model replay verifies that the published benchmark implementation preserves it.

## Jacobian verification

- analytic vs independent complex-step maximum relative column discrepancy: **2.1461482414765403e-16**
- fixed-pressure null-vector residual: below **1e-12** (current replay about **3.06e-20**)

## Reference lambda = 13.23, column-normalized Jacobian

| Design | Observations | Rank | Condition metric |
|---|---:|---:|---:|
| c1 | 15 | 5 | structurally singular |
| c2 | 15 | 5 | structurally singular |
| c2+c3+c4 | 45 | 6 | structurally singular |
| c1+c2 | 30 | 7 | 1.97849689e8 |
| c1+c2+c3 | 45 | 7 | 409.652944671 |
| all four | 60 | 7 | 451.883733868 |
| balanced all-four | 30 | 7 | 447.223138834 |

Condition number is not a monotone measure of total information: c1+c2+c3 has a slightly lower scaled condition number than the all-four design at the reference point.

## Lambda robustness

On a deterministic 501-point grid over the published **lambda in [10,24]** range:

- c1 remains rank 5;
- c2 remains rank 5;
- c2+c3+c4 remains rank 6;
- c1+c2 remains rank 7 with column-normalized condition number about **1.75e8 to 2.69e8**;
- all four remains rank 7 with about **428.5 to 498.9**;
- balanced all-four 30 remains rank 7 with about **426.2 to 487.6**.

With common parameter-box scaling, the absolute numbers change but the orders-of-magnitude separation persists.

## Claim boundary

The fixed-temperature transformation proves finite non-injectivity along a feasible equivalence class. Multi-temperature rank 7 proves only full local numerical rank at the evaluated point, not global identifiability.
