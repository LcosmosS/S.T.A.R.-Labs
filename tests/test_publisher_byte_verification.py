"""Verify provenance-only publisher-byte transitions remain fail closed."""
from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "data/provenance/publisher_byte_verification_2026-10-08.json"
HI_SHA = "0f51e1852f7103bd9af9699213a7548a7e6b9969ab1256ec86df04352ddec8f5"
HI_PATH = f"data/intake/recovered/2026-10-08/{HI_SHA}.fits"


def _rows(name: str, key: str) -> dict[str, dict[str, str]]:
    with (ROOT / "registry" / name).open(encoding="utf-8", newline="") as stream:
        return {row[key]: row for row in csv.DictReader(stream, strict=True)}


def test_hi_publisher_bytes_match_real_lfs_object_and_only_provenance_advances():
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    record = next(row for row in receipt["datasets"] if row["dataset_id"] == "DATA-MANGA-HI-ALL")
    dataset = _rows("dataset_registry_v0.1.csv", "Dataset_ID")["DATA-MANGA-HI-ALL"]
    provenance = _rows("data_provenance_registry_v0.1.csv", "Dataset_ID")["DATA-MANGA-HI-ALL"]

    pointer = subprocess.check_output(
        ["git", "show", f"HEAD:{HI_PATH}"], cwd=ROOT, text=True
    )
    assert f"oid sha256:{HI_SHA}" in pointer
    assert "size 1584000" in pointer
    assert record["publisher"]["sha256"] == HI_SHA
    assert record["comparison"] == {
        "publisher_equals_recovered_copy": True,
        "publisher_equals_repository_lfs": True,
    }
    assert dataset["Status"] == "planned"
    assert dataset["Provenance_Status"] == provenance["Provenance_Status"] == "verified"
    assert dataset["Achieved_Evidence_Status"] == provenance["Evidence_Status"] == "unknown"
    assert all(dataset[field] == "false" for field in (
        "Controlled_Execution_Eligible",
        "Controlled_Support_Eligible",
        "Physical_Support_Eligible",
    ))


def test_pipe3d_match_is_recorded_without_repository_or_registry_promotion():
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    record = next(row for row in receipt["datasets"] if row["dataset_id"] == "DATA-SFR-MANGA-PIP3D")
    dataset = _rows("dataset_registry_v0.1.csv", "Dataset_ID")["DATA-SFR-MANGA-PIP3D"]
    provenance = _rows("data_provenance_registry_v0.1.csv", "Dataset_ID")["DATA-SFR-MANGA-PIP3D"]

    assert record["publisher"]["sha256"] == "ac714809044c02dcb2cc8b5007d02981d9316c34dc398a79f4c07bde4d3496fc"
    assert record["repository_lfs"]["present"] is False
    assert dataset["Provenance_Status"] == provenance["Provenance_Status"] == "unknown"
    assert dataset["Achieved_Evidence_Status"] == provenance["Evidence_Status"] == "unknown"
    assert all(dataset[field] == "false" for field in (
        "Controlled_Execution_Eligible",
        "Controlled_Support_Eligible",
        "Physical_Support_Eligible",
    ))


def test_arithmetic_reverification_matches_existing_canonical_identity():
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    record = receipt["arithmetic_reverification"]
    assert record["commit"] == "25cec5ecfec8b9f016eb1631ac633194c2bed39f"
    assert record["sha256"] == "259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968"
    assert record["git_blob_sha1"] == "baab5801d7f81e1d5c44f5eb5acf4f1e100bc90b"
    assert record["rows"] == 64687
    assert record["matches_canonical_registry"] is True
