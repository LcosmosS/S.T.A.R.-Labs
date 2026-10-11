# CI-admitted observational sky overlay: v1 contract (ALFALFA display-only proposal in PR #95)

This contract follows merged PRs #68 and #71. The production interface now lists **only CI-admitted releases**. The historical user-entered hash/local-file viewer is removed from the production projection page; the parsing module retains the isolated historical verifier as an archival utility. Display admission is separate from upstream provenance, controlled support and physical support.

## Proposed first release (PR #95, not yet on main)

PR #95 proposes exactly **one** CI-admitted source in
`web_tool/content/sky-overlay-releases.v1.json:sources[0]`:
`DATA-VIZIER-ALFALFA100`, `coordinateRole=hi_centroid`, with 2,000
deterministically selected H I radio centroids. The corrected CDS/VizieR
table2 source, reviewer receipt and derivative CSV are bound by SHA-256.
The recorded review is **display-only** and does not establish any optical
counterpart, crossmatch, inferred property, experiment or physical claim.

Within this open PR's verified preview, the dataset selector is enabled.
The positive browser smoke requires 2,000 exact marker API inputs; the
tampering test requires zero. **Main/deployment admission remains pending**
exact-final-head GitHub checks, accountable off-author GitHub approval and
authorized merge. No historical catalogue becomes admitted merely because
its publisher provenance was verified.

## Release-time rejection contract
The production build runs `npm run sky:check`, backed by `scripts/check-frozen-sky-releases.mjs`. It fails if an operational future source record does not meet all of these conditions:

1. Existing canonical `Dataset_ID` and fully namespace-qualified `REPO-CSV-v0.2:...` identity, exactly one matching dataset row and one matching provenance row. Both registries must say `Provenance_Status=verified`. Never infer that from an arbitrary user SHA or accepted manifest field.
2. Exact publisher and version/release must equal the approved provenance row. Nonempty provider URL, acquisition date, original format, license, selection and integrity record. The canonical provenance integrity record must contain the exact source-file SHA-256.
3. Actual raw file bytes and normalized coordinate bytes must be on disk under narrowly scoped repository paths and must match both **committed SHA-256 values**. Raw Git LFS pointers **cannot** substitute for actual hydrated source bytes. Missing object, corrupted download, wrong file or changed transformation fails the build.
4. Normalized coordinate CSV is exact UTF-8, `source_id,ra_deg,dec_deg`, 1..2,000 rows, up to 1,000,000 bytes, finite decimal ICRS degrees, unique conservative IDs and bounded RA/Dec. The SHA-256 of the exact newline-delimited selected source ID sequence is separately pinned. The pipeline **does not produce** this derived table from unknown raw bytes: a separate reviewed converter and config are required.
5. A distinct, stored review decision with SHA-256 binds dataset ID, raw SHA, derived coordinate SHA and a designated reviewer/reviewed commit, and may approve **display only**. The CI validator checks presence, content and hash **but cannot prove reviewer independence or publication authority**. Branch protection, accountable off-author approvals and independent source audit must verify reviewer identity and original acquisition.
6. A sky-display manifest cannot grant `controlledSupportEligible` or `physicalSupportEligible`. Evidence belongs in claim/experiment registries after original preregistered analysis, independent rerun and review, not in this file.

## Future versioned source record example — INVALID PLACEHOLDER; do not import it
```json
{
  "datasetId": "DATA-EXAMPLE",
  "qualifiedDatasetId": "REPO-CSV-v0.2:DATA-EXAMPLE",
  "provider": "INDEPENDENTLY_VERIFIED_PROVIDER",
  "versionOrRelease": "EXACT_RELEASE",
  "sourceRows": 1,
  "sourcePath": "data/intake/immutable-raw-file",
  "sourceSha256": "REVIEWED_64_HEX_SOURCE_DIGEST",
  "coordinatePath": "web_tool/public/sky/versioned-derived-source.csv",
  "coordinateSha256": "REVIEWED_64_HEX_COORD_DIGEST",
  "selectedIdsSha256": "REVIEWED_64_HEX_SELECTED_IDS_DIGEST",
  "coordinateRole": "optical_counterpart",
  "reviewPath": "docs/independent-reviews/signed-acceptance.json",
  "reviewSha256": "REVIEWED_64_HEX_RECEIPT_DIGEST",
  "controlledSupportEligible": false,
  "physicalSupportEligible": false
}
```

The ID digest is SHA-256 of `source_id` values in coordinate-CSV order, joined with `\n` and followed by a final newline. The raw/derived content digests cover **exact bytes**, not rounded numerical arrays. No retiming, reordering, deduplicating, coordinate role substitutions or rerun-with-different-options is implicit. For ALFALFA, optical counterpart `RAO/DEO` and HI centroid `RAJ2000/DEJ2000` are distinct positional observables; this version must specify role and independent conversion review.

## Runtime selector, build and deployment limits

- `sources` is the sole production display admission list. PR #95 proposes
  one ALFALFA H I-centroid source; a separate `reviewCandidates` or pending
  review fixture must **never** enable the chooser or produce markers.
- The browser fetches only the admitted same-origin CSV, rejects redirects
  and oversized data, checks exact file SHA-256 and the ordered ID digest,
  parses strictly bounded ICRS coordinates, then supplies 2,000 Aladin Lite
  marker inputs. This is **not** a validation of CDS imagery or astronomy
  inference.
- `npm run build` runs `sky:check` first. The gate reads real source bytes,
  reviewed coordinate bytes and receipt in addition to the canonical
  dataset/provenance registry. **An unhydrated Git LFS pointer fails closed.**
- Vercel's root `.vercelignore` allows **only** the required exact ALFALFA
  VOTable path and receipt within `data/` and `docs/`. A Vercel upload must
  supply the already-hydrated **10,981,088-byte** object; the whitelist cannot
  hydrate it. If a Git-backed deployment supplies only the LFS pointer, the
  build must fail and ingestion must be repaired before deployment approval.
- The production wrapper generates a unique temporary public directory
  **per build**, copies only manifest-approved sky files plus non-sky public
  assets, passes it to Vite and removes it afterward. Concurrent builds
  cannot delete each other's staging. A direct production Vite invocation
  without a wrapper-provided staging path fails closed. `build:dev` uses
  checked-in `public/` for local development.
- CI verifies recorded byte integrity, schema and receipt fields, but does
  **not** independently prove a human reviewer's identity or publisher
  signatures. Accountability is an external, required off-author gate.

## Tests and required independent signoffs

- Latest-head CI must run `npm test`, `npm run sky:check`,
  `npm run build`, `npm run typecheck`, the desktop/mobile Aladin spy
  smoke, source/receipt/coordinate tampering regressions and concurrent
  staging tests. The Aladin script spy explicitly returns
  `Access-Control-Allow-Origin: *` because the real component loads the
  external script with `crossOrigin=anonymous`.
- The STARMAP workflow has **unfiltered** `pull_request` and `push`
  triggers; source-byte-only, receipt-only and code changes cannot skip
  the source-integrity job by path filtering.
- Before production admission, independently confirm LFS hydration in the
  actual Vercel deployment context and obtain a final human GitHub
  `APPROVED` review by a reviewer with write access.
- Passing CI or a previously recorded source-review receipt cannot approve
  A01/A03 execution, controlled or physical support, crossmatching or
  arithmetic-cosmology correspondence.
