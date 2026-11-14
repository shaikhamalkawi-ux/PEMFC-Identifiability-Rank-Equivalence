# v11 reproducibility closure

Closure date: 14 November 2026

Associated manuscript:

**Experiment-Conditioned Parameter Redundancy in Seven-Parameter PEMFC Models: Exact Equivalence and Rank-Aware Experimental Design**

Repository author: **Ghassan Malkawi**

## v11 closure status

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
- Fisher / optimal-design information calculations: PASS.
- Gram determinant / sensitivity-volume calculation: PASS.
- Eckart-Young distance-to-rank-loss calculation: PASS.

## Unified interpretation

The exact fixed-temperature transformation is written as a one-parameter output-preserving additive symmetry action. Under the affine-log oxygen law the two exact null directions form a commuting two-parameter action. The existing quotient coordinates are invariants of those actions.

For stacked experiments, `ker(J_stack) = intersection ker(J_i)`. Principal angles between condition-specific nullspaces, computed after common parameter-box scaling, explain why exact rank restoration can coexist with severe practical ill-conditioning.

The v11 information layer quantifies the same mechanism. At the same 30-observation count, the matched four-condition design raises total box-scaled sensitivity by only about **6.8%**, but raises the weakest information eigenvalue by **4.3964e9** and the normalized spectral distance to rank deficiency by **4.38325e5**. Thus its advantage is principally redistribution of information into previously weak directions rather than simple data-volume growth.

The possibilistic temperature-level test remains linked to the same symmetry-breaking geometry: at the 5 K support-touching threshold equal realized temperature levels become admissible and the universal symmetry-breaking angle can collapse to zero.

## Scope boundary

No novelty is claimed for Lie symmetries, principal-angle methods, standard E/D/A optimal-design criteria, Hadamard's inequality, or the Eckart-Young theorem themselves. Their role is explanatory. Fisher/confidence-region interpretations are local and require the stated error assumptions. The matched 30-point design is a deterministic observation-count-matched comparison, not a globally optimized design. Locked scientific results from earlier versions remain unchanged.
