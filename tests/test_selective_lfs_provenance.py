import subprocess
import sys
from pathlib import Path

def test_selective_lfs_provenance_fail_closed():
    """Verify the provenance CLI succeeds and reports zero newly committed assets."""
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run([sys.executable, str(root / "tools/validate_selective_lfs.py")],
                            cwd=root, text=True, capture_output=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "0 newly committed" in result.stdout
