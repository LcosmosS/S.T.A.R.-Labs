# Precise citation and attribution instructions

## Match the citation to the material used

The four original DOI identifiers below were **recorded in the audited repository**.
The collaboration-invitation DOI `10.5281/zenodo.23447557` was supplied after
that dated audit, and has been added as a separately identified archive link.
Resolver access was unavailable; publisher metadata, deposited bytes, authorship
and version relationships for these records have **not been independently
verified in this documentation update**. Before external publication, check the deposit directly and
use its exact title, authors, date and version. If a record cannot be accessed,
report that limitation and cite the inspected Git revision instead of inventing
metadata. Do not infer publication or peer review from a badge.

| Use | Repository-recorded identifier / target | Required scope statement |
| --- | --- | --- |
| Repository software | [CITATION.cff](../../CITATION.cff), repository URL and exact code commit | Software/proposed research framework; identify modules used and validation limits |
| A01 preregistration and activation design | [10.5281/zenodo.23292229](https://doi.org/10.5281/zenodo.23292229), [package](../EXP-MAP-A01-prereg-activation-repro-v0.1/README.md) | Earlier design/activation archive; not the primary run |
| A01 saved primary execution | [10.5281/zenodo.23409249](https://doi.org/10.5281/zenodo.23409249), [package](../EXP-MAP-A01-primary-execution-v0.1/README.md) | Primary arithmetic-null evidence; independent replication and physical support not established |
| A03 pre-execution verification | [10.5281/zenodo.23288785](https://doi.org/10.5281/zenodo.23288785), [lineage](../../docs/registries/EXP_MAP_A03_PREEXECUTION_RELEASE_LINEAGE_v0.1.md) | Author-produced reference verification, not A03 inference or activation |
| M1-INH-E1b certificate/pre-review package | [10.5281/zenodo.23260882](https://doi.org/10.5281/zenodo.23260882), [package](../M1-INH-E1b-pre-review-v0.1/README.md) | Candidate class-relative mathematical result; independent proof review remains separate |
| This invitation | [10.5281/zenodo.23447557](https://doi.org/10.5281/zenodo.23447557), [`release_packages/STAR-collaboration-invitation-v0.1/`](README.md) at its actual reviewed commit | Bounded collaboration/audit materials; Zenodo metadata/deposit bytes require independent verification; not a scientific result or assertion of a GitHub release tag |
| Frozen historical material | Original author/title/version and exact preserved path/hash, plus source/audit lineage | Historical, exploratory, quarantined or pending-review status as recorded; not silently promoted |
| Catalogs, methods and third-party figures | Original publisher/data release, primary methods paper, version/access date, source URL, actual data hash and required acknowledgments | Repository citation is additional attribution, not a substitute for the primary source |

For ecdata, record JohnCremona/ecdata, commit
`25cec5ecfec8b9f016eb1631ac633194c2bed39f`, file `allcurves/allcurves.00000-09999`
and its SHA-256 `259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968`
when that is the actual input. For observational catalogs, consult the publisher
references and version/selection fields in `registry/data_provenance_registry_v0.1.csv`,
intake request/response records and the relevant survey documentation. Independently
check their attribution and reuse terms. A recorded URL/hash is not proof that
an independent download was performed.

## Software citation example for the audited baseline

```bibtex
@software{mcnamara_star_audited_20261018,
  author  = {McNamara, Patrick J.},
  title   = {S.T.A.R. Labs Research: A Symbolic--Topological--Arithmetic--Relativity Program},
  year    = {2026},
  url     = {https://github.com/LcosmosS/S.T.A.R.-Labs/tree/d69868e3c1d9ae70944deb239369e53a9ecc1e5b},
  version = {d69868e3c1d9ae70944deb239369e53a9ecc1e5b},
  urldate = {2026-10-18},
  note    = {Audited source baseline; software citation does not establish scientific support}
}
```

Use this example only when that is the revision actually used. For subsequent
software or the new invitation itself, replace the revision and access date
with the actual inspected commit/date and describe the material used. Do not
call the baseline commit the invitation's release/deployment commit. A feature
branch, review head, squash merge, deposited archive and executed source can
all have different identities; record each applicable identity explicitly.
Do not add a generic `doi=TBD` or assign one archive's DOI to another artifact.

## Result and review citations

A result citation must also identify its qualified experiment/claim IDs, frozen
protocol, source revision, dataset/version/hash, parameter and null IDs,
transaction ID, complete output manifest and any correction record. Cite a new
independent reproduction through its own receipt/manifest; the primary DOI does
not document a later rerun. An independent reviewer should be credited only for
the work and attestation they actually supplied.

Preserve exact result scope: A01's saved `p=0.001` is the corrected one-sided
value for one arithmetic rank-permutation endpoint with 999 realizations.
It does not establish cosmological correspondence, distinguish ACSC from other
arithmetic structure, prove BSD, validate SFR or establish physical support.
A03 reference tests, M1 symbolic certificates, screenshots, DOI deposition,
GitHub merges and green software CI have their own narrower meanings.

The STARMAP banner/social card are generated communication graphics. If reused,
cite their [image lineage](../../web_tool/artifacts/exp-map-a01-primary-evidence-images.md),
exact file/hash and the underlying primary archive, retaining all caveats.
Do not caption them as experimental plots, observed sky data or app screenshots.
The display-only ALFALFA subset must retain H I-centroid identity and selection
limitations; it is not authorization to perform associations or inference.

## Credit and rights

Use the [MIT license](../../LICENSE) for repository software as applicable, and
retain its copyright notice. Verify third-party catalogs, manuscripts, recovered
code, artwork and assets under their own source terms before redistribution.
ORCID and authorship metadata in CITATION.cff come from the repository; this
audit does not authenticate identity or consent on behalf of contributors.
Agree acknowledgments/authorship based on actual contributions, disclose agent
assistance and conflicts as appropriate, and do not imply institutional
partnership, independent review, endorsement or guaranteed publication.
