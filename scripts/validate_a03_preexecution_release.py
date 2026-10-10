"""Validate the immutable A03 PR #86 review archive without running an experiment."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "release_packages" / "EXP-MAP-A03-preexecution-verification-v0.1"
SOURCE_COMMIT = "ded6317a20d78fbb9c451b8ef54eb87cc09d8242"
SOURCE_SHA = "259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968"
HISTORICAL_VERIFIER_SHA = "845a9f7e50b454bffcfb7df637c462df454a38ecba10a5823276e6c8ad7e9590"

def reject_if(condition: bool, message: str) -> None:
    """Fail closed on malformed archive content or unauthorized claim boundaries."""
    if condition:
        raise ValueError(message)

def verify_package(package: Path = PACKAGE, *, verify_origin: bool = False,
                   repository: Path = ROOT) -> dict:
    """Check exact archived bytes, provenance, historical receipt and closed gates.

    verify_origin also compares each archive file with the original immutable
    Git commit; it requires a full local Git history but never fetches data or
    executes the preregistered experiment.
    """
    manifest = json.loads((package / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
    reject_if(manifest.get("schema_version") != "star-exp-map-a03-preexecution-review-release-v0.1",
              "incorrect archive schema")
    reject_if(manifest.get("source_commit") != SOURCE_COMMIT, "source revision drift")
    reject_if(manifest.get("record_kind") != "candidate_review_archive_not_an_authorized_scientific_release",
              "archive evidence status was promoted")
    receipt_meta = manifest["historical_local_receipt"]
    reject_if(receipt_meta.get("verifier_sha256") != HISTORICAL_VERIFIER_SHA
              or receipt_meta.get("not_a_receipt_for_archived_pr86_code") is not True,
              "historical receipt was relabeled")
    ci = manifest["ci_reference"]
    reject_if(ci.get("run_id") != 38085559993 or ci.get("artifact_id") != 11682142104
              or ci.get("artifact_contents_embedded") is not False,
              "CI receipt was misrepresented")
    reject_if(manifest["source_input"].get("sha256") != SOURCE_SHA,
              "pinned arithmetic source hash changed")
    reject_if(manifest["science_boundaries"] != {
        "registered_experiment_executed": False,
        "actual_cohort_endpoint_computed": False,
        "controlled_execution_authorized": False,
        "controlled_support_established": False,
        "physical_support_established": False,
        "off_author_review_pending": True,
    }, "archive scientific scope was promoted")
    checksums = {}
    for line in (package / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        parts = line.split("  ", 1)
        reject_if(len(parts) != 2 or len(parts[0]) != 64
                  or any(c not in "0123456789abcdef" for c in parts[0]),
                  "invalid SHA256SUMS entry")
        digest, filename = parts
        reject_if(filename in checksums, "duplicate SHA256SUMS entry")
        checksums[filename] = digest
    source_files = manifest["files"]
    names = [item["path"] for item in source_files]
    expected = set(names) | {"SOURCE_MANIFEST.json", "README.md", "REVIEW_CHECKLIST.md"}
    reject_if(len(names) != len(set(names)) or set(checksums) != expected,
              "checksum coverage/duplication mismatch")
    for name, expected_digest in sorted(checksums.items()):
        rel = PurePosixPath(name)
        reject_if(rel.is_absolute() or ".." in rel.parts or not name or name == "SHA256SUMS",
                  "unsafe archive path")
        f = package / name
        reject_if(not f.is_file() or f.is_symlink(), "missing/unsafe file: " + name)
        actual = hashlib.sha256(f.read_bytes()).hexdigest()
        reject_if(actual != expected_digest, "archive SHA-256 mismatch: " + name)
    for item in source_files:
        path = item["path"]
        reject_if(checksums[path] != item["sha256"], "source manifest/checksum mismatch: " + path)
        reject_if(len(item["git_blob_sha"]) != 40, "malformed Git blob ID")
        if verify_origin:
            try:
                original = subprocess.check_output(
                    ["git", "show", SOURCE_COMMIT + ":" + item["origin_path"]],
                    cwd=repository, stderr=subprocess.PIPE,
                )
            except subprocess.CalledProcessError as exc:
                raise ValueError("cannot resolve frozen origin: " + path) from exc
            reject_if(original != (package / path).read_bytes(),
                      "origin differs from archived bytes: " + path)
            try:
                original_blob = subprocess.check_output(
                    ["git", "rev-parse", SOURCE_COMMIT + ":" + item["origin_path"]],
                    cwd=repository, text=True, stderr=subprocess.PIPE,
                ).strip()
            except subprocess.CalledProcessError as exc:
                raise ValueError("cannot resolve original blob: " + path) from exc
            reject_if(original_blob != item["git_blob_sha"],
                      "origin Git blob identity mismatch: " + path)
    config = json.loads((package / "frozen/config.json").read_text(encoding="utf-8"))
    spec = json.loads((package / "frozen/controlled_execution_spec.json").read_text(encoding="utf-8"))
    dataset_manifest = json.loads((package / "frozen/dataset_manifest.json").read_text(encoding="utf-8"))
    local = json.loads((package / "local_verification_2026-10-10.json").read_text(encoding="utf-8"))
    reject_if(spec["config"] != config, "frozen spec/config disagreement")
    reject_if(config["experiment_id"] != "EXP-MAP-A03" or config["input"]["source_sha256"] != SOURCE_SHA,
              "wrong experiment or raw source")
    reject_if(dataset_manifest["artifact"]["sha256"] != SOURCE_SHA, "dataset manifest source drift")
    reject_if(config["controls"] != {
        "controlled_execution_eligible": False,
        "controlled_support_eligible": False,
        "physical_support_eligible": False,
        "no_run_without_separate_activation": True,
    }, "frozen A03 activation gates opened")
    reject_if(local["verification_status"] != "PASS" or
              local["verifier_sha256"] != HISTORICAL_VERIFIER_SHA,
              "historical local record was altered")
    reject_if(local["registered_experiment_executed"] is not False or
              local["actual_cohort_endpoint_computed"] is not False or
              local["off_author_scientific_approval"] is not False,
              "historical scientific status was promoted")
    reject_if(local["cohort"]["accepted"] != 37936 or
              local["cohort"]["j_zero_exclusions"] != 106 or
              local["cohort"]["representatives"] != 38042 or
              local["cohort"]["source_rows"] != 64687,
              "historical cohort record was altered")
    for kind in ("dataset", "experiment"):
        reject_if(set(local["registry_flags"][kind].values()) != {"false"},
                  "historical eligibility record was altered")
    reject_if(checksums["verify_a03.py"] == HISTORICAL_VERIFIER_SHA,
              "PR86 source incorrectly identified as old local receipt")
    return {"archive_integrity": "PASS", "source_commit": SOURCE_COMMIT,
            "file_count": len(expected), "origin_verified": verify_origin,
            "experiment_executed": False, "activation_authorized": False}

def main() -> int:
    """Print a review-archive integrity result without executing inference."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-origin", action="store_true",
                        help="compare each archived byte against the immutable Git source commit")
    args = parser.parse_args()
    print(json.dumps(verify_package(verify_origin=args.verify_origin), sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
