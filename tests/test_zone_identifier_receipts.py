"""Do not silently elevate Zone.Identifier origin hints to scientific dataset proof."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPTS = ROOT / "data/provenance/zone_identifier_receipts_v0.1.json"


def test_zone_receipts_are_distinct_quarantined_source_hints():
    record = json.loads(RECEIPTS.read_text(encoding="utf-8"))
    rows = record["receipts"]
    assert record["observedSidecarCount"] == len(rows)
    names = [row["localName"] for row in rows]
    assert len(names) == len(set(names))
    assert all(row["zoneIdentifierDropboxPath"].endswith(
        row["localName"] + "\uf03aZone.Identifier") for row in rows)
    assert all(row["sourceSha256"] is None and not row["byteEqualityVerified"]
               and not row["upstreamReleaseVerified"]
               and row["status"] == "historical_download_origin_hint_only" for row in rows)
    assert record["admission"] == {
        "executionEligible": False,
        "controlledSupportEligible": False,
        "physicalSupportEligible": False,
    }


def test_historical_sdss_basename_and_sql_copy_divergence():
    record = json.loads(RECEIPTS.read_text(encoding="utf-8"))
    by_name = {r["localName"]: r for r in record["receipts"]}
    sdss = by_name["SDSSDR18_200000.csv"]
    assert sdss["originalDownloadName"] == "MyTable_pmqr771_0.csv"
    assert sdss["renameIndicatedByBasename"] is True
    sql = record["casJobsHistory"]
    assert sql["SQLJobAndExportBindingVerified"] is False
    assert sql["TOPWithoutOrderByNonDeterministic"] is True
    assert sql["rawSDSSSampleGalaxyOnly"] is False
    assert by_name["GZ2.csv"]["originalDownloadName"] == "MyTable_pmqr771.csv"
    assert by_name["MyTable_pmqr771.csv"]["originalDownloadName"] == "MyTable_pmqr771.csv"


def test_xmatch_preserves_job_id_without_publishing_session_parameters():
    record = json.loads(RECEIPTS.read_text(encoding="utf-8"))
    xmatch = [r for r in record["receipts"] if r["sourceService"] == "CDS_XMATCH"]
    assert xmatch
    assert all("jobId=" in r["hostUrlOrJobId"] and "sessionId=" not in r["hostUrlOrJobId"]
               for r in xmatch)
    assert all(r["originalDownloadName"] is None for r in xmatch)
