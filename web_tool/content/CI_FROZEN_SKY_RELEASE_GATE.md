# CI-admitted observational sky overlay: v1 contract (runtime selector, no admitted sources)

This contract follows merged PRs #68 and #71. The production interface now lists **only CI-admitted releases**. The historical user-entered hash/local-file viewer is removed from the production projection page; the parsing module retains the isolated historical verifier as an archival utility. Display admission is separate from upstream provenance, controlled support and physical support.

## Current release
`web_tool/content/sky-overlay-releases.v1.json` contains `sources: []`. That is intentional. `DATA-MANGA-HI-ALL` publisher FITS source provenance was independently recorded as `verified` by PR #74; `DATA-SDSS18-200K` remains `unknown`. No reviewed, coordinate-role-locked, hashed sky derivative and independent release review has been admitted for either source. The arithmetic ecdata input has verified arithmetic provenance, but contains no observed sky positions. Therefore **zero astronomical catalogues are released for automatic plotting**.

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

## Runtime selector and limits
- The runtime dataset chooser is bound to `sky-overlay-releases.v1.json` at build time. A source must pass `npm run sky:check` for a production build. No human-entered digest can authorize a dataset. The browser fetches a same-origin static file, rejects redirects/oversized payloads, rechecks its exact SHA-256 and the ordered selected-ID digest, and parses the strict coordinate schema before rendering markers. Empty admission means the selector is disabled and no sky catalog is rendered.
- `DATA-MANGA-HI-ALL` has verified publisher FITS source bytes, but there is **no** independently reviewed coordinate derivative/release. `DATA-SDSS18-200K` and prospective ALFALFA remain unadmitted for display. No original science inference is performed by a release.
- The v1 validator does not recompute source astrophysical row counts from FITS/VOTable or verify publisher signatures/independent reviewer identity. Those require format-specific acquisition checks and human or cryptographic review. `sourceRows` is a reviewed binding, not an automatically proven row count.
- No PR merges, controlled A01 executions, independent reruns, astronomical crossmatch, topology result, SFR score or physical-support promotion.
- Do not mutate audit-pinned v0.1 registries in this stacked PR. Versioned provenance transitions remain separately reviewed and accepted upstream before populating the manifest.

## Tests and next signoffs
- The contract's `*.test.mjs` synthetic tests include runtime byte and ID-chain rejection; production `npm run build` invokes `sky:check`, and the browser smoke test must show a disabled chooser with no markers for the empty release. Run CI and require reviewer approval before merge.
- Require the #68 independent live-CDS/HiPS and privacy/license review before merge, then review this stacked PR.
- Acquire independently pinned original source, verify complete schema, license, row count and precise positional coordinate roles; register accepted source in versioned source and provenance registries; independently review derived converter and display; make a separate PR adding the first **real** release record and a runtime selector that fails closed on mismatched bytes. Claim-level support stays false until independent experiments.
