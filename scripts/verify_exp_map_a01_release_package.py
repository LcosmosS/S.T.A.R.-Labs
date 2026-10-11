"""Read-only EXP-MAP-A01 preregistration/activation package verifier.

No registered graph, endpoint, null distribution, or controlled run is computed.
"""
import argparse
import csv
import hashlib
import json
import os
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "release_packages/EXP-MAP-A01-prereg-activation-repro-v0.1"

# Independent reviewed-state anchors: these are not read from the mutable
# SOURCE_MANIFEST or either mutable execution spec. Values were checked against
# GitHub's PR #78 review/merge records and source bytes at merge commit.
REVIEWED_APPROVAL = {
    "pr": 78,
    "url": "https://github.com/LcosmosS/S.T.A.R.-Labs/pull/78",
    "approved_by": "LibertySquared",
    "approved_at_utc": "2026-10-11T01:05:41Z",
    "final_head": "e0e57cd336a9fce84f21fafadce49ebfcc56fa67",
    "merge_sha": "7f1a03692539542e23b78263422f3be71da952ea",
    "approved_scope": "execution-only; not controlled or physical support",
    "compatible_layer_pr": 87,
}
REVIEWED_APPROVAL_REVIEW_ID = 5481428263
REVIEWED_COMPAT_MERGE_SHA = "4f89bd3bc5c2225d9b0d2ce985e7eb18e8cbd73d"
REVIEWED_SHA256 = {
    "charter/STAR_Research_Charter_v0-2.pdf":
        "9a63284900d5349f1d307160929b2542885e4c751439b785369b722d349a5c03",
    "controlled_execution/specs/EXP-MAP-A01.json":
        "ba9df175f5ddd43c5026a63a9d58cd47e7571927d406eaa7e59db17cf8ac7a0e",
    "controlled_execution/specs/EXP-MAP-A03.json":
        "6486e199bdc51359b8dd7b6c31b413b095e54c2fedaba3b85d0e1cf533a12f3f",
    "preregistrations/EXP-MAP-A01/config.json":
        "f3818f2753961feab603cd6c69b1ab0c1d743705e51de1641757d4d5fd96be75",
    "preregistrations/EXP-MAP-A01/dataset_manifest.json":
        "8550aaf6b5769fbf33f0a9ac6ee6fd8aa1cc59635bb92c59b461d107af34da42",
    "preregistrations/EXP-MAP-A01/protocol.md":
        "762f2ab0e457e3a396e799fc7349d9652383c9449f68922f02c0df174466df71",
}
EXPECTED_A03_EXPERIMENT_SHA256 = (
    "3b0bb9c77c80a19a0fca69103f084bb9368593d56d1e3bf037775fb74732794e"
)
EXPECTED_A03_INACTIVE_DATASET_SHA256 = (
    "2fe4ab7f5763f39c6cde8392c3f7d8ff1a565e4664ce6e192640b99f3fe146d7"
)
EXPECTED_ECDATA_SHA256 = (
    "259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968"
)


def require(ok, message):
    """Stop immediately on a missing source, binding, or eligibility invariant."""
    if not ok:
        raise ValueError(message)


def digest(path):
    """Compute the actual file's SHA-256 hex digest."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row_hash(row):
    """Match the controlled runner's compact, sorted-key UTF-8 row binding."""
    data = json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def registry(root, filename, field):
    """Load one canonical CSV table and reject duplicate or malformed records."""
    with (root / "registry" / filename).open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh, strict=True)
        require(reader.fieldnames and field in reader.fieldnames, "invalid CSV schema")
        require(len(set(reader.fieldnames)) == len(reader.fieldnames), "duplicate fields")
        rows = list(reader)
    require(bool(rows) and all(x.get(field) and None not in x for x in rows),
            "malformed or empty CSV")
    require(len({x[field] for x in rows}) == len(rows), "duplicate registry IDs")
    return {x[field]: x for x in rows}


def check_reviewed_baselines(root):
    """Compare governed files against SHA-256 pins independent of package metadata.

    The pins identify the exact reviewed A01/A03 specs and scientific inputs at
    the original PR #78 merge, not hashes supplied by the spec being checked.
    """
    for path, expected in REVIEWED_SHA256.items():
        require(digest(root / path) == expected,
                "reviewed baseline SHA-256 mismatch: " + path)


def _github_json(relative_path):
    """Fetch independent GitHub approval records; errors fail verification."""
    url = "https://api.github.com/repos/LcosmosS/S.T.A.R.-Labs/" + relative_path
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "star-a01-read-only-verifier",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers),
                                    timeout=25) as response:
            return json.load(response)
    except (OSError, ValueError) as exc:
        raise ValueError("GitHub approval lookup unavailable: " + relative_path) from exc


def verify_online_approval():
    """Cross-check the pinned approval against actual PR/review/merge records.

    This is an independent live GitHub check; a local offline PASS is never
    recorded as external authentication of a historical review.
    """
    pr = _github_json("pulls/78")
    require(pr.get("merged") is True and
            pr.get("merge_commit_sha") == REVIEWED_APPROVAL["merge_sha"] and
            pr.get("head", {}).get("sha") == REVIEWED_APPROVAL["final_head"],
            "PR #78 merge/head differs from reviewed approval")
    require(pr.get("user", {}).get("login") != REVIEWED_APPROVAL["approved_by"],
            "approval is not independent of PR author")
    reviews = _github_json("pulls/78/reviews?per_page=100")
    require(isinstance(reviews, list), "GitHub approval review response malformed")
    require(any(
        r.get("id") == REVIEWED_APPROVAL_REVIEW_ID and
        r.get("user", {}).get("login") == REVIEWED_APPROVAL["approved_by"] and
        r.get("state") == "APPROVED" and
        r.get("commit_id") == REVIEWED_APPROVAL["final_head"] and
        r.get("submitted_at") == REVIEWED_APPROVAL["approved_at_utc"]
        for r in reviews
    ), "reviewer identity, exact final head, or approval time differs")
    compatibility = _github_json("pulls/87")
    require(compatibility.get("merged") is True and
            compatibility.get("merge_commit_sha") == REVIEWED_COMPAT_MERGE_SHA,
            "PR #87 reviewed shared-dataset compatibility merge differs")
    return True


def check_a03_compatibility(dataset, experiment, spec, previous_sha):
    """Require that the shared dataset differs from A03's frozen row by one bit."""
    require(row_hash(experiment) == EXPECTED_A03_EXPERIMENT_SHA256 ==
            spec["registry_bindings"]["experiment"],
            "A03 frozen experiment binding mismatch")
    require(experiment["Controlled_Execution_Eligible"] == "false",
            "A03 experiment execution unexpectedly eligible")
    require(all(experiment[f] == "false" for f in
                ("Controlled_Support_Eligible", "Physical_Support_Eligible")),
            "A03 support unexpectedly eligible")
    require(dataset["Controlled_Execution_Eligible"] == "true",
            "A01 shared dataset inactive")
    old = dict(dataset)
    old["Controlled_Execution_Eligible"] = "false"
    require(row_hash(old) == previous_sha ==
            EXPECTED_A03_INACTIVE_DATASET_SHA256 ==
            spec["registry_bindings"]["dataset"],
            "A03 frozen dataset binding differs beyond approved A01 bit")


def verify(root=ROOT, *, require_source=False, verify_github_approval=False):
    """Verify frozen preregistration, activated rows and optional actual ecdata.

    This checks live registry bytes and source identity without invoking the
    controlled runner; it cannot establish a result or a reproduction.
    """
    meta = json.loads((root / PACKAGE / "SOURCE_MANIFEST.json").read_text())
    require(meta["schema_version"] == "star-a01-package-v0.1", "package schema drift")
    require(meta.get("approval") == REVIEWED_APPROVAL,
            "approval lineage differs from independent pinned GitHub record")
    require(meta.get("review_baseline_main") == REVIEWED_APPROVAL["merge_sha"],
            "approved historical merge baseline drift")
    require(meta.get("charter_sha256") == REVIEWED_SHA256[
        "charter/STAR_Research_Charter_v0-2.pdf"], "charter anchor drift")
    require(meta.get("a03_original_dataset_sha256") ==
            EXPECTED_A03_INACTIVE_DATASET_SHA256, "A03 inactive hash anchor drift")
    require(meta["source"]["sha256"] == EXPECTED_ECDATA_SHA256,
            "publisher source digest anchor drift")
    check_reviewed_baselines(root)
    github_verified = verify_online_approval() if verify_github_approval else False
    exps = registry(root, "experiment_registry_v0.2.csv", "Experiment_ID")
    data = registry(root, "dataset_registry_v0.1.csv", "Dataset_ID")
    prov = registry(root, "data_provenance_registry_v0.1.csv", "Dataset_ID")
    params = registry(root, "parameter_registry_v0.1.csv", "Parameter_Set_ID")
    nulls = registry(root, "null_registry_v0.1.csv", "Null_ID")
    a01, a03, dataset = exps["EXP-MAP-A01"], exps["EXP-MAP-A03"], data["DATA-ARITHMETIC"]
    source_prov = prov["DATA-ARITHMETIC"]
    spec = json.loads((root / "controlled_execution/specs/EXP-MAP-A01.json").read_text())
    a03_spec = json.loads((root / "controlled_execution/specs/EXP-MAP-A03.json").read_text())
    config = json.loads((root / "preregistrations/EXP-MAP-A01/config.json").read_text())
    manifest = json.loads((root / "preregistrations/EXP-MAP-A01/dataset_manifest.json").read_text())
    require(a01["Status"] == "preregistered" and a01["Mode"] == "controlled",
            "A01 preregistration status drift")
    require((a01["Claim_IDs"], a01["Dataset_ID"], a01["Parameter_Set_ID"],
             a01["Null_ID"]) == ("CLAIM-ACSC-001", "DATA-ARITHMETIC",
                                "PAR-MAP-001", "NULL-MAP-001"), "A01 IDs drift")
    require((a01["Controlled_Execution_Eligible"],
             dataset["Controlled_Execution_Eligible"]) == ("true", "true"),
            "A01 activation flags incomplete")
    require(all(r[k] == "false" for r in (a01, a03, dataset) for k in
                ("Controlled_Support_Eligible", "Physical_Support_Eligible")),
            "unsupported scientific promotion")
    require(dataset["Status"] == "locked" and
            dataset["Provenance_Status"] == source_prov["Provenance_Status"] == "verified" and
            dataset["Achieved_Evidence_Status"] == source_prov["Evidence_Status"] == "controlled",
            "arithmetic provenance/evidence drift")
    require(params["PAR-MAP-001"]["Preregistration_Status"] == "locked" and
            nulls["NULL-MAP-001"]["Preregistration_Status"] == "locked",
            "parameter/null locking drift")
    require(spec["config"] == config and config["protocol_version"] == "EXP-MAP-A01-prereg-v1",
            "A01 frozen configuration drift")
    require(config["input"]["analysis_rows"] == 38042 and
            config["endpoint"]["k"] == 10 and
            config["null"]["realizations"] == 999 and config["null"]["seed"] == 1729 and
            config["inference"]["alpha"] == 0.01, "primary endpoint/null drift")
    require(spec["output_paths"] == ["summary.json", "observed_projection.csv",
                                     "null_statistics.csv"], "output contract drift")
    rows = {"experiment": a01, "dataset": dataset, "provenance": source_prov,
            "parameter": params["PAR-MAP-001"], "null": nulls["NULL-MAP-001"]}
    hashes = {key: row_hash(value) for key, value in rows.items()}
    require(hashes == spec["registry_bindings"] == meta["approved_active_bindings"],
            "approved activation binding drift")
    check_a03_compatibility(dataset, a03, a03_spec, meta["a03_original_dataset_sha256"])
    require(spec["dataset_inputs"] == [{"path": meta["source"]["path"],
                                        "sha256": meta["source"]["sha256"]}],
            "source path/hash drift")
    require(manifest["artifact"]["sha256"] == meta["source"]["sha256"] and
            manifest["artifact"]["expected_rows"] == 64687 and
            manifest["experiment_selection"]["expected_rows"] == 38042,
            "source manifest drift")
    require(meta["source"]["sha256"] in source_prov["Integrity_Check"],
            "missing provenance SHA-256")
    for item in spec["config_files"] + spec["code_inputs"]:
        require(digest(root / item["path"]) == item["sha256"],
                "frozen input hash mismatch: " + item["path"])
    source = root / meta["source"]["path"]
    hydrated = False
    if require_source or source.is_file():
        require(source.is_file(), "upstream source not hydrated")
        require(source.stat().st_size == 2146401 and
                digest(source) == meta["source"]["sha256"],
                "source bytes mismatch")
        with source.open(encoding="ascii") as fh:
            require(sum(1 for _ in fh) == 64687, "source row count mismatch")
        hydrated = True
    if require_source:
        gitlink = subprocess.check_output(["git", "ls-tree", "HEAD", "data/ecdata"],
                                          cwd=root, text=True).split()
        require(len(gitlink) >= 3 and gitlink[2] == meta["source"]["gitlink"],
                "upstream ecdata gitlink mismatch")
    return {
        "kind": "A01_READ_ONLY_PACKAGE_VERIFICATION", "status": "PASS",
        "source_bytes_verified": hydrated, "registry_hashes": hashes,
        "approval_pr": REVIEWED_APPROVAL["pr"],
        "approval_merge": REVIEWED_APPROVAL["merge_sha"],
        "approval_identity_pinned": True,
        "approval_verified_against_github": github_verified,
        "approval_evidence_level": (
            "LIVE_GITHUB_PR_AND_REVIEW_MATCHED" if github_verified else
            "PINNED_REVIEW_CLAIMS_ONLY_EXTERNAL_RECORD_NOT_CHECKED"
        ),
        "reviewed_baseline_sha256": REVIEWED_SHA256,
        "a03_frozen_experiment_binding_verified": True,
        "a03_execution_eligible": False, "controlled_support_eligible": False,
        "physical_support_eligible": False,
        "registered_experiment_executed_by_verifier": False,
        "independent_reproduction_executed_by_verifier": False
    }


def main():
    """Print a diagnostic receipt and optionally create it without overwrite."""
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--require-source", action="store_true")
    p.add_argument("--verify-github-approval", action="store_true",
                   help="Fail closed unless live PR #78/#87 GitHub review records match")
    p.add_argument("--receipt", type=Path)
    args = p.parse_args()
    result = json.dumps(verify(require_source=args.require_source,
                               verify_github_approval=args.verify_github_approval),
                        indent=2, sort_keys=True) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        with args.receipt.open("x", encoding="utf-8", newline="\n") as fh:
            fh.write(result)
    print(result, end="")


if __name__ == "__main__":
    main()
