# Planck chain files

The tracked `base_plikHM_TTTEEE_lowl_lowE_*.txt` files are sample-chain
tables in the GetDist/CosmoMC family of text formats. They are **not**
three-column `z, mu, sigma_mu` observations.

For the tracked `base_plikHM_TTTEEE_lowl_lowE_1.txt` object currently in this
repository:

- size: 9,322,250 bytes;
- rows: 6,125;
- columns per row: 95;
- Git blob SHA-1: `30ea354f7cc359306969fedcc4f3724014c9c953`;
- SHA-256: `f17a149cbb9bdd4095e279419d6bd0146f96dc5755d92e6ca2d9527e6920bc9d`;
- all parsed values are finite in the audited copy.

The chain convention uses the first column for sample weight and the second for
`-log(posterior)`. The remaining 93 columns are kept as positional
`param_001` ... `param_093` values by
`src.likelihoods.data.planck_compressed.load_planck_chain`.

The repository does not currently contain the matching `.paramnames` metadata.
Accordingly, the loader does not assign scientific parameter names to those 93
columns. A controlled use of these chains must provenance-lock the corresponding
parameter metadata before interpreting individual positional columns.

The old loader treated the first three columns as `z, mu, sigma_mu`. That
interpretation is invalid for these files and is now rejected explicitly.

The chain is intentionally not bundled inside the Python wheel. From an
installed package, pass an explicit path to `load_planck_chain` or set
`STAR_PLANCK_CHAIN_PATH`. From a repository checkout, the tracked
`data/planck/base_plikHM_TTTEEE_lowl_lowE_1.txt` path is discovered
automatically.
