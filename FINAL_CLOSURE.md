# v7 reproducibility closure

Closure date: 6 October 2026

Associated manuscript:

**Experiment-Conditioned Parameter Redundancy in Seven-Parameter PEMFC Models: Exact Equivalence and Rank-Aware Experimental Design**

Repository author: **Ghassan Malkawi**

## v7 closure status

- Complete Ballard Mark V voltage-model replay: PASS.
- Published rounded Ballard THRO SSE reproduction: PASS.
- Exact fixed-temperature voltage/SSE invariance: PASS.
- Fixed-pressure second null direction: PASS.
- Full seven-column analytic Jacobian audit: PASS.
- Independent complex-step derivative check: PASS.
- Single-condition rank 5: PASS.
- Same-temperature pressure-diversity rank 6: PASS.
- c1+c2 local rank 7 with severe conditioning: PASS.
- Deterministic observation-count-matched four-condition 30-observation design: PASS.
- 501-point lambda-grid robustness over published [10,24]: PASS.
- Common parameter-box scaling robustness: PASS.
- Automated Python 3.10-3.12 workflow remains the CI target.

The repository uses the complete Ballard model for the numerical invariance replay. Numerical rank uses the NumPy/LAPACK-style tolerance tau = sigma_1 max(m,n) eps_machine. Parameter-box scaling is J_box = J diag(U_i-L_i).

The scope remains bounded: fixed-temperature finite equivalence is a non-injectivity result; multi-temperature rank 7 is a local numerical-rank result and is not claimed to prove global identifiability. Matching the number of observations does not imply equal experimental cost.
