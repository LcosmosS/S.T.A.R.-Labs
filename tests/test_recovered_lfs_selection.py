"""Metadata-gate regression, never loads raw survey data or executes pickles."""
import importlib.util
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("verify_selected_lfs", ROOT / "tools" / "verify_recovered_lfs_selection.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_archival_lfs_selection_metadata():
    assert module.validate(ROOT) == 5

def test_selection_does_not_promote_evidence(tmp_path):
    import json
    f = json.loads((ROOT / module.SELECTION).read_text())
    f["assets"][0]["controlledExecutionEligible"] = True
    (tmp_path / "registry").mkdir()
    (tmp_path / "registry" / "recovered_lfs_selection_v0.1.json").write_text(json.dumps(f))
    for source in (f["sourceManifest"], f["lfsProof"]):
        (tmp_path / source).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / source).write_bytes((ROOT / source).read_bytes())
    with pytest.raises(ValueError, match="promoted"):
        module.validate(tmp_path)
