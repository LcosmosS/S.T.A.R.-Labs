"""Inspect saved primary evidence; never import or execute the experiment."""

import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import statistics
import subprocess
import tarfile


RUN_ID = "20261016T041335361140Z-e60fd05117fc"
SOURCE_SHA = "1b0f2d7853608bfbab79cf2dc04b002f1f193eb2"
ARCHIVE = "EXP-MAP-A01-primary-execution.tar.gz"
ARCHIVE_SHA = "1a62bf4320a7465ff7308dffd9840e58ed9c68dad9267757c630ff621b60f9a8"
MANIFEST_SHA = "8a85f37958b5a2337fea40b02a69c5a521e5e599a9a13987524e2d40f5608cdb"
FILES = {
    "execution_config.json", "manifest.json", "manifest.sha256",
    "null_statistics.csv", "observed_projection.csv", "stderr.log",
    "stdout.log", "summary.json",
}
OUTPUTS = {"summary.json", "observed_projection.csv", "null_statistics.csv"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(data):
    return json.loads(data, object_pairs_hook=unique_object)


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def inspect(package, repo):
    archive_bytes = (package / ARCHIVE).read_bytes()
    require(sha(archive_bytes) == ARCHIVE_SHA, "Archive SHA256 mismatch")
    require(
        (package / (ARCHIVE + ".sha256")).read_bytes()
        == f"{ARCHIVE_SHA}  {ARCHIVE}\n".encode(),
        "Archive sidecar mismatch",
    )
    payload = {}
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as tar:
        members = tar.getmembers()
        names = [member.name for member in members]
        require(len(names) == len(set(names)), "Duplicate archive members")
        require(set(names) == {RUN_ID} | {f"{RUN_ID}/{n}" for n in FILES},
                "Unexpected or missing archive member")
        for member in members:
            if member.name == RUN_ID:
                require(member.isdir(), "Run root is not a directory")
                continue
            require(member.isfile(), "Archive contains a non-regular file")
            name = member.name.split("/", 1)[1]
            payload[name] = tar.extractfile(member).read()
            target = package / RUN_ID / name
            require(not target.is_symlink(), f"Symlink in unpacked run: {name}")
            require(target.read_bytes() == payload[name],
                    f"Unpacked bytes differ from archive: {name}")
    require({p.name for p in (package / RUN_ID).iterdir()} == FILES,
            "Unexpected or missing unpacked run entry")
    require(sha(payload["manifest.json"]) == MANIFEST_SHA,
            "Pinned raw manifest hash mismatch")
    require(payload["manifest.sha256"] == f"{MANIFEST_SHA}  manifest.json\n".encode(),
            "Manifest sidecar mismatch")
    manifest = load_json(payload["manifest.json"])
    summary = load_json(payload["summary.json"])
    execution = manifest["execution"]
    require(manifest["run_id"] == RUN_ID, "Run ID mismatch")
    require(manifest["experiment_id"] == "EXP-MAP-A01", "Experiment mismatch")
    require(manifest["git"]["sha"] == SOURCE_SHA, "Source commit mismatch")
    require(manifest["git"]["dirty"] is False, "Recorded source was dirty")
    require(manifest["mode"] == "primary" and manifest["reproduction"] is None,
            "Package is not a primary execution")
    require(manifest["transaction_status"] == "completed"
            and manifest["exit_status"] == manifest["runner_exit_status"] == 0,
            "Primary transaction did not complete successfully")
    require(manifest["post_run_integrity"]["passed"] is True
            and manifest["post_run_integrity"]["failures"] == []
            and manifest["post_run_integrity"]["git_after"]["sha"] == SOURCE_SHA
            and manifest["post_run_integrity"]["git_after"]["dirty"] is False,
            "Recorded post-run integrity did not pass")
    require(manifest["support_promotion"]["automatic"] is False,
            "Unexpected automatic support promotion")
    for name in ("experiment", "dataset"):
        record = manifest["registry"]["records"][name]
        require(record["Controlled_Support_Eligible"] == "false"
                and record["Physical_Support_Eligible"] == "false",
                f"Unexpected support eligibility: {name}")
    artifacts = manifest["outputs"]["artifacts"]
    require(len(artifacts) == 3 and {a["path"] for a in artifacts} == OUTPUTS,
            "Wrong output inventory")
    require(set(manifest["outputs"]["expected_paths"]) == OUTPUTS
            and manifest["outputs"]["missing_expected_paths"] == [],
            "Incomplete output contract")
    for artifact in artifacts + list(manifest["logs"].values()):
        data = payload[artifact["path"]]
        require(sha(data) == artifact["sha256"]
                and len(data) == artifact["size_bytes"],
                f"Artifact hash/size mismatch: {artifact['path']}")
    require(sha(payload["execution_config.json"]) == execution["config_sha256"],
            "Execution config hash mismatch")
    require(load_json(payload["execution_config.json"]) == execution["config"],
            "Execution config content mismatch")
    environment = dict(manifest["environment"])
    require(environment.pop("environment_sha256") == sha(canonical(environment)),
            "Environment canonical hash mismatch")
    binding = execution["binding"]
    require(sha(canonical(binding)) == execution["binding_sha256"],
            "Execution binding hash mismatch")
    require(binding["git_sha"] == SOURCE_SHA
            and binding["config"] == execution["config"]
            and binding["registry_file_sha256"] == manifest["registry"]["registry_file_sha256"]
            and binding["registry_record_sha256"] == manifest["registry"]["record_sha256"],
            "Execution binding disagreement")
    for name, record in manifest["registry"]["records"].items():
        require(sha(canonical(record)) == manifest["registry"]["record_sha256"][name],
                f"Registry row canonical hash mismatch: {name}")
    identity = manifest["transaction_identity"]
    require(identity["git_sha"] == SOURCE_SHA
            and identity["execution_binding_sha256"] == execution["binding_sha256"]
            and identity["environment_sha256"] == manifest["environment"]["environment_sha256"],
            "Transaction identity hash disagreement")
    for key in ("experiment_id", "claim_ids", "dataset_id", "null_id", "parameter_set_id"):
        require(identity[key] == manifest[key], f"Transaction identity mismatch: {key}")

    source_hashes = {}
    for item in execution["code_inputs"] + execution["config_files"]:
        path = item["declared_path"]
        data = git(repo, "show", f"{SOURCE_SHA}:{path}")
        require(sha(data) == item["sha256"] and len(data) == item["size_bytes"],
                f"Pinned source hash/size mismatch: {path}")
        source_hashes[path] = sha(data)
    spec_path = "controlled_execution/specs/EXP-MAP-A01.json"
    spec = git(repo, "show", f"{SOURCE_SHA}:{spec_path}")
    require(sha(spec) == execution["spec_sha256"] == binding["spec_sha256"],
            "Pinned execution spec hash mismatch")
    source_hashes[spec_path] = sha(spec)
    registry_keys = {
        "experiment": ("experiment_registry_v0.2.csv", "Experiment_ID", "EXP-MAP-A01"),
        "dataset": ("dataset_registry_v0.1.csv", "Dataset_ID", "DATA-ARITHMETIC"),
        "provenance": ("data_provenance_registry_v0.1.csv", "Provenance_ID", "PROV-004"),
        "parameter": ("parameter_registry_v0.1.csv", "Parameter_Set_ID", "PAR-MAP-001"),
        "null": ("null_registry_v0.1.csv", "Null_ID", "NULL-MAP-001"),
    }
    registry_data = {}
    for name, expected in manifest["registry"]["registry_file_sha256"].items():
        data = git(repo, "show", f"{SOURCE_SHA}:registry/{name}")
        require(sha(data) == expected, f"Pinned registry file hash mismatch: {name}")
        source_hashes[f"registry/{name}"] = sha(data)
        registry_data[name] = data
    for key, (name, column, value) in registry_keys.items():
        rows = list(csv.DictReader(io.StringIO(registry_data[name].decode("utf-8-sig")), strict=True))
        matches = [row for row in rows if row[column].strip() == value]
        require(len(matches) == 1 and matches[0] == manifest["registry"]["records"][key],
                f"Pinned registry row mismatch: {key}")
    require("25cec5ecfec8b9f016eb1631ac633194c2bed39f" in
            git(repo, "ls-tree", SOURCE_SHA, "data/ecdata").decode(),
            "Pinned ecdata gitlink mismatch")

    null_reader = csv.DictReader(io.StringIO(payload["null_statistics.csv"].decode()))
    require(null_reader.fieldnames == ["realization", "statistic"], "Null header mismatch")
    rows = list(null_reader)
    require(len(rows) == 999, "Null row count mismatch")
    require([int(row["realization"]) for row in rows] == list(range(1, 1000)),
            "Null realization sequence mismatch")
    values = [float(row["statistic"]) for row in rows]
    require(all(set(row) == {"realization", "statistic"} for row in rows)
            and all(math.isfinite(value) for value in values), "Malformed null values")
    observed = summary["observed_statistic"]
    require(math.isfinite(observed), "Nonfinite observed statistic")
    exceedances = sum(value >= observed for value in values)
    p_value = (1 + exceedances) / (len(values) + 1)
    require(summary["null_realizations"] == 999 and summary["null_seed"] == 1729
            and summary["null_prng"] == "splitmix64-fisher-yates-v1"
            and summary["alpha"] == 0.01 and summary["neighbor_k"] == 10,
            "Summary disagrees with locked null/endpoint settings")
    require(exceedances == summary["null_exceedances"] == 0
            and p_value == summary["p_value"] == 0.001
            and summary["decision"] == "reject_null", "Summary inference mismatch")

    reader = csv.DictReader(io.StringIO(payload["observed_projection.csv"].decode()))
    require(reader.fieldnames == ["label", "isogeny_class", "conductor", "delta", "rank",
                                 "torsion_order", "longitude", "latitude", "elevation"],
            "Projection header mismatch")
    projection = list(reader)
    require(len(projection) == summary["analysis_rows"] == 38042
            and summary["source_rows"] == 64687, "Cohort count mismatch")
    require(len({row["label"] for row in projection}) == 38042
            and len({row["isogeny_class"] for row in projection}) == 38042,
            "Duplicate projection labels/classes")
    rank_counts = {}
    for row in projection:
        require(None not in row and None not in row.values(), "Malformed projection row")
        conductor, delta, rank, torsion = (int(row[key]) for key in
                                         ("conductor", "delta", "rank", "torsion_order"))
        longitude, latitude, elevation = (float(row[key]) for key in
                                          ("longitude", "latitude", "elevation"))
        require(row["label"] == row["isogeny_class"] + "1"
                and 11 <= conductor <= 9999 and delta != 0 and rank >= 0 and torsion > 0,
                "Projection record outside cohort contract")
        expected = (360 * math.log(abs(delta)) / math.log(1e30),
                    180 * math.log(conductor) / math.log(1e9), 200 * rank)
        require(all(math.isfinite(x) and math.isclose(x, y, rel_tol=1e-12, abs_tol=1e-12)
                    for x, y in zip((longitude, latitude, elevation), expected)),
                f"Projection formula mismatch: {row['label']}")
        rank_counts[str(rank)] = rank_counts.get(str(rank), 0) + 1
    return {
        "status": "PASS", "verification_scope": "saved_primary_package_integrity_and_consistency",
        "scientific_code_executed": False, "independent_rerun_performed": False,
        "neighbor_graph_recomputed": False, "null_permutations_regenerated": False,
        "execution_authenticity_independently_verified": False,
        "support_flags_promoted": False, "run_id": RUN_ID, "source_git_sha": SOURCE_SHA,
        "archive": {"name": ARCHIVE, "sha256": ARCHIVE_SHA, "size_bytes": len(archive_bytes)},
        "run_files": {name: {"sha256": sha(data), "size_bytes": len(data)}
                      for name, data in sorted(payload.items())},
        "pinned_source_file_sha256": source_hashes,
        "environment_sha256": manifest["environment"]["environment_sha256"],
        "binding_sha256": execution["binding_sha256"],
        "null_inspection": {"rows": len(values), "indices": "1..999 in order",
                            "finite": True, "unique_statistics": len(set(values)),
                            "minimum": min(values), "maximum": max(values),
                            "mean": statistics.mean(values), "sample_sd": statistics.stdev(values),
                            "observed_statistic": observed, "exceedances": exceedances,
                            "corrected_p_value": p_value, "alpha": summary["alpha"],
                            "decision": summary["decision"]},
        "projection_inspection": {"rows": len(projection), "unique_labels": 38042,
                                  "unique_isogeny_classes": 38042, "rank_counts": rank_counts,
                                  "formulas_checked_from_saved_columns": True},
        "interpretation_limit": summary["interpretation_limit"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    try:
        report = inspect(args.package, args.repo_root)
    except (ValueError, KeyError, OSError, TypeError, tarfile.TarError,
            subprocess.CalledProcessError, csv.Error) as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}, indent=2))
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
