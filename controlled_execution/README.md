# Controlled-experiment execution transaction

This directory defines the software transaction that sits between scientific
preregistration and a controlled S.T.A.R. execution.

The runner does **not** decide whether an experiment should be scientifically
promoted. It refuses to execute until the registries and an execution spec
already encode that decision.

## Lifecycle

The intended order is:

1. build and verify the controlled-execution transaction;
2. lock dataset provenance;
3. preregister/lock the parameter set and null model;
4. commit an execution spec that binds the exact registry records, data, code,
   command, configuration, seeds, expected outputs, and optional container
   image digest;
5. set `Controlled_Execution_Eligible=true` only after all readiness gates are
   genuinely satisfied;
6. run the experiment and retain its content-addressed manifest;
7. perform a separate rerun of the exact manifest and compare output hashes;
8. review the primary and rerun manifests before considering
   `Controlled_Support_Eligible=true`;
9. treat physical-support promotion as a separate scientific decision.

The runner never edits any registry and never promotes controlled or physical
support automatically.

## CLI

After installing the package:

```bash
star-controlled-experiment preflight \
  --spec controlled_execution/specs/EXP-EXAMPLE.json

star-controlled-experiment run \
  --spec controlled_execution/specs/EXP-EXAMPLE.json \
  --executor-id investigator-A

star-controlled-experiment rerun \
  --spec controlled_execution/specs/EXP-EXAMPLE.json \
  --original-manifest controlled_runs/EXP-EXAMPLE/<run>/manifest.json \
  --executor-id investigator-B \
  --independence-note "Fresh checkout on independent host"

star-controlled-experiment verify-reproduction \
  --original-manifest controlled_runs/EXP-EXAMPLE/<run>/manifest.json \
  --rerun-manifest controlled_runs/EXP-EXAMPLE/<rerun>/manifest.json
```

Generated run directories are ignored by Git. The manifest and its SHA-256
sidecar are write-once outputs. All experiment-created files under the run
directory are hashed and recorded.

## Fail-closed preflight

A run is rejected unless all of the following are true:

- `Experiment_ID` resolves uniquely;
- experiment mode is `controlled`;
- each explicitly bound `Claim_ID` is registered in `claim_evidence_v0.2.csv`
  and its exact `(Claim_ID, Experiment_ID)` pair is registered in
  `claim_experiment_crosswalk_v0.2.csv`;
- experiment and dataset are controlled-execution eligible;
- provenance is `verified`;
- provenance evidence status is `controlled` or `derived`;
- provenance contains explicit SHA-256 integrity evidence;
- parameter and null records are `preregistered` or `locked`;
- the execution spec binds the exact SHA-256 of all five resolved registry
  records;
- every dataset input hash is present in the provenance integrity record;
- every declared code/config file hash matches;
- code/config inputs are Git-tracked;
- the repository working tree is clean;
- any declared container image digest matches
  `STAR_CONTAINER_IMAGE_DIGEST`.

This is intentionally stricter than the registry readiness checker because an
execution transaction must bind concrete bytes, not only statuses.


### Non-authorizing binding-only preflight

A preregistration PR may prove that an execution-spec skeleton binds the exact
registry records, dataset bytes, tracked code, configuration, seed, and expected
outputs **without opening the execution gate**:

```bash
star-controlled-experiment preflight \
  --spec controlled_execution/specs/EXP-MAP-A03.json \
  --binding-only
```

Binding-only mode is intentionally the inverse of activation: it requires both
the experiment and dataset `Controlled_Execution_Eligible` flags to remain
`false`. It performs the same registry, provenance, row-binding, data-hash,
code-hash, config-hash, Git-state, and container checks as preflight, but it
cannot authorize or execute a command. The `run` and `rerun` paths never use
binding-only mode and continue to require normal execution eligibility.

## Execution spec

Specs conform to [`spec.schema.json`](spec.schema.json).

The command is an argument array and is executed without a shell. Three literal
tokens may appear in command arguments:

- `{run_dir}`
- `{repo_root}`
- `{experiment_id}`

The runner also exports:

- `STAR_RUN_DIR`
- `STAR_REPO_ROOT`
- `STAR_EXPERIMENT_ID`
- `STAR_EXECUTION_CONFIG`
- `STAR_RNG_SEEDS_JSON`
- `STAR_RNG_<NAME>` for each declared seed.

Commands are expected to place controlled outputs under `STAR_RUN_DIR`.
Every file there, other than runner-owned logs/config/manifest files, is hashed
into the manifest. Missing expected outputs fail the transaction.

EXP-MAP-A01 rejects any existing declared result path and creates its result
files exclusively. Reusing a manual output directory cannot overwrite an old
projection, null distribution, or summary. Runner-owned configuration and logs
may already be present in the output directory.
If another writer creates a result during reservation, the attempt fails before
writing result data. Empty reservations may remain as failed-attempt artifacts;
use a fresh directory for the next attempt. The writer never deletes result paths.

## Manifest

A successful or failed post-preflight execution writes `manifest.json` and
`manifest.sha256`. The manifest contains at least:

- Experiment_ID, Dataset_ID, Parameter_Set_ID, Null_ID;
- complete resolved registry records and their SHA-256 bindings;
- registry-file SHA-256 values;
- Git SHA and branch;
- source dataset SHA-256 and byte size;
- exact parameter and null definitions;
- exact command template and resolved command;
- inline config and tracked config-file hashes;
- RNG seeds;
- tracked code-input hashes;
- Python implementation/version/executable;
- platform identity and installed package versions;
- environment identity digest;
- container image digest when one is registered;
- start/end timestamps and duration;
- stdout/stderr hashes;
- all output hashes and sizes;
- experiment and runner exit status.

A rerun additionally records the original manifest SHA-256, the complete
execution-binding hash, output-hash comparison, exit-status comparison,
environment comparison, executor comparison, and the supplied independence
note. Verification requires a different declared executor identity. Environment
equality is recorded but deliberately not required: a separately provisioned
environment may reproduce the same locked Git/spec/data transaction, and that
difference must remain visible in the manifest.

After the command exits, the runner rechecks Git state plus every registry,
execution-spec, dataset, code, and config hash. Any mutation during execution
fails the transaction even when the experiment command itself returned zero.
The registry snapshot includes the canonical claim and crosswalk files in these
manifest hashes and post-run checks.

Passing `verify-reproduction` is necessary transaction-reproduction evidence.
It is not, by itself, proof of scientific validity or authorization to promote
a claim.
