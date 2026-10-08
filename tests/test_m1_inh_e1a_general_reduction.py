"""Regression gate for the review-only M1-INH-E1a general reduction.

This runs the real generic-metric algebraic certificate with SymPy, but does
not claim external mathematical review or change any scientific registry.
"""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "preregistrations" / "M1-INH-E1" / "derivations"
SCRIPT = DIR / "e1a_general_einstein_reduction.py"
PROOF = DIR / "E1a_general_reduction.md"


def test_e1a_exact_generic_einstein_to_weierstrass_certificate():
    assert SCRIPT.is_file()
    run = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert run.returncode == 0, run.stdout + "\n" + run.stderr
    assert run.stdout.count("PASS ") == 10, run.stdout
    assert "ALL CHECKS PASSED" in run.stdout
    assert "not external review" in run.stdout


def test_e1a_review_boundary_preserves_frozen_protocol():
    protocol = (ROOT / "preregistrations" / "M1-INH-E1" / "protocol.md")
    proof = PROOF.read_text(encoding="utf-8")
    frozen = protocol.read_text(encoding="utf-8")
    assert "## Frozen Weierstrass convention" in frozen
    assert "## M1-INH-E1a" in frozen
    assert "not independently peer-reviewed" in proof
    assert "does not" in proof.lower()
    assert "protocol" in proof.lower()
    assert "M1-INH-E1b" in proof
