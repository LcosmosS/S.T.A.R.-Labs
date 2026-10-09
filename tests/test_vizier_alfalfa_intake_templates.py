"""Require ALFALFA candidate templates to match existing registries, without admitting them."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "research/acquisition/vizier_alfalfa100"

def records(path):
    with path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source, strict=True)
        return list(reader.fieldnames or []), list(reader)

def test_vizier_candidate_templates_match_operational_headers_but_are_not_operational():
    specs = [
        ("dataset_registry_v0.1.csv", "dataset_registry_row.template.csv"),
        ("data_provenance_registry_v0.1.csv", "data_provenance_registry_row.template.csv"),
    ]
    for canonical, template in specs:
        canonical_fields, canonical_rows = records(ROOT / "registry" / canonical)
        fields, rows = records(INTAKE / template)
        assert fields == canonical_fields
        assert len(rows) == 1
        assert all(None not in row and all(value is not None for value in row.values()) for row in rows)
        assert rows[0]["Dataset_ID"] == "DATA-VIZIER-ALFALFA100"
        assert not any(row["Dataset_ID"] == "DATA-VIZIER-ALFALFA100" for row in canonical_rows)
    _, dataset = records(INTAKE / "dataset_registry_row.template.csv")
    _, source = records(INTAKE / "data_provenance_registry_row.template.csv")
    ds, pv = dataset[0], source[0]
    assert (ds["Status"], ds["Provenance_Status"], ds["Achieved_Evidence_Status"]) == ("planned", "unknown", "unknown")
    assert all(ds[field] == "false" for field in (
        "Controlled_Execution_Eligible", "Controlled_Support_Eligible", "Physical_Support_Eligible"
    ))
    assert (pv["Provenance_Status"], pv["Evidence_Status"]) == ("unknown", "unknown")
    assert "PENDING_" in pv["Integrity_Check"]
    assert pv["Match_Tolerance"] == "not_applicable"
