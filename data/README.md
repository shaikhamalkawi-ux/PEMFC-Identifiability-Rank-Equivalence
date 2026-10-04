# Data provenance

The arrays in `benchmark_data.py` are the minimal current/voltage vectors and operating conditions needed to reproduce the manuscript's rank and exact-invariance checks.

Primary public source:

- Repository: Yacine-Bouali/Benchmark-Data-for-PEMFC-Parameter-Extraction
- Paper: Y. Bouali, K. Imarazene, B. Alamri, E. M. Berkouk, *Scientific Reports* 16, 4980 (2026)
- DOI: 10.1038/s41598-026-35200-6

## Included here

- Ballard Mark V: 13 published current/voltage points, T = 343 K.
- 250 W stack: four 15-point operating conditions:
  - c1: 3/5 bar, 353.15 K
  - c2: 1/1 bar, 343.15 K
  - c3: 2.5/3 bar, 343.15 K
  - c4: 1.5/1.5 bar, 343.15 K

The repository intentionally does not repackage unrelated benchmark assets. For the complete six-stack source dataset, use the upstream repository and cite the original paper.


## Redistribution note

The upstream repository is publicly accessible, but its current root does not expose a standalone LICENSE file. Provenance and citation are provided here; redistribution terms should be confirmed with the upstream maintainer before any permanent archival redistribution beyond this scholarly reproducibility repository.
