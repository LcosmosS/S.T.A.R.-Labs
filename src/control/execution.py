"""Fail-closed controlled-experiment execution transactions."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import re
import stat
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from src.control.registry import (
    RegistrySnapshot,
    canonical_json_bytes,
    execution_gate_failures,
    extract_integrity_sha256s,
    file_sha256,
)


SPEC_SCHEMA_VERSION = "1.0"
MANIFEST_SCHEMA_VERSION = "1.0"
_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")
_CONTAINER_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_INTERNAL_RUN_FILES = {
    "execution_config.json",
    "stdout.log",
    "stderr.log",
    "manifest.json",
    "manifest.sha256",
}


class ControlledExecutionError(RuntimeError):
    """Base error for controlled execution failures."""


class PreflightError(ControlledExecutionError):
    """Raised when an experiment is not allowed to execute."""


@dataclass(frozen=True)
class PreparedExecution:
    root: Path
    spec_path: Path
    spec: dict
    spec_sha256: str
    registry: RegistrySnapshot
    resolved: object
    git: dict
    dataset_inputs: list[dict]
    code_inputs: list[dict]
    config_files: list[dict]
    container_image_digest: str | None


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def _reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise PreflightError(f"duplicate JSON key in execution spec: {key}")
        result[key] = value
    return result


def _load_json(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as stream:
            value = json.load(stream, object_pairs_hook=_reject_duplicate_keys)
    except json.JSONDecodeError as exc:
        raise PreflightError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise PreflightError(f"expected JSON object in {path}")
    return value


def _validate_sha256(value, field: str) -> str:
    value = str(value).lower()
    if not _SHA256_HEX.fullmatch(value):
        raise PreflightError(f"{field} must be a 64-character SHA256 hex digest")
    return value


def _safe_relative_path(value: str, field: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise PreflightError(f"{field} must be a safe relative path: {value!r}")
    return path


def _resolve_input_path(root: Path, value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = root / path
    return path.resolve()


def _inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _git_output(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise PreflightError(f"unable to inspect Git state: {args!r}") from exc
    return result.stdout.strip()


def _git_state_unchecked(root: Path) -> dict:
    sha = _git_output(root, "rev-parse", "HEAD")
    branch = _git_output(root, "rev-parse", "--abbrev-ref", "HEAD")
    status = _git_output(
        root, "status", "--porcelain", "--untracked-files=all"
    )
    return {
        "sha": sha,
        "branch": branch,
        "dirty": bool(status),
        "status_porcelain": status,
    }


def _git_state(root: Path) -> dict:
    state = _git_state_unchecked(root)
    if state["dirty"]:
        raise PreflightError(
            "controlled execution requires a clean Git working tree; "
            "commit, remove, or ignore local changes first"
        )
    return {
        "sha": state["sha"],
        "branch": state["branch"],
        "dirty": False,
    }


def _assert_tracked_code_path(root: Path, path: Path) -> None:
    if not _inside(path, root):
        raise PreflightError(f"code input must remain inside repository: {path}")
    relative = path.relative_to(root).as_posix()
    try:
        subprocess.run(
            ["git", "ls-files", "--error-unmatch", relative],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise PreflightError(
            f"code input is not tracked by Git: {relative}"
        ) from exc


def _normalize_hashed_inputs(
    root: Path,
    entries,
    field: str,
    *,
    require_tracked: bool = False,
    tracked_path_checker: Callable[[Path, Path], None] = _assert_tracked_code_path,
) -> list[dict]:
    if not isinstance(entries, list) or (field == "dataset_inputs" and not entries):
        raise PreflightError(
            f"{field} must be a {'non-empty ' if field == 'dataset_inputs' else ''}list"
        )

    result = []
    seen = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise PreflightError(f"{field}[{index}] must be an object")
        if set(entry) != {"path", "sha256"}:
            raise PreflightError(
                f"{field}[{index}] must contain exactly path and sha256"
            )
        raw_path = str(entry["path"])
        expected = _validate_sha256(
            entry["sha256"], f"{field}[{index}].sha256"
        )
        path = _resolve_input_path(root, raw_path)
        if not path.is_file():
            raise PreflightError(f"{field}[{index}] is missing: {path}")
        if require_tracked:
            tracked_path_checker(root, path)
        actual = file_sha256(path)
        if actual != expected:
            raise PreflightError(
                f"{field}[{index}] SHA256 mismatch for {path}: "
                f"expected {expected}, got {actual}"
            )
        key = str(path)
        if key in seen:
            raise PreflightError(f"duplicate {field} path: {path}")
        seen.add(key)
        result.append(
            {
                "declared_path": raw_path,
                "resolved_path": str(path),
                "sha256": actual,
                "size_bytes": path.stat().st_size,
            }
        )
    return result


def _validate_spec(spec: dict) -> None:
    required = {
        "schema_version",
        "experiment_id",
        "registry_bindings",
        "command",
        "dataset_inputs",
        "code_inputs",
        "config",
        "config_files",
        "rng_seeds",
        "output_paths",
        "timeout_seconds",
        "container_image_digest",
    }
    extra = set(spec) - required
    missing = required - set(spec)
    if missing or extra:
        raise PreflightError(
            "execution spec fields mismatch; "
            f"missing={sorted(missing)}, extra={sorted(extra)}"
        )
    if spec["schema_version"] != SPEC_SCHEMA_VERSION:
        raise PreflightError(
            f"unsupported execution spec version: {spec['schema_version']!r}"
        )
    if not isinstance(spec["experiment_id"], str) or not spec["experiment_id"].strip():
        raise PreflightError("experiment_id must be a non-empty string")

    bindings = spec["registry_bindings"]
    expected_binding_names = {
        "experiment",
        "dataset",
        "provenance",
        "parameter",
        "null",
    }
    if not isinstance(bindings, dict) or set(bindings) != expected_binding_names:
        raise PreflightError(
            "registry_bindings must contain exactly experiment, dataset, "
            "provenance, parameter, and null"
        )
    for name, digest in bindings.items():
        _validate_sha256(digest, f"registry_bindings.{name}")

    command = spec["command"]
    if (
        not isinstance(command, list)
        or not command
        or not all(isinstance(value, str) and value for value in command)
    ):
        raise PreflightError("command must be a non-empty array of strings")

    if not isinstance(spec["config"], dict):
        raise PreflightError("config must be a JSON object")

    seeds = spec["rng_seeds"]
    if not isinstance(seeds, dict):
        raise PreflightError("rng_seeds must be a JSON object")
    for name, value in seeds.items():
        if not isinstance(name, str) or not name:
            raise PreflightError("rng_seeds keys must be non-empty strings")
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise PreflightError(
                f"rng_seeds.{name} must be a non-negative integer"
            )

    outputs = spec["output_paths"]
    if not isinstance(outputs, list) or not outputs:
        raise PreflightError("output_paths must be a non-empty list")
    normalized_outputs = []
    for index, value in enumerate(outputs):
        if not isinstance(value, str) or not value:
            raise PreflightError(f"output_paths[{index}] must be a string")
        normalized_outputs.append(
            _safe_relative_path(value, f"output_paths[{index}]").as_posix()
        )
    if len(normalized_outputs) != len(set(normalized_outputs)):
        raise PreflightError("output_paths contains duplicates")

    timeout = spec["timeout_seconds"]
    if timeout is not None:
        if isinstance(timeout, bool) or not isinstance(timeout, int) or timeout <= 0:
            raise PreflightError("timeout_seconds must be null or a positive integer")

    digest = spec["container_image_digest"]
    if digest is not None:
        if not isinstance(digest, str) or not _CONTAINER_DIGEST.fullmatch(
            digest.lower()
        ):
            raise PreflightError(
                "container_image_digest must be null or sha256:<64 hex>"
            )


def _verify_container_digest(spec_digest: str | None) -> str | None:
    runtime = os.environ.get("STAR_CONTAINER_IMAGE_DIGEST")
    if runtime is not None:
        runtime = runtime.strip().lower()
        if not _CONTAINER_DIGEST.fullmatch(runtime):
            raise PreflightError(
                "STAR_CONTAINER_IMAGE_DIGEST is not a valid sha256 digest"
            )
    if spec_digest is not None:
        spec_digest = spec_digest.lower()
        if runtime is None:
            raise PreflightError(
                "execution spec binds a container image digest but runtime "
                "STAR_CONTAINER_IMAGE_DIGEST is not set"
            )
        if runtime != spec_digest:
            raise PreflightError(
                "runtime container image digest does not match execution spec"
            )
    elif runtime is not None:
        raise PreflightError(
            "runtime declares a container image digest but execution spec "
            "does not bind it"
        )
    return runtime or spec_digest


def preflight_controlled_experiment(
    root: Path | str,
    spec_path: Path | str,
    *,
    git_state_provider: Callable[[Path], dict] = _git_state,
    tracked_path_checker: Callable[[Path, Path], None] = _assert_tracked_code_path,
) -> PreparedExecution:
    root = Path(root).resolve()
    spec_path = Path(spec_path)
    if not spec_path.is_absolute():
        spec_path = root / spec_path
    spec_path = spec_path.resolve()
    if not spec_path.is_file():
        raise PreflightError(f"execution spec is missing: {spec_path}")
    if not _inside(spec_path, root):
        raise PreflightError("execution spec must be committed inside the repository")
    tracked_path_checker(root, spec_path)

    spec = _load_json(spec_path)
    _validate_spec(spec)
    snapshot = RegistrySnapshot.load(root)
    resolved = snapshot.resolve(spec["experiment_id"])

    failures = execution_gate_failures(resolved)
    if failures:
        raise PreflightError(
            "controlled-execution gates rejected the experiment:\n- "
            + "\n- ".join(failures)
        )

    actual_bindings = resolved.record_hashes
    declared_bindings = {
        key: str(value).lower()
        for key, value in spec["registry_bindings"].items()
    }
    if declared_bindings != actual_bindings:
        differences = [
            name
            for name in sorted(actual_bindings)
            if declared_bindings.get(name) != actual_bindings[name]
        ]
        raise PreflightError(
            "execution spec registry binding mismatch: " + ", ".join(differences)
        )

    dataset_inputs = _normalize_hashed_inputs(
        root, spec["dataset_inputs"], "dataset_inputs"
    )
    provenance_hashes = extract_integrity_sha256s(
        resolved.provenance.get("Integrity_Check", "")
    )
    declared_dataset_hashes = {item["sha256"] for item in dataset_inputs}
    if not declared_dataset_hashes.issubset(provenance_hashes):
        missing = sorted(declared_dataset_hashes - provenance_hashes)
        raise PreflightError(
            "dataset input SHA256 is not bound by provenance Integrity_Check: "
            + ", ".join(missing)
        )

    code_inputs = _normalize_hashed_inputs(
        root,
        spec["code_inputs"],
        "code_inputs",
        require_tracked=True,
        tracked_path_checker=tracked_path_checker,
    )
    if not code_inputs:
        raise PreflightError("code_inputs must contain at least one tracked file")

    config_files = _normalize_hashed_inputs(
        root,
        spec["config_files"],
        "config_files",
        require_tracked=True,
        tracked_path_checker=tracked_path_checker,
    )

    git = git_state_provider(root)
    if not isinstance(git, dict) or not git.get("sha"):
        raise PreflightError("git state provider returned no commit SHA")
    if git.get("dirty"):
        raise PreflightError("controlled execution requires a clean Git state")

    container_digest = _verify_container_digest(
        spec["container_image_digest"]
    )

    return PreparedExecution(
        root=root,
        spec_path=spec_path,
        spec=spec,
        spec_sha256=file_sha256(spec_path),
        registry=snapshot,
        resolved=resolved,
        git=git,
        dataset_inputs=dataset_inputs,
        code_inputs=code_inputs,
        config_files=config_files,
        container_image_digest=container_digest,
    )


def _portable_hashed_inputs(items: list[dict]) -> list[dict]:
    return [
        {
            "path": item["declared_path"],
            "sha256": item["sha256"],
            "size_bytes": item["size_bytes"],
        }
        for item in items
    ]


def _execution_binding(prepared: PreparedExecution) -> dict:
    binding = {
        "experiment_id": prepared.spec["experiment_id"],
        "claim_ids": prepared.resolved.experiment.get("Claim_IDs", ""),
        "dataset_id": prepared.resolved.dataset.get("Dataset_ID", ""),
        "parameter_set_id": prepared.resolved.parameter.get("Parameter_Set_ID", ""),
        "null_id": prepared.resolved.null.get("Null_ID", ""),
        "git_sha": prepared.git["sha"],
        "spec_sha256": prepared.spec_sha256,
        "registry_record_sha256": prepared.resolved.record_hashes,
        "registry_file_sha256": prepared.registry.file_hashes,
        "dataset_inputs": _portable_hashed_inputs(prepared.dataset_inputs),
        "code_inputs": _portable_hashed_inputs(prepared.code_inputs),
        "config": prepared.spec["config"],
        "config_files": _portable_hashed_inputs(prepared.config_files),
        "command_template": prepared.spec["command"],
        "rng_seeds": prepared.spec["rng_seeds"],
        "output_paths": [
            _safe_relative_path(value, "output_paths").as_posix()
            for value in prepared.spec["output_paths"]
        ],
        "timeout_seconds": prepared.spec["timeout_seconds"],
        "container_image_digest": prepared.container_image_digest,
    }
    return binding


def _execution_binding_sha256(prepared: PreparedExecution) -> str:
    return hashlib.sha256(
        canonical_json_bytes(_execution_binding(prepared))
    ).hexdigest()


def _post_run_integrity(
    prepared: PreparedExecution,
    git_state_provider: Callable[[Path], dict],
) -> dict:
    failures = []
    git_after = None
    try:
        git_after = git_state_provider(prepared.root)
    except (ControlledExecutionError, OSError, subprocess.SubprocessError) as exc:
        failures.append(f"Git state changed or became unverifiable: {exc}")
    else:
        if git_after.get("dirty"):
            failures.append("Git working tree became dirty during execution")
        if git_after.get("sha") != prepared.git.get("sha"):
            failures.append("Git HEAD changed during execution")

    def check_file(path: Path, expected: str, label: str):
        if not path.is_file():
            failures.append(f"{label} disappeared during execution: {path}")
            return
        actual = file_sha256(path)
        if actual != expected:
            failures.append(
                f"{label} changed during execution: {path}; "
                f"expected {expected}, got {actual}"
            )

    check_file(
        prepared.spec_path,
        prepared.spec_sha256,
        "execution spec",
    )

    for filename, expected in prepared.registry.file_hashes.items():
        check_file(
            prepared.registry.registry_dir / filename,
            expected,
            f"registry file {filename}",
        )

    for label, items in (
        ("dataset input", prepared.dataset_inputs),
        ("code input", prepared.code_inputs),
        ("config file", prepared.config_files),
    ):
        for item in items:
            check_file(
                Path(item["resolved_path"]),
                item["sha256"],
                label,
            )

    return {
        "passed": not failures,
        "failures": failures,
        "git_after": git_after,
    }


def _environment_snapshot() -> dict:
    packages = []
    for distribution in importlib.metadata.distributions():
        name = distribution.metadata.get("Name")
        if name:
            packages.append(
                {"name": str(name), "version": str(distribution.version)}
            )
    packages.sort(key=lambda item: (item["name"].lower(), item["version"]))

    snapshot = {
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "packages": packages,
        "pythonhashseed": os.environ.get("PYTHONHASHSEED"),
    }
    snapshot["environment_sha256"] = hashlib.sha256(
        canonical_json_bytes(snapshot)
    ).hexdigest()
    return snapshot


def _new_run_id() -> str:
    stamp = _utc_now().strftime("%Y%m%dT%H%M%S%fZ")
    return f"{stamp}-{uuid.uuid4().hex[:12]}"


def _substitute_command(command: list[str], run_dir: Path, root: Path, experiment_id: str):
    replacements = {
        "{run_dir}": str(run_dir),
        "{repo_root}": str(root),
        "{experiment_id}": experiment_id,
    }
    result = []
    for value in command:
        updated = value
        for token, replacement in replacements.items():
            updated = updated.replace(token, replacement)
        result.append(updated)
    return result


def _write_json_new(path: Path, value) -> None:
    payload = json.dumps(
        value,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
    ).encode("utf-8") + b"\n"
    with path.open("xb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())


def _make_read_only(path: Path) -> None:
    try:
        path.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    except OSError:
        pass


def _all_output_artifacts(run_dir: Path) -> list[dict]:
    artifacts = []
    for path in sorted(run_dir.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(run_dir).as_posix()
        if relative in _INTERNAL_RUN_FILES:
            continue
        artifacts.append(
            {
                "path": relative,
                "sha256": file_sha256(path),
                "size_bytes": path.stat().st_size,
            }
        )
    return artifacts


def _hash_log(path: Path) -> dict:
    return {
        "path": path.name,
        "sha256": file_sha256(path),
        "size_bytes": path.stat().st_size,
    }


def _write_manifest(run_dir: Path, manifest: dict) -> tuple[Path, str]:
    manifest_path = run_dir / "manifest.json"
    _write_json_new(manifest_path, manifest)
    digest = file_sha256(manifest_path)
    sidecar = run_dir / "manifest.sha256"
    with sidecar.open("x", encoding="ascii") as stream:
        stream.write(f"{digest}  manifest.json\n")
        stream.flush()
        os.fsync(stream.fileno())
    _make_read_only(manifest_path)
    _make_read_only(sidecar)
    return manifest_path, digest


def _load_verified_manifest(path: Path | str) -> tuple[dict, str]:
    path = Path(path).resolve()
    if not path.is_file():
        raise ControlledExecutionError(f"manifest is missing: {path}")
    digest = file_sha256(path)
    sidecar = path.with_name("manifest.sha256")
    if not sidecar.is_file():
        raise ControlledExecutionError(
            f"manifest SHA256 sidecar is missing: {sidecar}"
        )
    parts = sidecar.read_text(encoding="ascii").strip().split()
    if not parts or parts[0].lower() != digest:
        raise ControlledExecutionError(
            f"manifest SHA256 sidecar does not match {path}"
        )
    value = _load_json(path)
    return value, digest


def _execute_prepared(
    prepared: PreparedExecution,
    *,
    runs_root: Path,
    executor_id: str,
    mode: str,
    git_state_provider: Callable[[Path], dict],
    reproduction_source: tuple[dict, str] | None = None,
    independence_note: str | None = None,
) -> tuple[Path, dict, int]:
    if not executor_id.strip():
        raise ControlledExecutionError("executor_id must be non-empty")

    run_id = _new_run_id()
    run_dir = runs_root / prepared.spec["experiment_id"] / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    config_path = run_dir / "execution_config.json"
    _write_json_new(config_path, prepared.spec["config"])
    _make_read_only(config_path)

    stdout_path = run_dir / "stdout.log"
    stderr_path = run_dir / "stderr.log"
    command = _substitute_command(
        prepared.spec["command"],
        run_dir,
        prepared.root,
        prepared.spec["experiment_id"],
    )

    environment = _environment_snapshot()
    env = os.environ.copy()
    env.update(
        {
            "STAR_RUN_DIR": str(run_dir),
            "STAR_REPO_ROOT": str(prepared.root),
            "STAR_EXPERIMENT_ID": prepared.spec["experiment_id"],
            "STAR_EXECUTION_CONFIG": str(config_path),
            "STAR_RNG_SEEDS_JSON": json.dumps(
                prepared.spec["rng_seeds"],
                sort_keys=True,
                separators=(",", ":"),
            ),
        }
    )
    for name, value in prepared.spec["rng_seeds"].items():
        normalized = re.sub(r"[^A-Za-z0-9_]", "_", name).upper()
        env[f"STAR_RNG_{normalized}"] = str(value)

    start = _utc_now()
    monotonic_start = time.monotonic()
    experiment_exit_status = 127
    runtime_error = None

    with stdout_path.open("xb") as stdout_stream, stderr_path.open("xb") as stderr_stream:
        try:
            # SECURITY: command is a committed, SHA-bound argv list and
            # is executed with shell=False. Shell escaping is therefore neither
            # required nor used; the reviewed execution spec is the authority.
            completed = subprocess.run(
                command,
                cwd=prepared.root,
                shell=False,
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=stdout_stream,
                stderr=stderr_stream,
                timeout=prepared.spec["timeout_seconds"],
                check=False,
            )
            experiment_exit_status = int(completed.returncode)
        except subprocess.TimeoutExpired:
            experiment_exit_status = 124
            runtime_error = "experiment exceeded timeout_seconds"
            stderr_stream.write((runtime_error + "\n").encode("utf-8"))
        except OSError as exc:
            experiment_exit_status = 127
            runtime_error = f"unable to start experiment command: {exc}"
            stderr_stream.write((runtime_error + "\n").encode("utf-8"))

    end = _utc_now()
    duration = time.monotonic() - monotonic_start

    post_run_integrity = _post_run_integrity(
        prepared,
        git_state_provider,
    )
    artifacts = _all_output_artifacts(run_dir)
    artifact_by_path = {item["path"]: item for item in artifacts}
    expected_outputs = [
        _safe_relative_path(value, "output_paths").as_posix()
        for value in prepared.spec["output_paths"]
    ]
    missing_outputs = [
        path for path in expected_outputs if path not in artifact_by_path
    ]

    reproduction = None
    reproduction_match = None
    if reproduction_source is not None:
        original, original_digest = reproduction_source
        original_outputs = {
            item["path"]: item["sha256"]
            for item in original.get("outputs", {}).get("artifacts", [])
        }
        current_outputs = {
            item["path"]: item["sha256"] for item in artifacts
        }
        reproduction_match = (
            original_outputs == current_outputs
            and original.get("exit_status") == experiment_exit_status
        )
        reproduction = {
            "original_manifest_sha256": original_digest,
            "original_run_id": original.get("run_id"),
            "output_hash_match": original_outputs == current_outputs,
            "exit_status_match": (
                original.get("exit_status") == experiment_exit_status
            ),
            "environment_match": (
                original.get("environment", {}).get("environment_sha256")
                == environment["environment_sha256"]
            ),
            "different_executor": (
                original.get("executor_id") != executor_id
            ),
            "independence_note": independence_note,
            "reproduction_match": reproduction_match,
        }

    if not post_run_integrity["passed"]:
        transaction_status = "post_run_integrity_failed"
        runner_exit_status = 7
    elif experiment_exit_status != 0:
        transaction_status = "experiment_failed"
        runner_exit_status = 3
    elif missing_outputs:
        transaction_status = "output_contract_failed"
        runner_exit_status = 4
    elif reproduction_source is not None and not reproduction_match:
        transaction_status = "reproduction_mismatch"
        runner_exit_status = 5
    else:
        transaction_status = "completed"
        runner_exit_status = 0

    resolved = prepared.resolved
    manifest = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "run_id": run_id,
        "mode": mode,
        "transaction_status": transaction_status,
        "exit_status": experiment_exit_status,
        "runner_exit_status": runner_exit_status,
        "executor_id": executor_id,
        "experiment_id": resolved.experiment["Experiment_ID"],
        "claim_ids": [
            value.strip()
            for value in resolved.experiment.get("Claim_IDs", "").split(";")
            if value.strip()
        ],
        "dataset_id": resolved.dataset["Dataset_ID"],
        "parameter_set_id": resolved.parameter["Parameter_Set_ID"],
        "null_id": resolved.null["Null_ID"],
        "git": prepared.git,
        "registry": {
            "records": resolved.records,
            "record_sha256": resolved.record_hashes,
            "registry_file_sha256": prepared.registry.file_hashes,
        },
        "dataset": {
            "inputs": prepared.dataset_inputs,
            "provenance_integrity_sha256": sorted(
                extract_integrity_sha256s(
                    resolved.provenance.get("Integrity_Check", "")
                )
            ),
        },
        "parameters": {
            "definition": resolved.parameter.get("Definition"),
            "preregistration_status": resolved.parameter.get(
                "Preregistration_Status"
            ),
        },
        "null_model": {
            "definition": resolved.null.get("Definition"),
            "preregistration_status": resolved.null.get(
                "Preregistration_Status"
            ),
        },
        "execution": {
            "spec_path": str(prepared.spec_path),
            "spec_sha256": prepared.spec_sha256,
            "binding": _execution_binding(prepared),
            "binding_sha256": _execution_binding_sha256(prepared),
            "command_template": prepared.spec["command"],
            "resolved_command": command,
            "config": prepared.spec["config"],
            "config_sha256": file_sha256(config_path),
            "config_files": prepared.config_files,
            "code_inputs": prepared.code_inputs,
            "rng_seeds": prepared.spec["rng_seeds"],
            "timeout_seconds": prepared.spec["timeout_seconds"],
            "container_image_digest": prepared.container_image_digest,
            "runtime_error": runtime_error,
        },
        "environment": environment,
        "transaction_identity": {
            "experiment_id": resolved.experiment["Experiment_ID"],
            "claim_ids": [
                value.strip()
                for value in resolved.experiment.get("Claim_IDs", "").split(";")
                if value.strip()
            ],
            "dataset_id": resolved.dataset["Dataset_ID"],
            "parameter_set_id": resolved.parameter["Parameter_Set_ID"],
            "null_id": resolved.null["Null_ID"],
            "git_sha": prepared.git["sha"],
            "execution_binding_sha256": _execution_binding_sha256(prepared),
            "environment_sha256": environment["environment_sha256"],
        },
        "timestamps": {
            "started_at_utc": _iso(start),
            "ended_at_utc": _iso(end),
            "duration_seconds": duration,
        },
        "outputs": {
            "expected_paths": expected_outputs,
            "missing_expected_paths": missing_outputs,
            "artifacts": artifacts,
        },
        "logs": {
            "stdout": _hash_log(stdout_path),
            "stderr": _hash_log(stderr_path),
        },
        "post_run_integrity": post_run_integrity,
        "reproduction": reproduction,
        "support_promotion": {
            "automatic": False,
            "statement": (
                "This manifest records execution/reproduction evidence only. "
                "It never changes controlled-support or physical-support eligibility."
            ),
        },
    }

    for artifact in artifacts:
        _make_read_only(run_dir / artifact["path"])
    _make_read_only(stdout_path)
    _make_read_only(stderr_path)

    manifest_path, manifest_digest = _write_manifest(run_dir, manifest)
    manifest["manifest_sha256"] = manifest_digest
    return manifest_path, manifest, runner_exit_status


def execute_controlled_experiment(
    root: Path | str,
    spec_path: Path | str,
    *,
    runs_root: Path | str | None = None,
    executor_id: str,
    git_state_provider: Callable[[Path], dict] = _git_state,
    tracked_path_checker: Callable[[Path, Path], None] = _assert_tracked_code_path,
) -> tuple[Path, dict, int]:
    prepared = preflight_controlled_experiment(
        root,
        spec_path,
        git_state_provider=git_state_provider,
        tracked_path_checker=tracked_path_checker,
    )
    run_root = (
        Path(runs_root).resolve()
        if runs_root is not None
        else prepared.root / "controlled_runs"
    )
    return _execute_prepared(
        prepared,
        runs_root=run_root,
        executor_id=executor_id,
        mode="primary",
        git_state_provider=git_state_provider,
    )


def _assert_reproduction_source(
    prepared: PreparedExecution,
    original: dict,
) -> None:
    if original.get("schema_version") != MANIFEST_SCHEMA_VERSION:
        raise PreflightError("original manifest schema version is unsupported")
    if (
        original.get("transaction_status") != "completed"
        or original.get("exit_status") != 0
    ):
        raise PreflightError(
            "original manifest is not a successful controlled execution"
        )
    if original.get("experiment_id") != prepared.spec["experiment_id"]:
        raise PreflightError("rerun Experiment_ID does not match original manifest")
    if not original.get("post_run_integrity", {}).get("passed"):
        raise PreflightError(
            "original manifest did not pass post-run integrity validation"
        )
    if original.get("git", {}).get("sha") != prepared.git.get("sha"):
        raise PreflightError(
            "rerun must execute the exact Git SHA recorded by the original manifest"
        )

    expected_binding = _execution_binding(prepared)
    expected_binding_sha = _execution_binding_sha256(prepared)
    execution = original.get("execution", {})
    if execution.get("binding_sha256") != expected_binding_sha:
        raise PreflightError(
            "rerun execution binding hash does not match original manifest"
        )
    if execution.get("binding") != expected_binding:
        raise PreflightError(
            "rerun complete execution binding does not match original manifest"
        )

    expected_fields = {
        "spec_sha256": prepared.spec_sha256,
        "command_template": prepared.spec["command"],
        "config": prepared.spec["config"],
        "rng_seeds": prepared.spec["rng_seeds"],
        "timeout_seconds": prepared.spec["timeout_seconds"],
        "container_image_digest": prepared.container_image_digest,
    }
    for field, expected in expected_fields.items():
        if execution.get(field) != expected:
            raise PreflightError(
                f"rerun original manifest execution.{field} does not "
                "match the current locked transaction"
            )

    for field, current_items in (
        ("code_inputs", prepared.code_inputs),
        ("config_files", prepared.config_files),
    ):
        original_items = execution.get(field, [])
        if (
            _portable_hashed_inputs(original_items)
            != _portable_hashed_inputs(current_items)
        ):
            raise PreflightError(
                f"rerun original manifest execution.{field} does not "
                "match the current locked transaction"
            )

    if (
        original.get("registry", {}).get("record_sha256")
        != prepared.resolved.record_hashes
    ):
        raise PreflightError(
            "rerun registry record hashes do not match original manifest"
        )
    if (
        original.get("registry", {}).get("registry_file_sha256")
        != prepared.registry.file_hashes
    ):
        raise PreflightError(
            "rerun registry file hashes do not match original manifest"
        )

    original_inputs = _portable_hashed_inputs(
        original.get("dataset", {}).get("inputs", [])
    )
    current_inputs = _portable_hashed_inputs(prepared.dataset_inputs)
    if original_inputs != current_inputs:
        raise PreflightError(
            "rerun dataset input bindings do not match original manifest"
        )

    original_expected_outputs = (
        original.get("outputs", {}).get("expected_paths")
    )
    current_expected_outputs = expected_binding["output_paths"]
    if original_expected_outputs != current_expected_outputs:
        raise PreflightError(
            "rerun output contract does not match original manifest"
        )

def rerun_controlled_experiment(
    root: Path | str,
    spec_path: Path | str,
    original_manifest: Path | str,
    *,
    runs_root: Path | str | None = None,
    executor_id: str,
    independence_note: str,
    git_state_provider: Callable[[Path], dict] = _git_state,
    tracked_path_checker: Callable[[Path, Path], None] = _assert_tracked_code_path,
) -> tuple[Path, dict, int]:
    if not independence_note.strip():
        raise PreflightError(
            "rerun requires a non-empty independence_note describing the "
            "separate execution context"
        )
    original = _load_verified_manifest(original_manifest)
    prepared = preflight_controlled_experiment(
        root,
        spec_path,
        git_state_provider=git_state_provider,
        tracked_path_checker=tracked_path_checker,
    )
    _assert_reproduction_source(prepared, original[0])
    run_root = (
        Path(runs_root).resolve()
        if runs_root is not None
        else prepared.root / "controlled_runs"
    )
    return _execute_prepared(
        prepared,
        runs_root=run_root,
        executor_id=executor_id,
        mode="rerun",
        git_state_provider=git_state_provider,
        reproduction_source=original,
        independence_note=independence_note,
    )


def verify_reproduction_manifests(
    original_manifest: Path | str,
    rerun_manifest: Path | str,
) -> dict:
    original, original_digest = _load_verified_manifest(original_manifest)
    rerun, rerun_digest = _load_verified_manifest(rerun_manifest)

    checks = {
        "original_success": (
            original.get("transaction_status") == "completed"
            and original.get("exit_status") == 0
        ),
        "rerun_success": (
            rerun.get("transaction_status") == "completed"
            and rerun.get("exit_status") == 0
        ),
        "different_run_id": original.get("run_id") != rerun.get("run_id"),
        "same_experiment_id": (
            original.get("experiment_id") == rerun.get("experiment_id")
        ),
        "same_git_sha": (
            original.get("git", {}).get("sha")
            == rerun.get("git", {}).get("sha")
        ),
        "same_spec_sha256": (
            original.get("execution", {}).get("spec_sha256")
            == rerun.get("execution", {}).get("spec_sha256")
        ),
        "same_execution_binding": (
            original.get("execution", {}).get("binding_sha256")
            == rerun.get("execution", {}).get("binding_sha256")
        ),
        "same_registry_bindings": (
            original.get("registry", {}).get("record_sha256")
            == rerun.get("registry", {}).get("record_sha256")
        ),
        "rerun_references_original": (
            rerun.get("reproduction", {}).get("original_manifest_sha256")
            == original_digest
        ),
        "output_hash_match": bool(
            rerun.get("reproduction", {}).get("output_hash_match")
        ),
        "exit_status_match": bool(
            rerun.get("reproduction", {}).get("exit_status_match")
        ),
        "independence_note_present": bool(
            str(
                rerun.get("reproduction", {}).get("independence_note") or ""
            ).strip()
        ),
        "different_executor": bool(
            rerun.get("reproduction", {}).get("different_executor")
        ),
    }
    return {
        "schema_version": "1.0",
        "original_manifest_sha256": original_digest,
        "rerun_manifest_sha256": rerun_digest,
        "checks": checks,
        "necessary_reproduction_conditions_met": all(checks.values()),
        "different_executor": rerun.get("reproduction", {}).get(
            "different_executor"
        ),
        "environment_match": rerun.get("reproduction", {}).get(
            "environment_match"
        ),
        "environment_match_required": False,
        "support_promotion_automatic": False,
        "statement": (
            "Passing this verification establishes the runner's transaction "
            "reproduction conditions, including a different executor identity. "
            "Environment equality is recorded but intentionally not required so "
            "a separately provisioned environment can reproduce the same locked "
            "Git/spec/data transaction. This is not automatic controlled-support "
            "or physical-support promotion."
        ),
    }
