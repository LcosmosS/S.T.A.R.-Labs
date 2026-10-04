"""Validate claims of controlled-experiment execution readiness.

A software-green repository may legitimately contain zero execution-ready
experiments. This script fails only when a registry claims readiness without
all registry-level execution gates.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.control.registry import RegistrySnapshot, execution_gate_failures


def _truth(value):
    return str(value).strip().lower() == "true"


def assess(root: Path):
    snapshot = RegistrySnapshot.load(root)
    claimed = []
    failures = []

    for experiment_id, experiment in snapshot.experiments.items():
        if not _truth(experiment.get("Controlled_Execution_Eligible", "false")):
            continue
        claimed.append(experiment_id)
        resolved = snapshot.resolve(experiment_id)
        failures.extend(execution_gate_failures(resolved))

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
