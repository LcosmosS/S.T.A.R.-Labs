"""Read-only EXP-MAP-A01 preregistration/activation package verifier.

No registered graph, endpoint, null distribution, or controlled run is computed.
"""
import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "release_packages/EXP-MAP-A01-prereg-activation-repro-v0.1"


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


def check_a03_compatibility(dataset, experiment, spec, previous_sha):
    """Require that the shared dataset differs from A03's frozen row by one bit."""
    require(experiment["Controlled_Execution_Eligible"] == "false",
            "A03 experiment execution unexpectedly eligible")
    require(all(experiment[f] == "false" for f in
                ("Controlled_Support_Eligible", "Physical_Support_Eligible")),
            "A03 support unexpectedly eligible")
    require(dataset["Controlled_Execution_Eligible"] == "true",
            "A01 shared dataset inactive")
    old = dict(dataset)
    old["Controlled_Execution_Eligible"] = "false"
    require(row_hash(old) == previous_sha == spec["registry_bindings"]["dataset"],
            "A03 frozen dataset binding differs beyond approved A01 bit")


def verify(root=ROOT, *, require_source=False):
    """Verify frozen preregistration, activated rows and optional actual ecdata.

    This checks live registry bytes and source identity without invoking the
    controlled runner; it cannot establish a result or a reproduction.
    """
    meta = json.loads((root / PACKAGE / "SOURCE_MANIFEST.json").read_text())
    require(meta["schema_version"] == "star-a01-package-v0.1", "package schema drift")
    require(digest(root / "charter/STAR_Research_Charter_v0-2.pdf") ==
            meta["charter_sha256"], "governing charter digest mismatch")
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
        "approval_pr": meta["approval"]["pr"], "approval_merge": meta["approval"]["merge_sha"],
        "a03_execution_eligible": False, "controlled_support_eligible": False,
        "physical_support_eligible": False,
        "registered_experiment_executed_by_verifier": False,
        "independent_reproduction_executed_by_verifier": False
    }


def main():
    """Print a diagnostic receipt and optionally create it without overwrite."""
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--require-source", action="store_true")
    p.add_argument("--receipt", type=Path)
    args = p.parse_args()
    result = json.dumps(verify(require_source=args.require_source),
                        indent=2, sort_keys=True) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        with args.receipt.open("x", encoding="utf-8", newline="\n") as fh:
            fh.write(result)
    print(result, end="")


if __name__ == "__main__":
    main()
