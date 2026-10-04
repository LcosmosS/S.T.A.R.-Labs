"""Validate claims of controlled-experiment execution readiness.

A software-green repository may legitimately contain zero execution-ready
experiments. This script fails only when a registry claims readiness without
the required provenance and preregistration gates.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ALLOWED_READY_EVIDENCE_STATUSES = {"controlled", "derived"}


def _rows(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def _truth(value):
    return str(value).strip().lower() == "true"


def assess(root: Path):
    registry = root / "registry"
    experiments = _rows(registry / "experiment_registry_v0.2.csv")
    datasets = {
        row["Dataset_ID"]: row for row in _rows(registry / "dataset_registry_v0.1.csv")
    }
    provenance = {
        row["Dataset_ID"]: row
        for row in _rows(registry / "data_provenance_registry_v0.1.csv")
    }
    parameters = {
        row["Parameter_Set_ID"]: row
        for row in _rows(registry / "parameter_registry_v0.1.csv")
    }
    nulls = {
        row["Null_ID"]: row for row in _rows(registry / "null_registry_v0.1.csv")
    }

    claimed = []
    failures = []
    for exp in experiments:
        if not _truth(exp.get("Controlled_Execution_Eligible", "false")):
            continue
        claimed.append(exp["Experiment_ID"])

        dataset = datasets.get(exp["Dataset_ID"])
        prov = provenance.get(exp["Dataset_ID"])
        parameter = parameters.get(exp["Parameter_Set_ID"])
        null = nulls.get(exp["Null_ID"])
        missing = [
            name
            for name, value in (
                ("dataset", dataset),
                ("provenance", prov),
                ("parameter set", parameter),
                ("null model", null),
            )
            if value is None
        ]
        if missing:
            failures.append(
                f"{exp['Experiment_ID']}: missing {', '.join(missing)}"
            )
            continue

        if not _truth(dataset.get("Controlled_Execution_Eligible", "false")):
            failures.append(
                f"{exp['Experiment_ID']}: dataset is not controlled-execution eligible"
            )
        if prov.get("Provenance_Status") != "verified":
            failures.append(
                f"{exp['Experiment_ID']}: provenance is not verified"
            )

        evidence_status = prov.get("Evidence_Status")
        if evidence_status not in ALLOWED_READY_EVIDENCE_STATUSES:
            failures.append(
                f"{exp['Experiment_ID']}: provenance evidence status "
                f"{evidence_status!r} is not accepted for controlled execution"
            )

        if parameter.get("Preregistration_Status") not in {"preregistered", "locked"}:
            failures.append(
                f"{exp['Experiment_ID']}: parameter set is not preregistered"
            )
        if null.get("Preregistration_Status") not in {"preregistered", "locked"}:
            failures.append(
                f"{exp['Experiment_ID']}: null model is not preregistered"
            )

    return claimed, failures


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--require-ready",
        action="store_true",
        help="fail when no controlled experiment is execution-ready",
    )
    args = parser.parse_args()

    claimed, failures = assess(args.root.resolve())
    if failures:
        raise SystemExit(
            "invalid controlled-execution readiness claim(s):\n- "
            + "\n- ".join(failures)
        )

    print(f"controlled_execution_ready_count={len(claimed)}")
    if claimed:
        print("ready_experiments=" + ",".join(claimed))
    else:
        print(
            "software checks may pass, but no experiment currently claims "
            "controlled execution readiness"
        )
        if args.require_ready:
            raise SystemExit("no controlled experiment is execution-ready")


if __name__ == "__main__":
    main()
