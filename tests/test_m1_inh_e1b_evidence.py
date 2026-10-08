"""Integrity tests for archived M1-INH-E1b metric-first candidate evidence.

These tests check provenance and scientific boundaries only. They deliberately do
not label the mathematical certificate independently peer reviewed, nor launch
a heavy symbolic proof during the default test suite.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "preregistrations" / "M1-INH-E1" / "evidence" / "metric-first"

SOURCES = {
    "development-history/m1_inh_e1b_metric_first_audit.py":
        "2cea1c169a6080a08d9a6834d3d5a60e7095d38f4ebc9acec5e64126d8ce5a43",
    "development-history/m1_inh_e1b_metric_first_audit_v2.py":
        "f35286d090d4c84c9c9a95ff30226254009c84fa81d52c78074d7802b06640a6",
    "development-history/m1_inh_e1b_metric_first_audit_v3.py":
        "8a7701f2a3d746d3b53068b5b6051772fac64177c05a3219b45c3f77c1f4e51a",
    "m1_inh_e1b_metric_first_audit_v4.py":
        "10ccfa264f475fd7bd6d490c80c8862a174730567ee51c0d759b87939b93e6bb",
}


def test_archived_source_sha256_matches_execution_provenance():
    for relative, expected in SOURCES.items():
        source = EVIDENCE / relative
        assert source.is_file()
        assert hashlib.sha256(source.read_bytes()).hexdigest() == expected


def test_certificates_are_binded_to_exact_source_versions():
    for relative, expected in SOURCES.items():
        certificate = (EVIDENCE / relative).with_suffix(".json")
        data = json.loads(certificate.read_text(encoding="utf-8"))
        assert data["script_sha256"] == expected
        assert data["sympy_version"] == "1.14.0"
        assert "NOT CLAIMED" in data["general_E1a"]
        assert "same M,K,f,Lambda,epsilon,v0,sigma,g2,g3,Delta" in data["elliptic_record"]
        for name in ("S1", "S2"):
            sector = data[name]
            assert sector["Einstein_dust_tensor"].startswith("PASS:")
            assert sector["rank_one_timelike_dust_projector"].startswith("PASS:")
            assert sector["shear_projector_idempotent_rank2"].startswith("PASS:")
        assert data["S1"]["J_identity"] == "0"
        assert "positive" in data["S2"]["J_identity"]


def test_e1b_evidence_remains_explicitly_unreviewed_and_e1a_pending():
    readme = (EVIDENCE / "README.md").read_text(encoding="utf-8")
    next_step = (EVIDENCE / "E1a_handoff.md").read_text(encoding="utf-8")
    provenance = (EVIDENCE / "execution_provenance.md").read_text(encoding="utf-8")
    assert "EXTERNAL_REVIEW_AND_GENERAL_E1a_PENDING" in readme
    assert "NOT EXECUTED" in next_step
    assert "four passing versions are *not* four independent" in readme
    assert "Earlier notebook-cell failures" in provenance


def test_frozen_elliptic_record_has_explicit_common_branch_normalization():
    """The proof must fix the inverse-WP and time origins, not just the cubic."""
    from sympy import Symbol, cancel

    record = (EVIDENCE / "M1-INH-E1b_metric_first_proof_record.md").read_text(
        encoding="utf-8"
    )
    for requirement in (
        "J=(-1/4,1/4)",
        "\\epsilon=0",
        "v_0(z)=\\int_0^\\infty",
        "\\sigma(z)=",
        "\\operatorname{sgn}\\dot\\Phi=+1",
        "\\operatorname{sgn}\\wp'=-1",
        "(n,m)=(0,0)",
        "\\int_{-\\infty}^{X(t,z)}",
        "\\int_0^{u(t,z)}\\Phi",
    ):
        assert requirement in record, f"Missing preregistered branch datum: {requirement}"

    # Frozen X=-2*xi/M and Q(X)=1-2*M*X**3 must give the
    # nondegenerate Weierstrass cubic with g2=0, g3=-M**2/4.
    mass = Symbol("M", positive=True)
    xi = Symbol("xi", positive=True)
    X = -2 * xi / mass
    Q = 1 - 2 * mass * X**3
    assert cancel((mass**2 / 4) * Q - (4 * xi**3 + mass**2 / 4)) == 0

    # This is a documentary and algebraic regression check, not an
    # independent numerical assessment of the Weierstrass inverse.
