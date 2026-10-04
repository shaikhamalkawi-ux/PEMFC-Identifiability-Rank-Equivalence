# Final reproducibility closure

Closure date: 5 October 2026

Associated manuscript:

**Exact Experiment-Conditioned Parameter Redundancy in the Seven-Parameter PEMFC Benchmark**

Repository author: **Ghassan Malkawi**

## Locked reproducibility status

- Exact fixed-temperature xi1/xi2 invariance: PASS.
- Ballard feasible-equivalence reproduction: PASS.
- Full seven-column analytic Jacobian audit: PASS.
- Single-condition 250 W rank 5 result: PASS.
- Same-temperature pressure-diversity rank 6 result: PASS.
- Two-temperature c1+c2 rank 7 result with severe conditioning: PASS.
- All-four-condition conditioning improvement: PASS.
- Automated workflow: PASS on Python 3.10, 3.11, and 3.12.

The manuscript and repository use the same benchmark convention and the same locked numerical targets documented in `RESULTS.md`.

The repository supports the narrow experiment-conditioned rank/nullspace and equivalence-class contribution only. It does not claim novelty for PEMFC identifiability in general, coefficient grouping, or separable regression.
