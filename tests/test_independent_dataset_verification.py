"""Tests for independent dataset-source verification infrastructure."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "independent_dataset_verification.py"
MATRIX = ROOT / "verification/datasets/dataset_verification_matrix_v0.1.csv"
HISTORICAL_SQL = (
    ROOT
    / "verification/datasets/casjobs/DATA-SDSS18-200K_historical_recovered.sql"
)
DETERMINISTIC_SQL = (
    ROOT
    / "verification/datasets/casjobs/DATA-SDSS18-200K_deterministic_probe.sql"
)
VIZIER = (
    ROOT
    / "verification/datasets/vizier/DATA-VIZIER-ALFALFA100_request.json"
)


def _module():
    spec = importlib.util.spec_from_file_location("dataset_verifier", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_canonical_dataset_census_and_unknown_count():
    report = _module().static_report()

    assert report["canonical_dataset_count"] == 9
    assert report["source_provenance_unknown_count"] == 4
    assert report["source_provenance_unknown_ids"] == [
        "DATA-ECC-THEORY",
        "DATA-PHYS-CONSTRAINTS",
        "DATA-PROVENANCE-ALL",
        "DATA-SDSS18-200K",
    ]


def test_eight_of_nine_need_dataset_level_independent_review():
    report = _module().static_report()

    assert report["needs_independent_verification_count"] == 8
    assert report["source_locked_controlled_ids"] == ["DATA-ARITHMETIC"]


def test_matrix_covers_all_canonical_dataset_ids_once():
    with MATRIX.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))

    ids = [row["Dataset_ID"] for row in rows]
    assert len(ids) == 9
    assert len(ids) == len(set(ids))


def test_historical_casjobs_query_preserves_nondeterminism():
    sql = HISTORICAL_SQL.read_text(encoding="utf-8").upper()

    assert "SELECT TOP 200000" in sql
    assert "JOIN SPECOBJ AS S" in sql
    assert "S.BESTOBJID = P.OBJID" in sql
    assert "ORDER BY" not in sql
    assert "CLASS = 'GALAXY'" not in sql
    assert "CLASS='GALAXY'" not in sql


def test_deterministic_probe_is_explicitly_ordered():
    sql = DETERMINISTIC_SQL.read_text(encoding="utf-8").upper()

    assert "SELECT TOP 200000" in sql
    assert "ORDER BY" in sql
    assert "P.OBJID ASC" in sql
    assert "S.SPECOBJID ASC" in sql
    assert "MYDB.STAR_SDSS18_200K_DETERMINISTIC_PROBE" in sql


def test_vizier_request_is_complete_and_unbounded():
    spec = json.loads(VIZIER.read_text(encoding="utf-8"))

    assert spec["dataset_id"] == "DATA-VIZIER-ALFALFA100"
    assert spec["catalogue"] == "J/ApJ/861/49/table2"
    assert "-out.max=unlimited" in spec["url"]
    assert "-out.all=1" in spec["url"]
    assert spec["expected_rows"] == 31502
    assert spec["expected_fields"] == 25


def test_static_verifier_never_promotes_registry_state():
    report = _module().static_report()

    assert report["automatic_registry_promotion"] is False
