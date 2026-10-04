# Quarantine: rtch_e1_synthetic

Date: 2026-10-03.

Status: **QUARANTINED – not eligible for controlled empirical claims until rebuilt**.

Findings: E-LCL-007, E-LCL-008, E-LCL-009, E-LCL-010, E-LCL-011.

Original scientific files are preserved. Repository copies retain canonical Git blob bytes at the intake commit. External SDSS/HI copies retain the exact audited bytes. Checkout hashes and line ending transformations are recorded separately; a checkout CRLF transformation does not indicate research artifact corruption. No research source was executed, no independent replication was performed, and no controlled or physical support was promoted.

The outer_900 and nested_350 folders preserve separate synthetic generations. The 900-point result has topology-null p-values of 1.0; constant pc2/pc3 scalars have undefined correlations and invalid apparent permutation significance. The 350-point run has only 2 nulls, so its minimum attainable plus-one p-value is 1/3 at declared alpha 0.01. Its two stability rows repeat the full data. These outputs remain simulation and negative/null diagnostic evidence, with no demonstrated canonical protocol completion or physical support.

The nested historical manifest records input RTCH_E1/data/demo_torus.csv without a saved working directory. From repository root, that path identifies the 900-row file; the 350-row input is RTCH_E1/RTCH_E1/data/demo_torus.csv. The generation-specific audit input hashes match the retained inputs. Neither manifest records the executed code hash/revision, so current source has not been retrospectively assigned to either historical execution.

The table gives canonical source/copy SHA256 and the prior audit SHA256. Complete original source paths, Git commit/blob IDs, checkout hashes, file sizes, eligibility, and reasons remain in manifest.json and manifest.csv. “Observed new SHA256” means no prior digest was present in the imported audit; no historical hash was fabricated.

| Retained file | Prior audit SHA256 | Canonical source and copy SHA256 | Verification |
|---|---|---|---|
| outer_900/data/demo_torus.csv | `2790c3bdebb665ffa9a5df3ec6b8093dc678c743303b56732be751678bdcfce7` | `2790c3bdebb665ffa9a5df3ec6b8093dc678c743303b56732be751678bdcfce7` | Exact prior hash match |
| outer_900/results/figures/geodesic_projection.png | `Not previously hashed` | `02442569be3683db2f12f16123c561e6fa2df3d015c1060d661b27eb5616d229` | Observed new SHA256; copy verified |
| outer_900/results/figures/persistence_H0.png | `Not previously hashed` | `4186bae4043643a8009e625840b85b4b1545b8d97c5aee19dfae98884fff9b5e` | Observed new SHA256; copy verified |
| outer_900/results/figures/scalar_embedding.png | `Not previously hashed` | `6f54fa3a466626c1bc19852365b9516426df4f2c6da5b2f3fec8503d4017e579` | Observed new SHA256; copy verified |
| outer_900/results/geodesics.csv | `a5f38a93d272e25c5ac384c69e1583797b10d11e1c2ecd61c22c703a8f2d3830` | `a5f38a93d272e25c5ac384c69e1583797b10d11e1c2ecd61c22c703a8f2d3830` | Exact prior hash match |
| outer_900/results/null_persistence.csv | `8b08621f928530576b22d197d831f72c34dfe35d3d49411b74718cca778a0772` | `8b08621f928530576b22d197d831f72c34dfe35d3d49411b74718cca778a0772` | Exact prior hash match |
| outer_900/results/prediction_tests.csv | `6a2c0490e6d8e82a554037067719f620ffd3210f12c2da356d53fc70a53e06fb` | `6a2c0490e6d8e82a554037067719f620ffd3210f12c2da356d53fc70a53e06fb` | Exact prior hash match |
| outer_900/results/rank_label_nulls.csv | `d8b357e6a10b52279605f26a5b6f233f2eb2e954edc9f6d744185523fbf3ad32` | `d8b357e6a10b52279605f26a5b6f233f2eb2e954edc9f6d744185523fbf3ad32` | Exact prior hash match |
| outer_900/results/result.json | `09136ef0b8d380f09f49f968d9f749673a2470bb8557353e4d31566dddf94460` | `09136ef0b8d380f09f49f968d9f749673a2470bb8557353e4d31566dddf94460` | Exact prior hash match |
| outer_900/results/run_manifest.json | `331fc7e3c749ff1f0c12632e1d77ba73096ffe6f55e6e40bc3a0e5fe10978925` | `331fc7e3c749ff1f0c12632e1d77ba73096ffe6f55e6e40bc3a0e5fe10978925` | Exact prior hash match |
| outer_900/results/scalar_embeddings.csv | `2fa37333da3cf2b876ace8db20561f2695a807cbaf952a3785956f97d3142887` | `2fa37333da3cf2b876ace8db20561f2695a807cbaf952a3785956f97d3142887` | Exact prior hash match |
| outer_900/results/stability_summary.csv | `2a4ba4073400126cad152411a675a207ecbae95f6465bec1f4b6a1b8500215f8` | `2a4ba4073400126cad152411a675a207ecbae95f6465bec1f4b6a1b8500215f8` | Exact prior hash match |
| outer_900/results/topology_summary.csv | `e2f3f17041d54bba9276791ab9f552bf130e85896c943fd101e194d015ba4c43` | `e2f3f17041d54bba9276791ab9f552bf130e85896c943fd101e194d015ba4c43` | Exact prior hash match |
| nested_350/data/demo_torus.csv | `ce3e2d8dd919c83362de1fcbe099f8074abe8a693d1dc2664da6956240021e69` | `ce3e2d8dd919c83362de1fcbe099f8074abe8a693d1dc2664da6956240021e69` | Exact prior hash match |
| nested_350/results/figures/geodesic_projection.png | `Not previously hashed` | `2002abc025045f8650da99a6e6fffacc7577c34d1df832c0f6ba54f28f9ac156` | Observed new SHA256; copy verified |
| nested_350/results/figures/persistence_H0.png | `Not previously hashed` | `ee46bcd2b4eb98744f6c9e6dac1e524086758a83e1b7f53de4b30211c7d5de27` | Observed new SHA256; copy verified |
| nested_350/results/figures/persistence_H1.png | `Not previously hashed` | `1419aa7ee51e8b5d3b149951226fbce27d4de2d743bd1d508a7ec42ffaeb8752` | Observed new SHA256; copy verified |
| nested_350/results/figures/persistence_H2.png | `Not previously hashed` | `ebaaa78ead859198d5cad0f5b5e88674e7927cee148aba5e5446ae0105a7bfea` | Observed new SHA256; copy verified |
| nested_350/results/figures/scalar_embedding.png | `Not previously hashed` | `85b12971260e04aa7b2df814f2a9de4ecf5dedf667e8426a2c711db6edf9120b` | Observed new SHA256; copy verified |
| nested_350/results/geodesics.csv | `702d2310f7fe314e9811235ccc2e4c55eb118c44f080a212416e100306b8b6f5` | `702d2310f7fe314e9811235ccc2e4c55eb118c44f080a212416e100306b8b6f5` | Exact prior hash match |
| nested_350/results/null_persistence.csv | `2681b3e39e80847fda2005432b1024c7ec898f43127468643b16e185c03c45b4` | `2681b3e39e80847fda2005432b1024c7ec898f43127468643b16e185c03c45b4` | Exact prior hash match |
| nested_350/results/prediction_tests.csv | `30b91aed6a6a687b2fe73cdebed209552e6f41f1af1127e1110e9bc7ca26f3e6` | `30b91aed6a6a687b2fe73cdebed209552e6f41f1af1127e1110e9bc7ca26f3e6` | Exact prior hash match |
| nested_350/results/rank_label_nulls.csv | `c356fe7106d9806f4dd0cad4193f60901e7b19a48aba1c8afd8761c1b6760fdd` | `c356fe7106d9806f4dd0cad4193f60901e7b19a48aba1c8afd8761c1b6760fdd` | Exact prior hash match |
| nested_350/results/result.json | `d294a3426d69f565d33b07b641768479d04bc12b586cb2b2f17e9f9d9b64cef4` | `d294a3426d69f565d33b07b641768479d04bc12b586cb2b2f17e9f9d9b64cef4` | Exact prior hash match |
| nested_350/results/run_manifest.json | `bd3c605cdcf76c7ba0d348b3266024165c9133e19f4b3b81fb82d81a8b2a5901` | `bd3c605cdcf76c7ba0d348b3266024165c9133e19f4b3b81fb82d81a8b2a5901` | Exact prior hash match |
| nested_350/results/scalar_embeddings.csv | `faf680af972780341116a6e14ecbe3acffa6b73f294e8fb11884c4c2a8437b42` | `faf680af972780341116a6e14ecbe3acffa6b73f294e8fb11884c4c2a8437b42` | Exact prior hash match |
| nested_350/results/stability_summary.csv | `4af317de92879957316bd3bbeb4cd4c1755b4b4adf15f437aa2ae37e2d0fb265` | `4af317de92879957316bd3bbeb4cd4c1755b4b4adf15f437aa2ae37e2d0fb265` | Exact prior hash match |
| nested_350/results/topology_summary.csv | `553574c8c7e3508ee6f1316973388449509ff87934a9c71c3269bf9726d49f95` | `553574c8c7e3508ee6f1316973388449509ff87934a9c71c3269bf9726d49f95` | Exact prior hash match |

All required sources for this quarantine group were available; no required copy source is missing.
