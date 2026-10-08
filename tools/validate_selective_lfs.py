#!/usr/bin/env python3
"""Read-only validation of selective recovery evidence. Never hydrates or executes historical assets."""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "registry/recovered_asset_selection_v0.1.json"

def require(condition, message):
    if not condition:
        raise ValueError(message)

def validate(root=ROOT):
    ledger = json.loads((root / "registry/recovered_asset_selection_v0.1.json").read_text(encoding="utf-8"))
    manifest = json.loads((root / ledger["source_manifest"]).read_text(encoding="utf-8"))
    proof = json.loads((root / ledger["remote_lfs_proof"]).read_text(encoding="utf-8"))
    require(ledger["schema_version"] == "selective-lfs-candidate-v0.1", "Unknown ledger version")
    require(proof["uploaded_before_pointer_commit"] is True, "LFS upload proof absent")
    require(proof["independent_empty_cache_download_verified"] is True, "Independent LFS download proof absent")
    require(ledger["controls"] == {
        "controlled_execution_eligible": False, "controlled_support_eligible": False,
        "physical_support_eligible": False, "auto_ingest_enabled": False,
        "lfs_new_objects_committed": 0,
    }, "Candidate ledger cannot promote eligibility or claim new objects")
    archived = {a["path"]: a for a in manifest["assets"]}
    verified = {a["path"]: a for a in proof["files"]}
    seen = set()
    for record in ledger["existing_verified"]:
        p = record["path"]
        require(p not in seen, "Duplicate selection")
        seen.add(p)
        require(p.startswith("data/intake/recovered/2026-10-08/"), "Unexpected source scope")
        require(p in archived and p in verified, "Missing manifest or remote LFS proof")
        a, b = archived[p], verified[p]
        require(record["sha256"] == a["sha256"] == b["oid"] == b["remote_download_sha256"], "Source digest mismatch")
        require(record["bytes"] == a["bytes"] == b["bytes"], "Source size mismatch")
        require(a["controlled_execution_eligible"] is False and a["controlled_support_eligible"] is False
                and a["physical_support_eligible"] is False, "Source evidence promotion prohibited")
        # git show reads committed Git blobs; no lfs smudge/download is needed.
        pointer = subprocess.check_output(["git", "show", "HEAD:" + p], cwd=root, text=True)
        expected = ("version https://git-lfs.github.com/spec/v1\\n"
                    + "oid sha256:" + record["sha256"] + "\\n"
                    + "size " + str(record["bytes"]) + "\\n")
        require(pointer == expected, "Missing or mismatched *committed* LFS pointer for " + p)
    require(len(ledger["pending_review"]) > 0, "Pending candidate records missing")
    for record in ledger["pending_review"]:
        require(record["status"].startswith("pending_"), "Unverified candidate status")
        require(record["sha256"] is None and record["oid"] is None and record["repository_path"] is None,
                "Unverified candidate must not invent object or repository identity")
        require(isinstance(record["reported_bytes"], int) and record["reported_bytes"] > 0, "Invalid candidate size")
    return len(seen), len(ledger["pending_review"])

if __name__ == "__main__":
    verified, pending = validate()
    print(f"Selective recovery provenance valid: {verified} existing uploaded LFS assets; {pending} pending; 0 newly committed.")
