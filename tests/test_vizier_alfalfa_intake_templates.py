"""Require ALFALFA provenance intake while web admission remains pending."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "research/acquisition/vizier_alfalfa100"

def records(path):
    with path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source, strict=True)
        return list(reader.fieldnames or []), list(reader)

def test_vizier_templates_preserve_pre_acquisition_design_and_operational_row_is_conservative():
    """Keep intake templates unchanged and live ALFALFA eligibility disabled."""
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
        operational = [row for row in canonical_rows if row["Dataset_ID"] == "DATA-VIZIER-ALFALFA100"]
        assert len(operational) == 1
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

    _, live_datasets = records(ROOT / "registry/dataset_registry_v0.1.csv")
    _, live_provenance = records(ROOT / "registry/data_provenance_registry_v0.1.csv")
    live_ds = next(row for row in live_datasets if row["Dataset_ID"] == "DATA-VIZIER-ALFALFA100")
    live_pv = next(row for row in live_provenance if row["Dataset_ID"] == "DATA-VIZIER-ALFALFA100")
    assert live_ds["Status"] == "planned"
    assert live_ds["Provenance_Status"] == live_pv["Provenance_Status"] == "verified"
    assert live_ds["Achieved_Evidence_Status"] == live_pv["Evidence_Status"] == "unknown"
    assert all(live_ds[field] == "false" for field in (
        "Controlled_Execution_Eligible", "Controlled_Support_Eligible", "Physical_Support_Eligible"
    ))
    assert "654217f9b3414856c1a8b09071c81eb834a0b0fbc6ec3aea9777e01fdaea1079" in live_pv["Integrity_Check"]
