"""CLI for registry-aware controlled experiment execution."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from src.control.execution import (
    ControlledExecutionError,
    execute_controlled_experiment,
    preflight_controlled_experiment,
    rerun_controlled_experiment,
    verify_reproduction_manifests,
)
from src.control.registry import RegistryError


def _print_json(value):
    print(json.dumps(value, indent=2, sort_keys=True))


def _preflight_summary(prepared, *, binding_only=False):
    resolved = prepared.resolved
    return {
        "ready": True,
        "binding_only": bool(binding_only),
        "controlled_execution_authorized": not bool(binding_only),
        "experiment_id": resolved.experiment["Experiment_ID"],
        "dataset_id": resolved.dataset["Dataset_ID"],
        "parameter_set_id": resolved.parameter["Parameter_Set_ID"],
        "null_id": resolved.null["Null_ID"],
        "git_sha": prepared.git["sha"],
        "spec_sha256": prepared.spec_sha256,
        "registry_record_sha256": resolved.record_hashes,
        "dataset_inputs": prepared.dataset_inputs,
        "code_inputs": prepared.code_inputs,
        "config_files": prepared.config_files,
        "rng_seeds": prepared.spec["rng_seeds"],
        "output_paths": prepared.spec["output_paths"],
        "container_image_digest": prepared.container_image_digest,
    }


def build_parser():
    parser = argparse.ArgumentParser(
        prog="star-controlled-experiment",
        description=(
            "Fail-closed registry-aware controlled-experiment transaction runner"
        ),
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="repository root (default: current directory)",
    )
    sub = parser.add_subparsers(dest="command_name", required=True)

    preflight = sub.add_parser(
        "preflight",
        help="verify registry gates, bindings, hashes, Git state, and execution spec",
    )
    preflight.add_argument("--spec", required=True, type=Path)
    preflight.add_argument(
        "--binding-only",
        action="store_true",
        help=(
            "verify preregistration bindings while requiring experiment and "
            "dataset execution eligibility to remain false; never authorizes a run"
        ),
    )

    run = sub.add_parser(
        "run",
        help="execute one eligible controlled experiment and emit a manifest",
    )
    run.add_argument("--spec", required=True, type=Path)
    run.add_argument("--executor-id", required=True)
    run.add_argument("--runs-root", type=Path)

    rerun = sub.add_parser(
        "rerun",
        help="re-execute an exact successful manifest and compare output hashes",
    )
    rerun.add_argument("--spec", required=True, type=Path)
    rerun.add_argument("--original-manifest", required=True, type=Path)
    rerun.add_argument("--executor-id", required=True)
    rerun.add_argument("--independence-note", required=True)
    rerun.add_argument("--runs-root", type=Path)

    verify = sub.add_parser(
        "verify-reproduction",
        help=(
            "verify manifest linkage and reproduction conditions without "
            "promoting registry support status"
        ),
    )
    verify.add_argument("--original-manifest", required=True, type=Path)
    verify.add_argument("--rerun-manifest", required=True, type=Path)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    root = args.root.resolve()

    try:
        if args.command_name == "preflight":
            prepared = preflight_controlled_experiment(
                root,
                args.spec,
                require_execution_eligibility=not args.binding_only,
            )
            _print_json(_preflight_summary(prepared, binding_only=args.binding_only))
            return 0

        if args.command_name == "run":
            manifest_path, manifest, code = execute_controlled_experiment(
                root,
                args.spec,
                runs_root=args.runs_root,
                executor_id=args.executor_id,
            )
            _print_json(
                {
                    "manifest": str(manifest_path),
                    "run_id": manifest["run_id"],
                    "transaction_status": manifest["transaction_status"],
                    "exit_status": manifest["exit_status"],
                    "runner_exit_status": code,
                }
            )
            return code

        if args.command_name == "rerun":
            manifest_path, manifest, code = rerun_controlled_experiment(
                root,
                args.spec,
                args.original_manifest,
                runs_root=args.runs_root,
                executor_id=args.executor_id,
                independence_note=args.independence_note,
            )
            _print_json(
                {
                    "manifest": str(manifest_path),
                    "run_id": manifest["run_id"],
                    "transaction_status": manifest["transaction_status"],
                    "exit_status": manifest["exit_status"],
                    "runner_exit_status": code,
                    "reproduction": manifest["reproduction"],
                }
            )
            return code

        if args.command_name == "verify-reproduction":
            report = verify_reproduction_manifests(
                args.original_manifest,
                args.rerun_manifest,
            )
            _print_json(report)
            return 0 if report["necessary_reproduction_conditions_met"] else 6

        raise AssertionError(f"unhandled command: {args.command_name}")
    except (ControlledExecutionError, RegistryError) as exc:
        print(f"controlled execution rejected: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
