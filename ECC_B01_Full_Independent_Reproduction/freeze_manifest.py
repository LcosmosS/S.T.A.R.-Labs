#!/usr/bin/env python3
"""Create a new SHA-256 inventory without overwriting historical manifests."""
from __future__ import annotations
import argparse, hashlib, json, platform, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def skipped(path: Path, target: Path) -> bool:
    rel = path.relative_to(ROOT)
    return (path == target or path.suffix in {".pyc", ".pyo"}
            or any(part in {".venv", "venv", "__pycache__", "runs"} for part in rel.parts)
            or any(".staging-" in part for part in rel.parts))

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", help="New manifest path; defaults to a unique timestamped file")
    args = parser.parse_args()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    target = Path(args.out).expanduser() if args.out else Path(f"implementation_manifest_{stamp}.json")
    if not target.is_absolute():
        target = ROOT / target
    target = target.resolve()
    if target.exists():
        parser.error(f"refusing to overwrite existing manifest: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    files = []
    for path in sorted(ROOT.rglob("*")):
        if path.is_file() and not skipped(path, target):
            files.append({"path": str(path.relative_to(ROOT)), "sha256": digest(path), "bytes": path.stat().st_size})
    dependencies = {}
    for module in ("sympy", "numpy", "scipy", "gmsh", "gudhi"):
        try:
            imported = __import__(module)
            dependencies[module] = {"available": True, "version": getattr(imported, "__version__", None)}
        except Exception as exc:
            dependencies[module] = {"available": False, "error": f"{type(exc).__name__}: {exc}"}
    payload = {
        "manifest_format": "ECC-B01-independent-kit-sha256-v2",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "note": "New package inventory. The historical implementation_manifest.json is preserved. Run outputs under runs/ are separate snapshots.",
        "python": sys.version, "platform": platform.platform(), "dependencies": dependencies,
        "freeze_command": f"python freeze_manifest.py --out {target}", "files": files,
    }
    with target.open("x", encoding="utf-8") as stream:
        json.dump(payload, stream, indent=2)
        stream.write("\n")
    print(f"Wrote new manifest {target} with {len(files)} file hashes")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
