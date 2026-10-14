"""Tests for independent dataset-source verification infrastructure."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "independent_dataset_verification.py"
MATRIX = ROOT / "verification/datasets/dataset_verification_matrix_v0.1.csv"
HISTORICAL_SQL = (
    ROOT
    / "verification/datasets/casjobs/DATA-SDSS18-200K_historical_recovered.sql"
)
HISTORICAL_RERUN_SQL = (
    ROOT
    / "verification/datasets/casjobs/DATA-SDSS18-200K_historical_rerun.sql"
)
DETERMINISTIC_SQL = (
    ROOT
    / "verification/datasets/casjobs/DATA-SDSS18-200K_deterministic_probe.sql"
)
MEMBERSHIP_SQL = (
    ROOT
    / "verification/datasets/casjobs/DATA-SDSS18-200K_membership_backcheck.sql"
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


def test_exact_independent_review_set_is_locked():
    report = _module().static_report()

    assert set(report["needs_independent_verification_ids"]) == {
        "DATA-SDSS18-200K",
        "DATA-MANGA-HI-ALL",
        "DATA-PROVENANCE-ALL",
        "DATA-SFR-MANGA-PIP3D",
        "DATA-VIZIER-ALFALFA100",
        "DATA-COSMIC-ENV",
        "DATA-PHYS-CONSTRAINTS",
        "DATA-ECC-THEORY",
    }
    assert report["source_locked_controlled_ids"] == ["DATA-ARITHMETIC"]


def test_matrix_covers_all_canonical_dataset_ids_once():
    with MATRIX.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))

    ids = [row["Dataset_ID"] for row in rows]
    assert len(ids) == 9
    assert len(ids) == len(set(ids))


def test_duplicate_provenance_rows_are_rejected(monkeypatch):
    module = _module()
    original = module.canonical_provenance_rows()
    monkeypatch.setattr(
        module,
        "canonical_provenance_rows",
        lambda: original + [dict(original[0])],
    )

    with pytest.raises(ValueError, match="duplicate canonical provenance"):
        module.static_report()


def test_invalid_provenance_status_is_rejected(monkeypatch):
    module = _module()
    rows = [dict(row) for row in module.canonical_provenance_rows()]
    rows[0]["Provenance_Status"] = "verifed"
    monkeypatch.setattr(module, "canonical_provenance_rows", lambda: rows)

    with pytest.raises(ValueError, match="unrecognized canonical provenance"):
        module.static_report()


def test_historical_casjobs_query_preserves_recovered_predicates():
    module = _module()
    sql = module.sql_code(HISTORICAL_SQL.read_text(encoding="utf-8")).upper()

    assert "SELECT TOP 200000" in sql
    assert "JOIN SPECOBJ AS S" in sql
    assert "S.BESTOBJID = P.OBJID" in sql
    assert "P.U BETWEEN 0 AND 19.6" in sql
    assert "G BETWEEN 0 AND 20" in sql
    assert "ORDER BY" not in sql
    assert "CLASS = 'GALAXY'" not in sql
    assert "CLASS='GALAXY'" not in sql


def test_historical_rerun_wrapper_is_rerunnable_but_still_unordered():
    module = _module()
    sql = module.sql_code(
        HISTORICAL_RERUN_SQL.read_text(encoding="utf-8")
    ).upper()

    assert "DROP TABLE MYDB.MYTABLE" in sql
    assert "SELECT TOP 200000" in sql
    assert "G BETWEEN 0 AND 20" in sql
    assert "ORDER BY" not in sql


def test_deterministic_probe_is_rerunnable_and_ordered():
    module = _module()
    sql = module.sql_code(DETERMINISTIC_SQL.read_text(encoding="utf-8")).upper()

    assert "DROP TABLE MYDB.STAR_SDSS18_200K_DETERMINISTIC_PROBE" in sql
    assert "SELECT TOP 200000" in sql
    assert "P.U BETWEEN 0 AND 19.6" in sql
    assert "P.G BETWEEN 0 AND 20" in sql
    assert "ORDER BY" in sql
    assert "P.OBJID ASC" in sql
    assert "S.SPECOBJID ASC" in sql


def test_membership_backcheck_locks_pair_relation_and_predicates():
    module = _module()
    sql = module.sql_code(MEMBERSHIP_SQL.read_text(encoding="utf-8")).upper()

    assert "MYDB.STAR_SDSS18_200K_IDS" in sql
    assert "S.SPECOBJID = H.SPECOBJID" in sql
    assert "S.BESTOBJID = P.OBJID" in sql
    assert "P.U BETWEEN 0 AND 19.6" in sql
    assert "P.G BETWEEN 0 AND 20" in sql


def test_vizier_request_locks_shape_identifiers_coordinates_and_limits():
    spec = json.loads(VIZIER.read_text(encoding="utf-8"))

    assert spec["dataset_id"] == "DATA-VIZIER-ALFALFA100"
    assert spec["catalogue"] == "J/ApJ/861/49/table2"
    assert "-out.max=unlimited" in spec["url"]
    assert "-out.all=1" in spec["url"]
    assert spec["expected_rows"] == 31502
    assert spec["expected_fields"] == 25
    assert spec["expected_frozen_bytes"] == 10981088
    assert spec["max_response_bytes"] < 256 * 1024 * 1024
    assert spec["coordinate_contract"]["RAJ2000"] == {
        "ucd": "pos.eq.ra;meta.main",
        "ref": "J2000",
    }
    assert spec["coordinate_contract"]["DEJ2000"] == {
        "ucd": "pos.eq.dec;meta.main",
        "ref": "J2000",
    }
    assert spec["expected_invariants"]["partial_optical_coordinate_rows"] == 0


def test_casjobs_profile_rejects_duplicates_and_predicate_violations(tmp_path):
    module = _module()
    path = tmp_path / "bad.csv"
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(module.SDSS_COLUMNS)
        good = [
            "1", "10", "10", "10", "10", "9", "8", "7", "1", "1",
            "1", "1", "2", "GALAXY", "0.01", "1", "1", "1",
        ]
        writer.writerow(good)
        bad = good.copy()
        bad[4] = "25"
        writer.writerow(bad)

    profile = module._read_csv_profile(path)

    assert profile["duplicate_pair_rows"] == 1
    assert profile["predicate_violations"] == 1
    assert profile["semantic_valid"] is False


def test_live_source_failures_are_recorded_per_source(monkeypatch):
    module = _module()
    pins = {
        dataset_id: {"url": "x", "sha256": "0" * 64, "bytes": 1}
        for dataset_id in module.PUBLIC_PUBLISHER_IDS
    }

    calls = []

    def fake_publisher(dataset_id, source, preserve_dir):
        calls.append(dataset_id)
        if dataset_id == module.PUBLIC_PUBLISHER_IDS[0]:
            raise RuntimeError("boom")
        return {"dataset_id": dataset_id, "passed": True}

    monkeypatch.setattr(module, "verify_publisher_source", fake_publisher)
    monkeypatch.setattr(
        module,
        "verify_vizier_live",
        lambda preserve_dir: {
            "dataset_id": "DATA-VIZIER-ALFALFA100",
            "passed": True,
        },
    )

    receipt = module.verify_live_public_sources(pins, None)

    assert calls == list(module.PUBLIC_PUBLISHER_IDS)
    assert len(receipt["results"]) == 4
    assert receipt["results"][0]["passed"] is False
    assert receipt["all_passed"] is False


def test_receipt_write_is_atomic_non_overwriting(tmp_path):
    module = _module()
    path = tmp_path / "receipt.json"

    module.write_receipt(path, {"version": 1})
    with pytest.raises(FileExistsError):
        module.write_receipt(path, {"version": 2})

    assert json.loads(path.read_text(encoding="utf-8")) == {"version": 1}


def test_receipt_path_cannot_replace_registry_or_export(tmp_path):
    module = _module()
    export = tmp_path / "export.csv"
    export.write_text("x\n", encoding="utf-8")

    with pytest.raises(ValueError, match="protected input"):
        module._validate_receipt_path(module.DATASETS)
    with pytest.raises(ValueError, match="protected input"):
        module._validate_receipt_path(export, casjobs_export=export)


def test_static_verifier_never_promotes_registry_state():
    report = _module().static_report()

    assert report["automatic_registry_promotion"] is False


def test_live_vizier_parser_is_hardened_and_streaming():
    source = SCRIPT.read_text(encoding="utf-8")
    requirements = (
        ROOT / "verification" / "datasets" / "requirements.txt"
    ).read_text(encoding="utf-8")

    assert "xml.etree.ElementTree" not in source
    assert "from defusedxml import ElementTree as SafeET" in source
    assert "SafeET.iterparse" in source
    assert "defusedxml==0.7.1" in requirements
