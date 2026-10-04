# Locked reproduction targets

The manuscript audit reports the following column-normalized Jacobian behavior for the 250 W benchmark.

| Design | Rank | Normalized singular values (rounded) |
|---|---:|---|
| c1 | 5 | [2.4840508, 0.8306930, 0.3392128, 0.1549275, 0.0193166, ~4e-17, ~8e-18] |
| c2 | 5 | [2.4813946, 0.8320850, 0.3521625, 0.1609522, 0.0197800, ~6e-17, ~5e-18] |
| c2+c3+c4 | 6 | smallest singular value ~1.9e-16 |
| c1+c2 | 7 | smallest singular value ~1.25445e-8; kappa2 ~1.9785e8 |
| all four | 7 | smallest singular value ~5.49376e-3; kappa2 ~4.5188e2 |

For the Ballard Mark V THRO pair used in the manuscript:

- T0 = 343 K
- xi1 = -1.08604672
- xi2 = 0.003696006654
- delta = 3e-4
- transformed pair = (-1.18894672, 0.003996006654)
- feasible delta interval is approximately [-6.78853e-4, 3.31322e-4]
- max |Delta V| = 0 in the evaluated double-precision invariance check
- Delta SSE = 0

The algebraic invariance is exact; the floating-point outputs above are reproducibility diagnostics.
