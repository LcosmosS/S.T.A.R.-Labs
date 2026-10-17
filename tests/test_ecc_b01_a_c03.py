"""Regression guard for EXP-ECC-B01 Investigator A's C-03 symbolic assertion.

Historical ecc_b01/investigator_a.py and its preliminary report are not changed.
"""
import hashlib
import json
import runpy
import subprocess
import sys
from pathlib import Path

import sympy as sp

SCRIPT = Path(__file__).resolve().parents[1] / "ecc_b01" / "investigator_a_v2.py"


def test_c03_real_zero_predicate_and_injected_nonzero_rejection():
    namespace = runpy.run_path(str(SCRIPT), run_name="ecc_b01_regression")
    predicate = namespace["zero_residual"]
    assert predicate(sp.Integer(0))
    assert predicate(sp.sin(namespace["phi"])**2 + sp.cos(namespace["phi"])**2 - 1)
    assert not predicate(sp.Integer(1))
    assert not predicate(sp.Symbol("incorrect_residual"))
    fixtures = {row["fixture_id"]: row for row in namespace["results"]}
    assert fixtures["C-03"]["observed"] == "0"
    assert fixtures["C-03"]["pass_"] is True
    assert fixtures["C-03-NEG"]["observed"] == "1"
    assert fixtures["C-03-NEG"]["pass_"] is True


def test_versioned_runner_emits_hashed_c03_controls(tmp_path):
    target = tmp_path / "a_v2.json"
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), str(target)],
        check=False, capture_output=True, text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    report = json.loads(target.read_text(encoding="utf-8"))
    assert report["status"] == "PASS"
    assert len(report["results"]) == 16
    assert report["source_sha256"] == hashlib.sha256(SCRIPT.read_bytes()).hexdigest()
    fixtures = {row["fixture_id"]: row for row in report["results"]}
    assert fixtures["C-03"]["pass_"]
    assert fixtures["C-03-NEG"]["pass_"]

