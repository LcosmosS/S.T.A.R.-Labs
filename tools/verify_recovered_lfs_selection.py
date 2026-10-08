#!/usr/bin/env python3
"""Fail-closed, read-only verification of the selected EXISTING Git LFS assets."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELECTION = "registry/recovered_lfs_selection_v0.1.json"

def validate(root: Path = ROOT, hydrate: bool = False) -> int:
    read = lambda path: json.loads((root / path).read_text(encoding="utf-8"))
    selected = read(SELECTION)
    manifest = read(selected["sourceManifest"])
    proof = read(selected["lfsProof"])
    if selected["schemaVersion"] != "0.1" or selected["newObjectsUploadedByThisPR"] != 0:
        raise ValueError("unexpected schema or new LFS upload claim")
    if selected["selectionStatus"] != "reuse_prior_independently_verified_lfs_objects_no_new_uploads":
        raise ValueError("unsupported LFS evidence status")
    if not proof.get("uploaded_before_pointer_commit") or not proof.get("independent_empty_cache_download_verified"):
        raise ValueError("LFS upload and independent-download evidence absent")
    by_path = {a["path"]: a for a in manifest["assets"]}
    remote = {a["path"]: a for a in proof["files"]}
    paths = set()
    for a in selected["assets"]:
        p = a["path"]
        if p in paths or p not in by_path or p not in remote:
            raise ValueError(f"missing/duplicate source or LFS evidence: {p}")
        paths.add(p)
        if not p.startswith("data/intake/recovered/2026-10-08/") or not p.endswith((".csv", ".fits")):
            raise ValueError(f"unexpected payload location/format: {p}")
        for key, val in (("sha256", a["sha256"]), ("bytes", a["bytes"])):
            if by_path[p][key] != val:
                raise ValueError(f"manifest {key} conflict: {p}")
        evidence = remote[p]
        if evidence["oid"] != a["sha256"] or evidence["bytes"] != a["bytes"] or evidence["remote_download_sha256"] != a["sha256"]:
            raise ValueError(f"remote LFS digest/size conflict: {p}")
        if any(a[k] is not False for k in ("controlledExecutionEligible", "controlledSupportEligible", "physicalSupportEligible")):
            raise ValueError(f"candidate illegally promoted: {p}")
        if hydrate:
            path = root / p
            if not path.is_file():
                raise ValueError(f"LFS file not hydrated: {p}")
            with path.open("rb") as f:
                if f.read(40).startswith(b"version https://git-lfs.github.com/spec/v1"):
                    raise ValueError(f"LFS pointer without bytes: {p}")
                f.seek(0)
                h = hashlib.sha256()
                count = 0
                for block in iter(lambda: f.read(1024 * 1024), b""):
                    count += len(block)
                    h.update(block)
            if count != a["bytes"] or h.hexdigest() != a["sha256"]:
                raise ValueError(f"hydrated payload corrupted: {p}")
    if not paths:
        raise ValueError("empty selection")
    return len(paths)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--require-local-hydration", action="store_true")
    args = ap.parse_args()
    print(f"Validated {validate(hydrate=args.require_local_hydration)} archival LFS selection records; no scientific admission.")

if __name__ == "__main__":
    main()
