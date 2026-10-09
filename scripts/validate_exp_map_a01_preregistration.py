"""Validate the EXP-MAP-A01 preregistration without executing the experiment."""

from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path

from src.control.registry import RegistrySnapshot, file_sha256
from src.data.cremona_ecdata import load_allcurves, representative_records
from src.experiments.exp_map_a01 import _require_locked_config


EXPECTED_SUBMODULE = "25cec5ecfec8b9f016eb1631ac633194c2bed39f"
EXPECTED_SOURCE_SHA256 = (
    "259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968"
)
EXPECTED_SOURCE_ROWS = 64687
EXPECTED_REPRESENTATIVES = 38042
EXPECTED_CI_ROWS = 800


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    source = root / "data/ecdata/allcurves/allcurves.00000-09999"
    config_path = root / "preregistrations/EXP-MAP-A01/config.json"
    spec_path = root / "controlled_execution/specs/EXP-MAP-A01.json"
    ci_subset = root / "data/raw/ci_subset.csv"

    gitlink = _git(root, "ls-tree", "HEAD", "data/ecdata").split()
    if len(gitlink) < 3 or gitlink[2] != EXPECTED_SUBMODULE:
        raise SystemExit(
            f"unexpected data/ecdata gitlink: expected {EXPECTED_SUBMODULE}, got {gitlink}"
        )
    actual_source_hash = file_sha256(source)
    if actual_source_hash != EXPECTED_SOURCE_SHA256:
        raise SystemExit(
            f"allcurves SHA256 mismatch: {actual_source_hash}"
        )

    records = load_allcurves(source)
    representatives = representative_records(records)
    if len(records) != EXPECTED_SOURCE_ROWS:
        raise SystemExit(
            f"allcurves row mismatch: expected {EXPECTED_SOURCE_ROWS}, got {len(records)}"
        )
    if len(representatives) != EXPECTED_REPRESENTATIVES:
        raise SystemExit(
            "representative row mismatch: "
            f"expected {EXPECTED_REPRESENTATIVES}, got {len(representatives)}"
        )
    if min(record.conductor for record in records) != 11:
        raise SystemExit("unexpected minimum conductor")
    if max(record.conductor for record in records) != 9999:
        raise SystemExit("unexpected maximum conductor")

    config = json.loads(config_path.read_text(encoding="utf-8"))
    _require_locked_config(config)

    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    if spec["config"] != config:
        raise SystemExit("execution spec inline config differs from locked config")
    if spec["dataset_inputs"] != [
        {
            "path": "data/ecdata/allcurves/allcurves.00000-09999",
            "sha256": EXPECTED_SOURCE_SHA256,
        }
    ]:
        raise SystemExit("execution spec dataset input is not the locked ecdata source")
    if spec["rng_seeds"] != {"rank_permutation": 1729}:
        raise SystemExit("execution spec RNG seed drift")

    snapshot = RegistrySnapshot.load(root)
    resolved = snapshot.resolve("EXP-MAP-A01")
    # This validator was originally preregistration-only. A later, explicit
    # activation PR may change precisely the two execution-eligibility flags.
    # Accept no partial activation and no unbound or post-hoc scientific edits.
    execution_flags = (
        resolved.experiment["Controlled_Execution_Eligible"].lower(),
        resolved.dataset["Controlled_Execution_Eligible"].lower(),
    )
    if execution_flags != ("true", "true"):
        raise SystemExit(
            "A01 activation must set both experiment and dataset execution "
            f"eligible with the reviewed transition: got {execution_flags!r}"
        )
    expected_activation_bindings = {
        "experiment": "97dac41c4d8a866d0abbcdf5515829328e92ea1fb3cf7b4d03e1d9b9c0b9c868",
        "dataset": "1b81e05ab90ce822c7dcbda88bdb206f191f6523fac03fea5ecdf55724de44c2",
    }
    for record_name, expected_sha in expected_activation_bindings.items():
        if resolved.record_hashes[record_name] != expected_sha:
            raise SystemExit(
                f"A01 {record_name} activation changed beyond reviewed two-bit transition"
            )
    if resolved.experiment["Controlled_Support_Eligible"].lower() != "false":
        raise SystemExit("preregistration PR must not enable controlled support")
    if resolved.experiment["Physical_Support_Eligible"].lower() != "false":
        raise SystemExit("preregistration PR must not enable physical support")
    if resolved.provenance["Provenance_Status"] != "verified":
        raise SystemExit("DATA-ARITHMETIC provenance must be verified")
    if resolved.provenance["Evidence_Status"] != "controlled":
        raise SystemExit("DATA-ARITHMETIC evidence status must be controlled")
    if resolved.parameter["Preregistration_Status"] != "locked":
        raise SystemExit("PAR-MAP-001 must be locked")
    if resolved.null["Preregistration_Status"] != "locked":
        raise SystemExit("NULL-MAP-001 must be locked")
    if spec["registry_bindings"] != resolved.record_hashes:
        raise SystemExit("execution spec registry bindings drifted from preregistration")

    for entry in spec["code_inputs"] + spec["config_files"]:
        path = root / entry["path"]
        if file_sha256(path) != entry["sha256"]:
            raise SystemExit(f"bound file hash mismatch: {entry['path']}")

    expected_labels = [record.label for record in representatives[:EXPECTED_CI_ROWS]]
    with ci_subset.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["label"]:
            raise SystemExit("ci_subset.csv must contain exactly one CSV column: label")
        actual_labels = [row["label"] for row in reader]
    if actual_labels != expected_labels:
        raise SystemExit(
            "ci_subset.csv is not the first 800 number-1 representatives "
            "from the pinned allcurves source"
        )

    print("EXP-MAP-A01 preregistration and reviewed activation validation passed")
    print(f"ecdata_commit={EXPECTED_SUBMODULE}")
    print(f"source_sha256={EXPECTED_SOURCE_SHA256}")
    print(f"source_rows={len(records)}")
    print(f"representative_rows={len(representatives)}")
    print("controlled_execution_eligible=true; controlled_support=false; physical_support=false")
    print("no experiment was executed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
