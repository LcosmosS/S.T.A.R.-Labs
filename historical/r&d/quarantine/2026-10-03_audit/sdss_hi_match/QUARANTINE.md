# Quarantine: sdss_hi_match

Date: 2026-10-03.

Status: **QUARANTINED – not eligible for controlled empirical claims until rebuilt**.

Findings: E-LCL-001.

Original scientific files are preserved. Repository copies retain canonical Git blob bytes at the intake commit. External SDSS/HI copies retain the exact audited bytes. Checkout hashes and line ending transformations are recorded separately; a checkout CRLF transformation does not indicate research artifact corruption. No research source was executed, no independent replication was performed, and no controlled or physical support was promoted.

Both files contain 1,495 rows associated with one MANGAID, 1-48157. Every recomputed spherical separation exceeds the claimed 2 arcsec tolerance. The with_arcsec revision stores inf in every separation row. These files are negative data-quality evidence. This finding restricts these artifacts; it does not falsify the general possibility of cross-survey matching.

The imported independent diagnostic is historical/r&d/docs/provenance_audit/local_match_checks.json. Each external source passed its exact prior audit SHA256 requirement before copying.

The table gives canonical source/copy SHA256 and the prior audit SHA256. Complete original source paths, Git commit/blob IDs, checkout hashes, file sizes, eligibility, and reasons remain in manifest.json and manifest.csv. “Observed new SHA256” means no prior digest was present in the imported audit; no historical hash was fabricated.

| Retained file | Prior audit SHA256 | Canonical source and copy SHA256 | Verification |
|---|---|---|---|
| merged_sdss_hi.csv | `5a9606b75bc55de5e7833a04e5c56318df9f21a31560df180db2707374a22d50` | `5a9606b75bc55de5e7833a04e5c56318df9f21a31560df180db2707374a22d50` | Exact prior hash match |
| merged_sdss_hi_with_arcsec.csv | `e6e2e749d0ec45b5713311dfe3b3cc958fddb13166f770ce2c47a30dbd5f8dad` | `e6e2e749d0ec45b5713311dfe3b3cc958fddb13166f770ce2c47a30dbd5f8dad` | Exact prior hash match |

All required sources for this quarantine group were available; no required copy source is missing.
