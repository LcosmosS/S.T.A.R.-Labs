# Planck chain files

The tracked `base_plikHM_TTTEEE_lowl_lowE*.txt` files are GetDist/CosmoMC
sample-chain tables. They are **not** three-column `z, mu, sigma_mu`
observations.

## Base TTTEEE+lowl+lowE chain

For `base_plikHM_TTTEEE_lowl_lowE_1.txt`:

- size: 9,322,250 bytes;
- rows: 6,125;
- columns per row: 95;
- Git blob SHA-1: `30ea354f7cc359306969fedcc4f3724014c9c953`;
- SHA-256: `f17a149cbb9bdd4095e279419d6bd0146f96dc5755d92e6ca2d9527e6920bc9d`;
- all parsed values are finite in the audited copy.

The first two columns are sample weight and `-log(posterior)`. The accompanying
`base_plikHM_TTTEEE_lowl_lowE.paramnames` contains exactly 93 named parameter
entries, so the 95-column table resolves exactly as 2 structural columns plus
93 scientific/nuisance/derived columns. Examples include `omegabh2`,
`omegach2`, `theta`, `tau`, `H0`, `omegam`, `sigma8`, and the
CMB chi-square diagnostics.

Metadata copied from the supplied
`COM_CosmoParams_base-plikHM-TTTEEE-lowl-lowE_R3.00.zip`:

- `.paramnames`: SHA-256 `e3dbf066f4f026f11bdf11dde4e4d9246c0b5f9f6add914977d8371bee9e395e`;
- `.ranges`: SHA-256 `a90df1afa621c82219e2054977b99e478c2844a04359a2ebdd90b925ed7b8a0a`;
- `.properties.ini`: SHA-256 `7c77e31548960c720d6e384b89688314f826576d0849d945442362422d037892`.

The base properties specify `plik_foregrounds=T` and `burn_removed=T`.

## Post-BAO importance-sampled chain

For `base_plikHM_TTTEEE_lowl_lowE_post_BAO_1.txt`:

- size: 2,188,680 bytes;
- rows: 1,380;
- columns per row: 99;
- Git blob SHA-1: `39167f90cf412940f0dd0dcab975f08e37d58a46`;
- SHA-256: `5c1649c263a67e7b822c7cc7a8ae1a0a24f48346d3ef3069bda527ebad4add3f`;
- all parsed values are finite in the audited copy.

The post-BAO table preserves the base named parameter block and adds the BAO
chi-square diagnostics `chi2_6DF`, `chi2_MGS`, `chi2_DR12BAO`, and
`chi2_BAO`. The schema is validated against
`base_plikHM_TTTEEE_lowl_lowE_post_BAO.ranges` and by the numerical invariant

`chi2_BAO ~= chi2_6DF + chi2_MGS + chi2_DR12BAO`

for every tracked post-BAO row within the text precision.

Post-BAO metadata hashes:

- `.ranges`: SHA-256 `a417732d3bcc35aaf216635a6648914b9397f02b8961fa514587e729686ed0d3`;
- `.properties.ini`: SHA-256 `064fff7d2cf5a5763f2f65ace9d657af6a877ca9edeadd088e8014b0a0a2641e`.

The post-BAO properties also specify `burn_removed=T` and
`plik_foregrounds=T`.

## Loader policy

`src.likelihoods.data.planck_compressed.load_planck_chain` now requires and
parses the metadata next to a chain. The base chain uses the supplied
`.paramnames` directly. The post-BAO chain reuses the base parameter metadata
and validates its four additional BAO chi-square fields against the post-BAO
`.ranges` file.

The old loader interpreted the first three columns as `z, mu, sigma_mu`.
That interpretation is invalid for these files and is rejected explicitly.

The multi-megabyte chains are intentionally not bundled inside the Python
wheel. From an installed package, pass an explicit chain path or set
`STAR_PLANCK_CHAIN_PATH`; the metadata files must accompany the chain. From a
repository checkout, the tracked base chain and metadata are discovered
automatically.

These metadata additions establish column semantics. They do **not** by
themselves change any registry eligibility or promote the Planck artifacts to
controlled or physical evidence.
