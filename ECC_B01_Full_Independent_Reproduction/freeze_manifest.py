#!/usr/bin/env python3
"""Freeze SHA-256 hashes of all kit files except this manifest itself."""
from __future__ import annotations
import hashlib, json, platform, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"implementation_manifest.json"

def digest(p: Path) -> str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b)
    return h.hexdigest()

files=[]
for p in sorted(ROOT.rglob("*")):
    if not p.is_file() or p==OUT or ".venv" in p.parts or "__pycache__" in p.parts:
        continue
    files.append({"path":str(p.relative_to(ROOT)),"sha256":digest(p),"bytes":p.stat().st_size})

deps={}
for module in ("sympy","numpy","scipy","gmsh","gudhi"):
    try:
        mod=__import__(module)
        deps[module]={"available":True,"version":getattr(mod,"__version__",None)}
    except Exception as exc:
        deps[module]={"available":False,"error":f"{type(exc).__name__}: {exc}"}

payload={
  "manifest_format":"ECC-B01-independent-kit-sha256-v1",
  "generated_at_utc":datetime.now(timezone.utc).isoformat(),
  "note":"The manifest deliberately excludes itself; refresh after edits or reruns.",
  "python":sys.version,
  "platform":platform.platform(),
  "dependencies":deps,
  "freeze_command":"python freeze_manifest.py",
  "files":files,
}
OUT.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
print(f"Wrote {OUT} with {len(files)} file hashes")
