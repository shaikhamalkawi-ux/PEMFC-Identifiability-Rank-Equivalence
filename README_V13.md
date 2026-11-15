# Project 53 v13 reproducibility

This package/repository state reproduces the complete unified v13 manuscript results:

1. structural-identifiability theorems and exact fixed-temperature invariance;
2. complete Ballard Mark V replay;
3. multi-condition Jacobian rank and conditioning;
4. possibilistic temperature-level robustness;
5. parameter-symmetry and principal-angle geometry;
6. Fisher / optimal-design / Gram-volume / distance-to-rank-loss diagnostics;
7. local symmetry-breaking order near the equal-temperature boundary;
8. prior/regularization dependence as gauge fixing on an exact likelihood-flat orbit.

Run all checks:

```bash
python scripts/reproduce_v13_all.py
```

Or run separately:

```bash
python scripts/reproduce_v7.py
python scripts/possibilistic_temperature_levels.py
python scripts/symmetry_nullspace_geometry.py
python scripts/information_geometry_oed.py
python scripts/symmetry_breaking_order.py
python scripts/gauge_fixing_prior_dependence.py
```

## Unified result

Two v12 scientific branches are reconciled in v13:

- **symmetry-breaking order:** one pressure condition per temperature level gives quadratic opening of the weakest singular direction, while prior same-temperature pressure diversity changes the opening to linear;
- **gauge fixing:** priors, penalties, bounds, or parameter conventions can select a unique representative along an exact equivalence orbit without creating voltage-likelihood information in that direction.

The sparse nine-point greedy design remains exploratory and is not a v13 manuscript result.

## Claim boundaries

- perturbation power laws are local and benchmark-specific under the declared scaling and pressure law;
- Fisher/confidence interpretations are local and use the stated Gaussian-error assumptions;
- principal angles depend on the common declared parameter metric;
- possibilistic fuzzy sets are stress-test possibility distributions, not empirically calibrated sensor uncertainties;
- gauge fixing does not deny that physically justified external priors may add genuine external information.
