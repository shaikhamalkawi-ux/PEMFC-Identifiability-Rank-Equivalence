# v10 reproducibility closure

Closure date: 14 November 2026

Associated manuscript:

**Experiment-Conditioned Parameter Redundancy in Seven-Parameter PEMFC Models: Exact Equivalence and Rank-Aware Experimental Design**

Repository author: **Ghassan Malkawi**

## v10 closure status

- Complete Ballard Mark V voltage-model replay: PASS.
- Exact fixed-temperature voltage/SSE invariance: PASS.
- Fixed-pressure / affine-log second null direction: PASS.
- Full seven-column analytic Jacobian audit: PASS.
- Independent complex-step derivative check: PASS.
- Single-condition rank 5: PASS.
- Same-temperature pressure-diversity rank 6: PASS.
- c1+c2 local rank 7 with severe conditioning: PASS.
- Observation-count-matched four-condition 30-point design: PASS.
- Lambda-grid and parameter-box scaling robustness: PASS.
- Possibilistic temperature-level robustness: PASS.
- Symmetry-generator residual checks: PASS.
- Nullspace-principal-angle calculations: PASS.

## v10 interpretation layer

The exact fixed-temperature transformation is written as a one-parameter output-preserving additive symmetry action. Under the affine-log oxygen law the two exact null directions form a commuting two-parameter action. The existing quotient coordinates are invariants of those actions.

For stacked experiments, `ker(J_stack) = intersection ker(J_i)`. Principal angles between condition-specific nullspaces, computed after common parameter-box scaling, explain why exact rank restoration can coexist with severe practical ill-conditioning.

Key diagnostic:
- c1+c2 theta_min ≈ **1.69e-4 deg**;
- c1+c2+c3 and all-four theta_min ≈ **0.377286 deg**.

The possibilistic temperature-level test is linked to the same symmetry-breaking geometry: at the 5 K support-touching threshold equal realized temperature levels become admissible and the universal symmetry-breaking angle can collapse to zero.

## Scope boundary

No novelty is claimed for Lie symmetries or principal-angle methods themselves. Their role is explanatory. Locked scientific results from earlier versions remain unchanged.
