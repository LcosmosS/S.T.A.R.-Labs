"""Tests for the registry-aware controlled-experiment transaction runner."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import stat
import sys
from pathlib import Path

import pytest

from src.control.execution import (
    PreflightError,
    execute_controlled_experiment,
    preflight_controlled_experiment,
    rerun_controlled_experiment,
    verify_reproduction_manifests,
)
from src.control.registry import (
    RegistryError,
    RegistrySnapshot,
    execution_gate_failures,
    file_sha256,
)
from src.cli import star_controlled_experiment as controlled_cli


def _write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _fake_git(_root):
    return {"sha": "a" * 40, "branch": "test", "dirty": False}


def _dirty_git(_root):
    return {"sha": "a" * 40, "branch": "test", "dirty": True}


def _allow_tracked(_root, _path):
    return None


def _fixture_root(
    tmp_path,
    *,
    experiment_eligible=True,
    provenance_hash=None,
    claim_ids="CLAIM-TEST",
    registered_claims=("CLAIM-TEST",),
    crosswalk_claims=("CLAIM-TEST",),
):
    root = tmp_path / "repo"
    registry = root / "registry"
    data_dir = root / "data"
    data_dir.mkdir(parents=True)

    dataset_path = data_dir / "input.txt"
    dataset_path.write_text("elliptic-curve-fixture\n", encoding="utf-8")
    dataset_sha = file_sha256(dataset_path)

    experiment_script = root / "experiment.py"
    experiment_script.write_text(
        "from pathlib import Path\n"
        "import sys\n"
        "source = Path('data/input.txt').read_text(encoding='utf-8')\n"
        "Path(sys.argv[1]).write_bytes(source.upper().encode('utf-8'))\n",
        encoding="utf-8",
    )
    script_sha = file_sha256(experiment_script)

    integrity_sha = provenance_hash or dataset_sha

    _write_csv(
        registry / "experiment_registry_v0.2.csv",
        [
            "Experiment_ID",
            "Dataset_ID",
            "Parameter_Set_ID",
            "Null_ID",
            "Mode",
            "Claim_IDs",
            "Namespace_Resolution",
            "Controlled_Execution_Eligible",
        ],
        [
            {
                "Experiment_ID": "EXP-TEST",
                "Dataset_ID": "DATA-TEST",
                "Parameter_Set_ID": "PAR-TEST",
                "Null_ID": "NULL-TEST",
                "Mode": "controlled",
                "Claim_IDs": claim_ids,
                "Namespace_Resolution": "explicit_non_alias",
                "Controlled_Execution_Eligible": (
                    "true" if experiment_eligible else "false"
                ),
            }
        ],
    )
    _write_csv(
        registry / "claim_evidence_v0.2.csv",
        ["Claim_ID", "Controlled_Support_Eligible", "Physical_Support_Eligible"],
        [
            {
                "Claim_ID": claim_id,
                "Controlled_Support_Eligible": "false",
                "Physical_Support_Eligible": "false",
            }
            for claim_id in registered_claims
        ],
    )
    _write_csv(
        registry / "claim_experiment_crosswalk_v0.2.csv",
        ["Claim_ID", "Experiment_ID"],
        [
            {"Claim_ID": claim_id, "Experiment_ID": "EXP-TEST"}
            for claim_id in crosswalk_claims
        ],
    )
    _write_csv(
        registry / "dataset_registry_v0.1.csv",
        ["Dataset_ID", "Controlled_Execution_Eligible"],
        [{"Dataset_ID": "DATA-TEST", "Controlled_Execution_Eligible": "true"}],
    )
    _write_csv(
        registry / "data_provenance_registry_v0.1.csv",
        [
            "Dataset_ID",
            "Provenance_Status",
            "Evidence_Status",
            "Integrity_Check",
        ],
        [
            {
                "Dataset_ID": "DATA-TEST",
                "Provenance_Status": "verified",
                "Evidence_Status": "controlled",
                "Integrity_Check": f"SHA256={integrity_sha}",
            }
        ],
    )
    _write_csv(
        registry / "parameter_registry_v0.1.csv",
        [
            "Parameter_Set_ID",
            "Preregistration_Status",
            "Definition",
        ],
        [
            {
                "Parameter_Set_ID": "PAR-TEST",
                "Preregistration_Status": "locked",
                "Definition": "alpha=200; log_base=e",
            }
        ],
    )
    _write_csv(
        registry / "null_registry_v0.1.csv",
        [
            "Null_ID",
            "Preregistration_Status",
            "Definition",
        ],
        [
            {
                "Null_ID": "NULL-TEST",
                "Preregistration_Status": "locked",
                "Definition": "independent seeded invariant permutation",
            }
        ],
    )

    snapshot = RegistrySnapshot.load(root)
    bindings = snapshot.resolve("EXP-TEST").record_hashes
    spec = {
        "schema_version": "1.0",
        "experiment_id": "EXP-TEST",
        "registry_bindings": bindings,
        "command": [
            sys.executable,
            "{repo_root}/experiment.py",
            "{run_dir}/result.txt",
        ],
        "dataset_inputs": [
            {"path": "data/input.txt", "sha256": dataset_sha}
        ],
        "code_inputs": [
            {"path": "experiment.py", "sha256": script_sha}
        ],
        "config": {"projection": "primary", "alpha": 200},
        "config_files": [],
        "rng_seeds": {"permutation": 1729},
        "output_paths": ["result.txt"],
        "timeout_seconds": 30,
        "container_image_digest": None,
    }
    spec_dir = root / "controlled_execution" / "specs"
    spec_dir.mkdir(parents=True)
    spec_path = spec_dir / "EXP-TEST.json"
    spec_path.write_text(
        json.dumps(spec, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return root, spec_path, dataset_sha


def _execute(root, spec, runs_root, executor="executor-A"):
    return execute_controlled_experiment(
        root,
        spec,
        runs_root=runs_root,
        executor_id=executor,
        git_state_provider=_fake_git,
        tracked_path_checker=_allow_tracked,
    )


def test_preflight_resolves_and_binds_exact_registry_records(tmp_path):
    root, spec, dataset_sha = _fixture_root(tmp_path)

    prepared = preflight_controlled_experiment(
        root,
        spec,
        git_state_provider=_fake_git,
        tracked_path_checker=_allow_tracked,
    )

    assert prepared.resolved.experiment["Experiment_ID"] == "EXP-TEST"
    assert prepared.resolved.dataset["Dataset_ID"] == "DATA-TEST"
    assert prepared.resolved.parameter["Parameter_Set_ID"] == "PAR-TEST"
    assert prepared.resolved.null["Null_ID"] == "NULL-TEST"
    assert prepared.dataset_inputs[0]["sha256"] == dataset_sha
    assert prepared.git["sha"] == "a" * 40
    assert set(prepared.resolved.record_hashes) == {
        "experiment",
        "dataset",
        "provenance",
        "parameter",
        "null",
    }
    for filename in (
        "claim_evidence_v0.2.csv",
        "claim_experiment_crosswalk_v0.2.csv",
    ):
        assert prepared.registry.file_hashes[filename] == file_sha256(
            root / "registry" / filename
        )


@pytest.mark.parametrize(
    "claim_ids",
    ["CLAIM-UNKNOWN", "CLAIM-TEST;CLAIM-UNKNOWN", "OTHER:CLAIM-TEST"],
)
def test_preflight_rejects_unknown_claims_even_with_matching_spec(tmp_path, claim_ids):
    root, spec, _ = _fixture_root(tmp_path, claim_ids=claim_ids)

    with pytest.raises(PreflightError, match="unknown Claim_ID"):
        preflight_controlled_experiment(
            root,
            spec,
            git_state_provider=_fake_git,
            tracked_path_checker=_allow_tracked,
        )


@pytest.mark.parametrize(
    "claim_ids,reason",
    [
        ("CLAIM-TEST;", "Claim_IDs contains an empty Claim_ID"),
        ("CLAIM-TEST;;CLAIM-OTHER", "Claim_IDs contains an empty Claim_ID"),
        ("CLAIM-TEST;CLAIM-TEST", "duplicate Claim_ID 'CLAIM-TEST'"),
    ],
)
def test_preflight_rejects_malformed_claim_list_as_sole_gate_failure(
    tmp_path, claim_ids, reason
):
    root, spec, _ = _fixture_root(
        tmp_path,
        claim_ids=claim_ids,
        registered_claims=("CLAIM-TEST", "CLAIM-OTHER"),
        crosswalk_claims=("CLAIM-TEST", "CLAIM-OTHER"),
    )
    resolved = RegistrySnapshot.load(root).resolve("EXP-TEST")
    assert json.loads(spec.read_text(encoding="utf-8"))["registry_bindings"] == (
        resolved.record_hashes
    )
    assert execution_gate_failures(resolved) == [f"EXP-TEST: {reason}"]

    with pytest.raises(PreflightError, match=reason):
        preflight_controlled_experiment(
            root,
            spec,
            git_state_provider=_fake_git,
            tracked_path_checker=_allow_tracked,
        )


@pytest.mark.parametrize("claim_ids", ["CLAIM-OTHER", "CLAIM-TEST;CLAIM-OTHER"])
def test_preflight_rejects_known_claim_without_exact_crosswalk(tmp_path, claim_ids):
    root, spec, _ = _fixture_root(
        tmp_path,
        claim_ids=claim_ids,
        registered_claims=("CLAIM-TEST", "CLAIM-OTHER"),
    )

    with pytest.raises(PreflightError, match="missing claim/experiment crosswalk pair"):
        preflight_controlled_experiment(
            root,
            spec,
            git_state_provider=_fake_git,
            tracked_path_checker=_allow_tracked,
        )


def test_preflight_accepts_multiple_registered_claim_pairs(tmp_path):
    root, spec, _ = _fixture_root(
        tmp_path,
        claim_ids="CLAIM-TEST; CLAIM-OTHER",
        registered_claims=("CLAIM-TEST", "CLAIM-OTHER"),
        crosswalk_claims=("CLAIM-TEST", "CLAIM-OTHER"),
    )

    prepared = preflight_controlled_experiment(
        root,
        spec,
        git_state_provider=_fake_git,
        tracked_path_checker=_allow_tracked,
    )

    assert prepared.resolved.claim_experiments == {
        ("CLAIM-TEST", "EXP-TEST"),
        ("CLAIM-OTHER", "EXP-TEST"),
    }


def test_preflight_rejects_crosswalk_pair_for_another_experiment(tmp_path):
    root, spec, _ = _fixture_root(tmp_path)
    experiment_path = root / "registry" / "experiment_registry_v0.2.csv"
    with experiment_path.open(newline="", encoding="utf-8") as stream:
        experiments = list(csv.DictReader(stream))
    other = dict(experiments[0], Experiment_ID="EXP-OTHER")
    _write_csv(experiment_path, list(experiments[0]), [*experiments, other])
    _write_csv(
        root / "registry" / "claim_experiment_crosswalk_v0.2.csv",
        ["Claim_ID", "Experiment_ID"],
        [{"Claim_ID": "CLAIM-TEST", "Experiment_ID": "EXP-OTHER"}],
    )

    with pytest.raises(PreflightError, match="missing claim/experiment crosswalk pair"):
        preflight_controlled_experiment(
            root,
            spec,
            git_state_provider=_fake_git,
            tracked_path_checker=_allow_tracked,
        )


@pytest.mark.parametrize(
    "filename", ["claim_evidence_v0.2.csv", "claim_experiment_crosswalk_v0.2.csv"]
)
def test_preflight_rejects_missing_claim_registry(tmp_path, filename):
    root, spec, _ = _fixture_root(tmp_path)
    (root / "registry" / filename).unlink()

    with pytest.raises(RegistryError, match="missing controlled registry file"):
        preflight_controlled_experiment(
            root,
            spec,
            git_state_provider=_fake_git,
            tracked_path_checker=_allow_tracked,
        )


@pytest.mark.parametrize(
    "filename,content,message",
    [
        ("claim_evidence_v0.2.csv", b"Other\nCLAIM-TEST\n", "invalid registry headers"),
        (
            "claim_evidence_v0.2.csv",
            b"Claim_ID,Claim_ID\nCLAIM-TEST,CLAIM-TEST\n",
            "invalid registry headers",
        ),
        (
            "claim_evidence_v0.2.csv",
            b"Claim_ID\nCLAIM-TEST\nCLAIM-TEST\n",
            "duplicate Claim_ID",
        ),
        ("claim_evidence_v0.2.csv", b"Claim_ID,Status\nCLAIM-TEST\n", "malformed row"),
        ("claim_evidence_v0.2.csv", b"Claim_ID\nCLAIM-TEST,extra\n", "malformed row"),
        (
            "claim_evidence_v0.2.csv",
            b'Claim_ID\n"CLAIM-TEST\n',
            "cannot read controlled registry",
        ),
        (
            "claim_evidence_v0.2.csv",
            b"Claim_ID\n\xff\n",
            "cannot read controlled registry",
        ),
        (
            "claim_experiment_crosswalk_v0.2.csv",
            b"Claim_ID\nCLAIM-TEST\n",
            "invalid registry headers",
        ),
        (
            "claim_experiment_crosswalk_v0.2.csv",
            b"Claim_ID,Experiment_ID\nCLAIM-TEST\n",
            "malformed row",
        ),
        (
            "claim_experiment_crosswalk_v0.2.csv",
            b"Claim_ID,Experiment_ID\n,EXP-TEST\n",
            "empty Claim_ID/Experiment_ID",
        ),
        (
            "claim_experiment_crosswalk_v0.2.csv",
            b"Claim_ID,Experiment_ID\nCLAIM-UNKNOWN,EXP-TEST\n",
            "unknown Claim_ID",
        ),
        (
            "claim_experiment_crosswalk_v0.2.csv",
            b"Claim_ID,Experiment_ID\nCLAIM-TEST,EXP-UNKNOWN\n",
            "unknown Experiment_ID",
        ),
        (
            "claim_experiment_crosswalk_v0.2.csv",
            b"Claim_ID,Experiment_ID\nCLAIM-TEST,EXP-TEST\nCLAIM-TEST,EXP-TEST\n",
            "duplicate claim/experiment pair",
        ),
    ],
)
def test_preflight_rejects_malformed_claim_registry(
    tmp_path, filename, content, message
):
    root, spec, _ = _fixture_root(tmp_path)
    (root / "registry" / filename).write_bytes(content)

    with pytest.raises(RegistryError, match=message):
        preflight_controlled_experiment(
            root,
            spec,
            git_state_provider=_fake_git,
            tracked_path_checker=_allow_tracked,
        )


def test_preflight_rejects_ineligible_experiment_before_execution(tmp_path):
    root, spec, _ = _fixture_root(tmp_path, experiment_eligible=False)

    with pytest.raises(PreflightError, match="not controlled-execution eligible"):
        preflight_controlled_experiment(
            root,
            spec,
            git_state_provider=_fake_git,
            tracked_path_checker=_allow_tracked,
        )


def test_preflight_rejects_dataset_hash_not_bound_by_provenance(tmp_path):
    root, spec, _ = _fixture_root(tmp_path, provenance_hash="b" * 64)

    with pytest.raises(PreflightError, match="not bound by provenance"):
        preflight_controlled_experiment(
            root,
            spec,
            git_state_provider=_fake_git,
            tracked_path_checker=_allow_tracked,
        )


def test_preflight_rejects_registry_mutation_after_spec_lock(tmp_path):
    root, spec, _ = _fixture_root(tmp_path)
    parameter_path = root / "registry" / "parameter_registry_v0.1.csv"
    parameter_path.write_text(
        "Parameter_Set_ID,Preregistration_Status,Definition\n"
        "PAR-TEST,locked,alpha=999\n",
        encoding="utf-8",
    )

    with pytest.raises(PreflightError, match="registry binding mismatch"):
        preflight_controlled_experiment(
            root,
            spec,
            git_state_provider=_fake_git,
            tracked_path_checker=_allow_tracked,
        )


def test_preflight_rejects_dirty_git_state(tmp_path):
    root, spec, _ = _fixture_root(tmp_path)

    with pytest.raises(PreflightError, match="clean Git state"):
        preflight_controlled_experiment(
            root,
            spec,
            git_state_provider=_dirty_git,
            tracked_path_checker=_allow_tracked,
        )


def test_execution_emits_content_addressed_manifest(tmp_path):
    root, spec, dataset_sha = _fixture_root(tmp_path)
    runs_root = tmp_path / "runs"

    assert not runs_root.exists()
    manifest_path, manifest, code = _execute(root, spec, runs_root)

    assert runs_root.is_dir()
    assert code == 0
    assert manifest["transaction_status"] == "completed"
    assert manifest["exit_status"] == 0
    assert manifest["experiment_id"] == "EXP-TEST"
    assert manifest["claim_ids"] == ["CLAIM-TEST"]
    assert manifest["dataset_id"] == "DATA-TEST"
    assert manifest["parameter_set_id"] == "PAR-TEST"
    assert manifest["null_id"] == "NULL-TEST"
    assert manifest["git"]["sha"] == "a" * 40
    assert manifest["transaction_identity"]["experiment_id"] == "EXP-TEST"
    assert manifest["transaction_identity"]["claim_ids"] == ["CLAIM-TEST"]
    assert manifest["transaction_identity"]["dataset_id"] == "DATA-TEST"
    assert manifest["transaction_identity"]["parameter_set_id"] == "PAR-TEST"
    assert manifest["transaction_identity"]["null_id"] == "NULL-TEST"
    assert manifest["transaction_identity"]["git_sha"] == "a" * 40
    assert manifest["transaction_identity"]["environment_sha256"]
    assert manifest["transaction_identity"]["execution_binding_sha256"]
    assert manifest["dataset"]["inputs"][0]["sha256"] == dataset_sha
    assert manifest["parameters"]["definition"] == "alpha=200; log_base=e"
    assert (
        manifest["null_model"]["definition"]
        == "independent seeded invariant permutation"
    )
    assert manifest["execution"]["rng_seeds"] == {"permutation": 1729}
    assert manifest["support_promotion"]["automatic"] is False

    outputs = {item["path"]: item for item in manifest["outputs"]["artifacts"]}
    assert outputs["result.txt"]["sha256"] == hashlib.sha256(
        b"ELLIPTIC-CURVE-FIXTURE\n"
    ).hexdigest()

    sidecar = manifest_path.with_name("manifest.sha256")
    assert sidecar.is_file()
    assert sidecar.read_text(encoding="ascii").split()[0] == file_sha256(
        manifest_path
    )

    if os.name != "nt":
        assert not (manifest_path.stat().st_mode & stat.S_IWUSR)


def test_failed_experiment_still_emits_manifest_with_exit_status(tmp_path):
    root, spec_path, _ = _fixture_root(tmp_path)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    spec["command"] = [
        sys.executable,
        "-c",
        "import sys; sys.exit(7)",
    ]
    spec_path.write_text(
        json.dumps(spec, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    manifest_path, manifest, code = _execute(
        root,
        spec_path,
        tmp_path / "failed-runs",
    )

    assert manifest_path.is_file()
    assert code == 3
    assert manifest["transaction_status"] == "experiment_failed"
    assert manifest["exit_status"] == 7
    assert manifest["runner_exit_status"] == 3


def test_rerun_reexecutes_exact_manifest_and_compares_outputs(tmp_path):
    root, spec, _ = _fixture_root(tmp_path)
    runs_root = tmp_path / "runs"

    original_path, original, original_code = _execute(
        root,
        spec,
        runs_root,
        executor="executor-A",
    )
    assert original_code == 0

    rerun_path, rerun, rerun_code = rerun_controlled_experiment(
        root,
        spec,
        original_path,
        runs_root=runs_root,
        executor_id="executor-B",
        independence_note="fresh process and independent executor",
        git_state_provider=_fake_git,
        tracked_path_checker=_allow_tracked,
    )

    assert rerun_code == 0
    assert rerun["mode"] == "rerun"
    assert rerun["reproduction"]["reproduction_match"] is True
    assert rerun["reproduction"]["different_executor"] is True
    assert (
        rerun["reproduction"]["original_manifest_sha256"]
        == file_sha256(original_path)
    )

    report = verify_reproduction_manifests(original_path, rerun_path)
    assert report["necessary_reproduction_conditions_met"] is True
    assert report["support_promotion_automatic"] is False


def test_rerun_rejects_git_sha_drift(tmp_path):
    root, spec, _ = _fixture_root(tmp_path)
    original_path, _, code = _execute(
        root,
        spec,
        tmp_path / "runs",
    )
    assert code == 0

    def other_git(_root):
        return {"sha": "b" * 40, "branch": "test", "dirty": False}

    with pytest.raises(PreflightError, match="exact Git SHA"):
        rerun_controlled_experiment(
            root,
            spec,
            original_path,
            runs_root=tmp_path / "reruns",
            executor_id="executor-B",
            independence_note="different checkout",
            git_state_provider=other_git,
            tracked_path_checker=_allow_tracked,
        )


@pytest.mark.parametrize(
    "filename",
    [
        "parameter_registry_v0.1.csv",
        "claim_evidence_v0.2.csv",
        "claim_experiment_crosswalk_v0.2.csv",
    ],
)
def test_post_run_registry_mutation_fails_transaction_and_is_manifested(
    tmp_path, filename
):
    root, spec_path, _ = _fixture_root(tmp_path)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    spec["command"] = [
        sys.executable,
        "-c",
        (
            "from pathlib import Path; "
            "out=Path(r'{run_dir}/result.txt'); "
            "out.write_bytes(b'result\\n'); "
            f"p=Path(r'{{repo_root}}/registry/{filename}'); "
            "p.write_bytes(p.read_bytes() + b'\\n')"
        ),
    ]
    spec_path.write_text(
        json.dumps(spec, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    manifest_path, manifest, code = _execute(
        root,
        spec_path,
        tmp_path / "mutation-runs",
    )

    assert manifest_path.is_file()
    assert code == 7
    assert manifest["transaction_status"] == "post_run_integrity_failed"
    assert manifest["post_run_integrity"]["passed"] is False
    assert any(
        filename in failure
        for failure in manifest["post_run_integrity"]["failures"]
    )


def test_rerun_rejects_internally_stale_original_execution_binding(tmp_path):
    root, spec, _ = _fixture_root(tmp_path)
    original_path, _, code = _execute(
        root,
        spec,
        tmp_path / "runs",
    )
    assert code == 0

    original_path.chmod(stat.S_IRUSR | stat.S_IWUSR)
    sidecar = original_path.with_name("manifest.sha256")
    sidecar.chmod(stat.S_IRUSR | stat.S_IWUSR)
    manifest = json.loads(original_path.read_text(encoding="utf-8"))
    manifest["execution"]["command_template"] = [sys.executable, "-c", "print('stale')"]
    original_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    sidecar.write_text(
        f"{file_sha256(original_path)}  manifest.json\n",
        encoding="ascii",
    )

    with pytest.raises(PreflightError, match="command_template"):
        rerun_controlled_experiment(
            root,
            spec,
            original_path,
            runs_root=tmp_path / "reruns",
            executor_id="executor-B",
            independence_note="separate execution",
            git_state_provider=_fake_git,
            tracked_path_checker=_allow_tracked,
        )


def test_reproduction_verification_requires_different_executor_identity(tmp_path):
    root, spec, _ = _fixture_root(tmp_path)
    runs_root = tmp_path / "runs"
    original_path, _, code = _execute(
        root,
        spec,
        runs_root,
        executor="executor-A",
    )
    assert code == 0

    rerun_path, rerun, rerun_code = rerun_controlled_experiment(
        root,
        spec,
        original_path,
        runs_root=runs_root,
        executor_id="executor-A",
        independence_note="separate process, same declared executor",
        git_state_provider=_fake_git,
        tracked_path_checker=_allow_tracked,
    )
    assert rerun_code == 0
    assert rerun["reproduction"]["different_executor"] is False

    report = verify_reproduction_manifests(original_path, rerun_path)
    assert report["checks"]["different_executor"] is False
    assert report["necessary_reproduction_conditions_met"] is False
    assert report["environment_match_required"] is False


def test_cli_reports_registry_errors_as_controlled_rejections(monkeypatch, capsys):
    def fail_preflight(*args, **kwargs):
        raise RegistryError("unknown controlled Experiment_ID: EXP-MISSING")

    monkeypatch.setattr(
        controlled_cli,
        "preflight_controlled_experiment",
        fail_preflight,
    )
    code = controlled_cli.main(
        ["preflight", "--spec", "controlled_execution/specs/missing.json"]
    )

    captured = capsys.readouterr()
    assert code == 2
    assert "controlled execution rejected" in captured.err
    assert "EXP-MISSING" in captured.err


@pytest.mark.parametrize(
    "claim_ids,message",
    [
        ("CLAIM-UNKNOWN", "unknown Claim_ID"),
        ("CLAIM-OTHER", "missing claim/experiment crosswalk pair"),
    ],
)
def test_cli_run_rejects_invalid_claim_admission_before_execution(
    tmp_path, monkeypatch, capsys, claim_ids, message
):
    root, spec, _ = _fixture_root(
        tmp_path,
        claim_ids=claim_ids,
        registered_claims=("CLAIM-TEST", "CLAIM-OTHER"),
    )
    runs_root = tmp_path / "rejected-runs"

    def execute_with_fixture_git(*args, **kwargs):
        return execute_controlled_experiment(
            *args,
            **kwargs,
            git_state_provider=_fake_git,
            tracked_path_checker=_allow_tracked,
        )

    monkeypatch.setattr(
        controlled_cli, "execute_controlled_experiment", execute_with_fixture_git
    )
    code = controlled_cli.main(
        [
            "--root", str(root), "run", "--spec", str(spec),
            "--executor-id", "fixture-review", "--runs-root", str(runs_root),
        ]
    )

    assert code == 2
    assert message in capsys.readouterr().err
    assert not runs_root.exists()
