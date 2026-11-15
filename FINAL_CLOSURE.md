# v13 unified-mechanism reproducibility closure

Closure date: 15 November 2026

Associated manuscript:

**Experiment-Conditioned Parameter Redundancy in Seven-Parameter PEMFC Models: Exact Equivalence and Rank-Aware Experimental Design**

Repository author: **Ghassan Malkawi**

## v13 closure status

- Complete Ballard Mark V voltage-model replay: PASS.
- Published rounded Ballard THRO SSE reproduction: PASS.
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
- Symmetry-breaking-order calculation: PASS.
- Gauge-fixing / prior-dependence calculation: PASS.
- Unified runner `scripts/reproduce_v13_all.py`: PASS.

## Reconciled v12 branches

v13 reconciles two independently developed v12 branches:

1. **Order of symmetry breaking.** With one pressure condition at each temperature level, the weakest box-scaled singular direction opens quadratically in temperature separation. Prior same-temperature pressure diversity removes the pressure-dependent ambiguity and changes the opening to linear.
2. **Gauge fixing.** Priors, penalties, bounds, or parameter conventions may select a unique representative from an exact equivalence orbit, but the fixed-temperature voltage likelihood remains flat along that orbit.

## Unified interpretation

The complete mechanism is:

`exact symmetry -> rank loss -> quotient coordinates -> symmetry breaking -> singular-value opening order -> near-null geometry -> information redistribution -> robust experimental design`,

with prior/regularization acting only as representative-selection rules along likelihood-flat directions.

## Package QA

- Main manuscript: 31 pages.
- Supplementary Material: 19 pages.
- References: 37/37 cited.
- Undefined citations/references: 0.
- Overfull boxes: 0.
- Type 3 fonts: 0.
- Clean-source visual parity: 0/31 changed Main pages and 0/19 changed Supplement pages.
- One non-blocking underfull hbox remains in the Main; rendered visual QA passes.
- Source ZIP integrity: PASS.
- Reproducibility ZIP integrity: PASS.

## Scope boundary

No novelty is claimed for Lie symmetries, principal-angle methods, standard E/D/A criteria, Hadamard's inequality, the Eckart-Young theorem, singular-value perturbation theory, or gauge fixing as general mathematical tools. Their use is explanatory and benchmark-specific. The perturbation laws are local near the equal-temperature boundary. Fuzzy sets are stress-test possibility distributions. A physically justified external prior may contribute external information, but it does not make the voltage likelihood informative along an exact null direction. The sparse nine-point greedy design remains future work and is not a manuscript result.
