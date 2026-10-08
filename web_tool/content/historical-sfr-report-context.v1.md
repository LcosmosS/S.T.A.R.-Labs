# Historical SFR report — review context v1

Source: user-supplied `Detailed Report_ Bridging BSD Conjecture and Cosmology.docx`, inspected 2026-10-08. This is a **public review extract**, not a commit of the original document. It is not treated as an independently verified experiment, proof, or evidence for BSD.

## Reported construction (M — candidate model)

The report describes `L_cosmo(s)=Σ_(n≥1) a_n n^(-s)`, where `a_n` is a number of galaxies in bins of stellar mass, redshift and Petrosian radius, indexed by a one-dimensional bin enumeration. This is not the Hasse–Weil L-function of an elliptic curve. The report uses a proposed rank-like interpretation near `s=1`, but a derivative value by itself does not determine an order of vanishing without analyticity and a verified zero at that point.

## Historical metrics (unverified)

The report gives 5-fold test MSE values `0.3904, 0.4312, 0.4420, 0.4322, 0.4371`, reporting mean `0.4266` and dispersion `0.0185`. These are **reported observations**, not controlled results. The dataset is named `Stellar_Mass2_Table_cleaned.csv`; exact input revision, code/seed, feature/target exclusions, split assignments, imputation fitting order and matched null are not bound here. The report also describes fitting 'formula coefficients' with a Random Forest; that does not itself yield fixed linear coefficients. The claimed interpretation of rank as independent physical drivers is conjectural.

## Required before any promotion

- Lock original data identity, download/query SQL, row-level keys, target, preprocessing and join lineage.
- Recompute bin series only from appropriate training data; prevent target leakage and train/test reuse.
- Implement a null prediction and ordinary SFR baseline with a frozen split, independent validation and error estimates.
- Test whether the arithmetic-inspired feature gives incremental out-of-sample value over non-arithmetic controls.
- Preserve original report as historical narrative rather than rewriting it or upgrading the reported metrics.
