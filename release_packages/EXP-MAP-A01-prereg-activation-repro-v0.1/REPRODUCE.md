# A01 controlled run and investigator-B reproduction — separate future transactions

This is a **manual procedure** for authorized investigators, NOT a shell script run by CI or the package verifier. Use Charter v0.2, the frozen A01 protocol, current reviewed canonical registry and `controlled_execution/README.md`. Record actual environment and timestamps; never invent missing run artifacts.

## Prerequisites / stop conditions

- Start from a clean checkout of the **same reviewed and activated source revision**, with `data/ecdata` at commit `25cec5ecfec8b9f016eb1631ac633194c2bed39f` and exact `allcurves.00000-09999` SHA-256 `259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968`.
- Confirm current human-approved A01 activation source lineage and that A03 remains prohibited. Confirm hashes of `EXP-MAP-A01.json`, configs, code inputs and source records through the source-package verifier, project registry audit and controlled runner preflight.
- Use a newly provisioned, recorded software environment; archive Python/package versions, OS, container digest if one is in fact used, machine identity policy, exact checkout SHA and the complete stdout/stderr and GitHub CI receipts.
- If preflight fails or source/identity/counts drift: **stop**. Retain diagnostics; do not silently edit parameters, cohort, exclusions, rank scale, graph metric, RNG or execution flag.
- The repository's current state authorizes eligibility only; the user/institution controls actual execution. No real-cohort run is made by this release package PR.

## Investigator A — original registered experiment

```sh
python scripts/verify_exp_map_a01_release_package.py --require-source
python scripts/validate_exp_map_a01_preregistration.py
python scripts/validate_audit_registries.py
star-controlled-experiment preflight --spec controlled_execution/specs/EXP-MAP-A01.json
star-controlled-experiment run --spec controlled_execution/specs/EXP-MAP-A01.json --executor-id investigator-A
```

The runner creates a fresh `controlled_runs/EXP-MAP-A01/<run_id>/` transaction with `manifest.json`, `manifest.sha256`, tracked logs and write-once outputs: `summary.json`, `observed_projection.csv`, `null_statistics.csv`. Store the **actual printed** manifest path; never substitute a guessed run ID. Retain all 999 null values, even for nonrejection (`p>=0.01`), errors, or failed transactions.

## Investigator B — independent environment / new executor

Provision a genuinely independent host/checkout and document what makes it independent. Use the same frozen source, protocol, spec, null and Git revision. Supply the actual investigator A manifest:

```sh
star-controlled-experiment rerun --spec controlled_execution/specs/EXP-MAP-A01.json --original-manifest /ABSOLUTE/PATH/TO/A/manifest.json --executor-id investigator-B --independence-note 'Independent host, clean checkout, separately provisioned environment'
star-controlled-experiment verify-reproduction --original-manifest /ABSOLUTE/PATH/TO/A/manifest.json --rerun-manifest /ABSOLUTE/PATH/TO/B/manifest.json
```

`/ABSOLUTE/PATH/TO/A/manifest.json` and `/ABSOLUTE/PATH/TO/B/manifest.json` are placeholders to replace with paths to **existing** manifests. The runner requires distinct executor identities, compares tracked bindings, output hashes, and records environment differences. Do not alter the run to make mismatches disappear.

## Independent reviewer outcome contract

The reviewer must receive the two complete manifests and SHA-256 sidecars, source/suite commit IDs, environment/version records, provenance and code hashes, exact observed T, all 999 ordered null values, effect and p-value, stdout/stderr, all output hashes, and any mismatches or failed attempts.

Determine reproduction from exact locked transaction and output comparisons, **not** from rough visual agreement. Report rejection, non-rejection, errors and inconclusive outcomes symmetrically. A separate evidence-review PR is required before changing `Controlled_Support_Eligible`; an independently derived physical mechanism and blind astronomical validations are additionally required before any physical support. Never run A03 through this A01 protocol.
