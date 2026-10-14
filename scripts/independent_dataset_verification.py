#!/usr/bin/env python3
"""Independent dataset-source verification helpers.

Default execution is static/read-only. Network access occurs only with the
explicit --live-public-sources flag. This script never mutates canonical
registries or eligibility flags.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import tempfile
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "verification/datasets/dataset_verification_matrix_v0.1.csv"
DATASETS = ROOT / "registry/dataset_registry_v0.1.csv"
PROVENANCE = ROOT / "registry/data_provenance_registry_v0.1.csv"
HISTORICAL_SQL = (
    ROOT
    / "verification/datasets/casjobs/DATA-SDSS18-200K_historical_recovered.sql"
)
DETERMINISTIC_SQL = (
    ROOT
    / "verification/datasets/casjobs/DATA-SDSS18-200K_deterministic_probe.sql"
)
VIZIER_REQUEST = (
    ROOT
    / "verification/datasets/vizier/DATA-VIZIER-ALFALFA100_request.json"
)
FROZEN_SDSS = (
    ROOT
    / "data/intake/recovered/2026-10-08/"
    "9dca2008683fde4b0f7a90af5de85ee846a30a47f6f6fae3968c83dea06fa5d2.csv"
)

SDSS_COLUMNS = [
    "objid",
    "ra",
    "dec",
    "u",
    "g",
    "r",
    "i",
    "z",
    "run",
    "rerun",
    "camcol",
    "field",
    "specobjid",
    "class",
    "redshift",
    "plate",
    "mjd",
    "fiberid",
]

PUBLIC_PUBLISHER_SOURCES = {
    "DATA-MANGA-HI-ALL": {
        "url": (
            "https://data.sdss.org/sas/dr17/env/MANGA_HI/"
            "v2_0_1/mangaHIall.fits"
        ),
        "sha256": "0f51e1852f7103bd9af9699213a7548a7e6b9969ab1256ec86df04352ddec8f5",
        "bytes": 1_584_000,
    },
    "DATA-SFR-MANGA-PIP3D": {
        "url": (
            "https://data.sdss.org/sas/dr17/env/MANGA_PIPE3D/"
            "v3_1_1/3.1.1/SDSS17Pipe3D_v3_1_1.fits"
        ),
        "sha256": "ac714809044c02dcb2cc8b5007d02981d9316c34dc398a79f4c07bde4d3496fc",
        "bytes": 55_889_280,
    },
    "DATA-COSMIC-ENV": {
        "url": (
            "https://data.sdss.org/sas/dr17/env/MANGA_GEMA/"
            "2.0.2/GEMA_2.0.2.fits"
        ),
        "sha256": "244e9286f225b9e1dbef73bb93e1101d840a2a62ec5dabf3aa16ec88cfef1597",
        "bytes": 7_223_040,
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_lfs_pointer(path: Path) -> bool:
    if not path.is_file():
        return False
    with path.open("rb") as stream:
        return stream.read(64).startswith(
            b"version https://git-lfs.github.com/spec/v1"
        )


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def canonical_dataset_rows() -> list[dict[str, str]]:
    return [row for row in rows(DATASETS) if row["Dataset_ID"].startswith("DATA-")]


def canonical_provenance_rows() -> list[dict[str, str]]:
    return [row for row in rows(PROVENANCE) if row["Dataset_ID"].startswith("DATA-")]


def matrix_rows() -> list[dict[str, str]]:
    return rows(MATRIX)


def _bool_text(value: str) -> bool:
    value = value.strip().lower()
    if value == "true":
        return True
    if value == "false":
        return False
    raise ValueError(f"invalid boolean text: {value!r}")


def sql_code(text: str) -> str:
    """Return SQL text with -- line comments removed for clause checks."""
    return "\n".join(line.split("--", 1)[0] for line in text.splitlines())


def static_report() -> dict:
    datasets = canonical_dataset_rows()
    provenance = canonical_provenance_rows()
    matrix = matrix_rows()

    dataset_ids = [row["Dataset_ID"] for row in datasets]
    provenance_ids = [row["Dataset_ID"] for row in provenance]
    matrix_ids = [row["Dataset_ID"] for row in matrix]

    if len(dataset_ids) != len(set(dataset_ids)):
        raise ValueError("duplicate canonical Dataset_ID")
    if set(dataset_ids) != set(provenance_ids):
        raise ValueError("canonical dataset/provenance IDs differ")
    if set(dataset_ids) != set(matrix_ids):
        raise ValueError("independent-verification matrix does not cover canonical datasets")

    by_provenance = {row["Dataset_ID"]: row for row in provenance}
    by_dataset = {row["Dataset_ID"]: row for row in datasets}

    for row in matrix:
        dataset_id = row["Dataset_ID"]
        actual_status = by_provenance[dataset_id]["Provenance_Status"]
        if row["Canonical_Provenance_Status"] != actual_status:
            raise ValueError(
                f"{dataset_id}: matrix provenance status drift "
                f"({row['Canonical_Provenance_Status']} != {actual_status})"
            )
        # This verification package is not an activation mechanism.
        if by_dataset[dataset_id]["Controlled_Support_Eligible"] != "false":
            raise ValueError(f"{dataset_id}: controlled support unexpectedly enabled")
        if by_dataset[dataset_id]["Physical_Support_Eligible"] != "false":
            raise ValueError(f"{dataset_id}: physical support unexpectedly enabled")

    unknown = sorted(
        row["Dataset_ID"]
        for row in provenance
        if row["Provenance_Status"] == "unknown"
    )
    needs_independent = sorted(
        row["Dataset_ID"]
        for row in matrix
        if _bool_text(row["Needs_Independent_Verification"])
    )

    historical_sql = HISTORICAL_SQL.read_text(encoding="utf-8")
    deterministic_sql = DETERMINISTIC_SQL.read_text(encoding="utf-8")
    historical_upper = sql_code(historical_sql).upper()
    deterministic_upper = sql_code(deterministic_sql).upper()

    required_sql = [
        "SELECT TOP 200000",
        "FROM PHOTOOBJ AS P",
        "JOIN SPECOBJ AS S",
        "S.BESTOBJID = P.OBJID",
        "P.U BETWEEN 0 AND 19.6",
    ]
    for token in required_sql:
        if token not in historical_upper:
            raise ValueError(f"historical CasJobs SQL missing {token}")
        if token not in deterministic_upper:
            raise ValueError(f"deterministic CasJobs SQL missing {token}")
    if "ORDER BY" in historical_upper:
        raise ValueError("historical SQL must preserve the no-ORDER-BY condition")
    if "ORDER BY" not in deterministic_upper:
        raise ValueError("deterministic probe must have ORDER BY")
    if "CLASS = 'GALAXY'" in historical_upper or "CLASS='GALAXY'" in historical_upper:
        raise ValueError("historical SQL was silently changed to galaxy-only")

    vizier = json.loads(VIZIER_REQUEST.read_text(encoding="utf-8"))
    if vizier["dataset_id"] != "DATA-VIZIER-ALFALFA100":
        raise ValueError("VizieR request has wrong dataset ID")
    if vizier["catalogue"] != "J/ApJ/861/49/table2":
        raise ValueError("VizieR catalogue identifier drift")
    if vizier["expected_rows"] != 31_502 or vizier["expected_fields"] != 25:
        raise ValueError("VizieR expected shape drift")

    return {
        "schema_version": "star-independent-dataset-verification-static-v0.1",
        "generated_at_utc": utc_now(),
        "canonical_dataset_count": len(dataset_ids),
        "canonical_dataset_ids": sorted(dataset_ids),
        "source_provenance_unknown_count": len(unknown),
        "source_provenance_unknown_ids": unknown,
        "needs_independent_verification_count": len(needs_independent),
        "needs_independent_verification_ids": needs_independent,
        "source_locked_controlled_ids": sorted(
            row["Dataset_ID"]
            for row in matrix
            if row["Independent_Status"] == "source_locked_controlled"
        ),
        "casjobs": {
            "historical_sql": HISTORICAL_SQL.relative_to(ROOT).as_posix(),
            "historical_order_by_present": False,
            "deterministic_probe_sql": DETERMINISTIC_SQL.relative_to(ROOT).as_posix(),
            "deterministic_order_by_present": True,
            "historical_exact_membership_reproducible": False,
        },
        "vizier": {
            "request": VIZIER_REQUEST.relative_to(ROOT).as_posix(),
            "catalogue": vizier["catalogue"],
            "expected_rows": vizier["expected_rows"],
            "expected_fields": vizier["expected_fields"],
        },
        "automatic_registry_promotion": False,
    }


def _download_to_temp(url: str) -> tuple[Path, str, int]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "STAR-Labs-independent-dataset-verifier/0.1"},
    )
    digest = hashlib.sha256()
    count = 0
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp_path = Path(temp.name)
    try:
        with urllib.request.urlopen(request, timeout=120) as response, temp:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                digest.update(chunk)
                count += len(chunk)
                temp.write(chunk)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise
    return temp_path, digest.hexdigest(), count


def verify_publisher_source(dataset_id: str, source: dict) -> dict:
    temp_path, digest, size = _download_to_temp(source["url"])
    try:
        return {
            "dataset_id": dataset_id,
            "method": "publisher_https_refetch",
            "url": source["url"],
            "download_sha256": digest,
            "download_bytes": size,
            "expected_sha256": source["sha256"],
            "expected_bytes": source["bytes"],
            "sha256_match": digest == source["sha256"],
            "size_match": size == source["bytes"],
            "passed": digest == source["sha256"] and size == source["bytes"],
        }
    finally:
        temp_path.unlink(missing_ok=True)


def local_name(element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def verify_vizier_live() -> dict:
    try:
        from defusedxml import ElementTree as SafeET
    except ImportError as exc:
        raise RuntimeError(
            "live VizieR verification requires defusedxml; install "
            "verification/datasets/requirements.txt"
        ) from exc

    spec = json.loads(VIZIER_REQUEST.read_text(encoding="utf-8"))
    temp_path, digest, size = _download_to_temp(spec["url"])
    try:
        root = SafeET.parse(temp_path).getroot()
        fields = [
            dict(element.attrib)
            for element in root.iter()
            if local_name(element) == "FIELD"
        ]
        table_rows = [
            [
                (child.text or "").strip()
                for child in element
                if local_name(child) == "TD"
            ]
            for element in root.iter()
            if local_name(element) == "TR"
        ]
        if any(len(row) != len(fields) for row in table_rows):
            raise ValueError("live VOTable row width differs from FIELD count")

        names = [field.get("name", "") for field in fields]
        required = set(spec["required_fields"])
        missing = sorted(required - set(names))
        by_name = {name: index for index, name in enumerate(names)}

        agcs = [row[by_name["AGC"]] for row in table_rows] if not missing else []
        duplicates = len(agcs) - len(set(agcs)) if agcs else None

        optical_missing = None
        quality = {}
        if not missing:
            optical_missing = sum(
                1
                for row in table_rows
                if not row[by_name["RAO"]] and not row[by_name["DEO"]]
            )
            quality = dict(
                sorted(
                    Counter(row[by_name["HI"]] for row in table_rows).items()
                )
            )

        expected = spec["expected_invariants"]
        semantic_match = (
            len(table_rows) == spec["expected_rows"]
            and len(fields) == spec["expected_fields"]
            and not missing
            and duplicates == expected["duplicate_agc_ids"]
            and optical_missing == expected["paired_missing_optical_coordinates"]
            and quality == expected["hi_quality_code_counts"]
        )
        raw_match = digest == spec["expected_frozen_sha256"]

        return {
            "dataset_id": spec["dataset_id"],
            "method": "vizier_votable_refetch",
            "url": spec["url"],
            "download_sha256": digest,
            "download_bytes": size,
            "expected_frozen_sha256": spec["expected_frozen_sha256"],
            "raw_sha256_match": raw_match,
            "rows": len(table_rows),
            "fields": len(fields),
            "missing_required_fields": missing,
            "duplicate_agc_ids": duplicates,
            "paired_missing_optical_coordinates": optical_missing,
            "hi_quality_code_counts": quality,
            "semantic_invariants_match": semantic_match,
            "passed": raw_match and semantic_match,
            "disposition": (
                "byte_and_semantic_match"
                if raw_match and semantic_match
                else "requires_manual_review"
            ),
        }
    finally:
        temp_path.unlink(missing_ok=True)


def verify_live_public_sources() -> dict:
    results = [
        verify_publisher_source(dataset_id, source)
        for dataset_id, source in PUBLIC_PUBLISHER_SOURCES.items()
    ]
    results.append(verify_vizier_live())
    return {
        "schema_version": "star-independent-live-source-receipt-v0.1",
        "generated_at_utc": utc_now(),
        "results": results,
        "all_passed": all(item["passed"] for item in results),
        "automatic_registry_promotion": False,
    }


def _read_csv_profile(path: Path) -> tuple[list[str], int, Counter, int, set[tuple[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != SDSS_COLUMNS:
            raise ValueError(
                f"CasJobs export header mismatch: {reader.fieldnames!r}"
            )
        classes: Counter = Counter()
        negative_redshift = 0
        pairs: set[tuple[str, str]] = set()
        row_count = 0
        for row in reader:
            row_count += 1
            classes[row["class"]] += 1
            try:
                if float(row["redshift"]) < 0:
                    negative_redshift += 1
            except ValueError:
                pass
            pairs.add((row["objid"], row["specobjid"]))
    return reader.fieldnames or [], row_count, classes, negative_redshift, pairs


def verify_casjobs_export(path: Path, mode: str) -> dict:
    path = path.resolve()
    if not path.is_file():
        raise ValueError(f"CasJobs export is missing: {path}")

    header, row_count, classes, negative_redshift, pairs = _read_csv_profile(path)
    result = {
        "schema_version": "star-independent-casjobs-receipt-v0.1",
        "generated_at_utc": utc_now(),
        "mode": mode,
        "export_path": str(path),
        "export_sha256": sha256_file(path),
        "export_bytes": path.stat().st_size,
        "rows": row_count,
        "columns": header,
        "class_counts": dict(sorted(classes.items())),
        "negative_redshift_rows": negative_redshift,
        "unique_objid_specobjid_pairs": len(pairs),
        "schema_match": header == SDSS_COLUMNS,
        "row_count_match": row_count == 200_000,
        "historical_exact_membership_reproducible": False,
        "automatic_registry_promotion": False,
    }

    if FROZEN_SDSS.is_file() and not is_lfs_pointer(FROZEN_SDSS):
        _, frozen_rows, frozen_classes, frozen_negative, frozen_pairs = _read_csv_profile(
            FROZEN_SDSS
        )
        intersection = len(pairs & frozen_pairs)
        union = len(pairs | frozen_pairs)
        result["frozen_comparison"] = {
            "frozen_sha256": sha256_file(FROZEN_SDSS),
            "frozen_rows": frozen_rows,
            "frozen_class_counts": dict(sorted(frozen_classes.items())),
            "frozen_negative_redshift_rows": frozen_negative,
            "pair_intersection": intersection,
            "pair_union": union,
            "pair_jaccard": intersection / union if union else 1.0,
            "byte_identical": result["export_sha256"] == sha256_file(FROZEN_SDSS),
        }
    else:
        result["frozen_comparison"] = {
            "available": False,
            "reason": "frozen Git LFS object is absent or not hydrated",
        }

    result["passed"] = result["schema_match"] and result["row_count_match"]
    return result


def markdown(report: dict) -> str:
    lines = [
        "# Independent dataset verification",
        "",
        f"- Canonical datasets: **{report['canonical_dataset_count']}**",
        (
            "- Canonical source provenance still `unknown`: "
            f"**{report['source_provenance_unknown_count']}**"
        ),
        (
            "- Datasets needing dataset-level independent verification/review: "
            f"**{report['needs_independent_verification_count']}**"
        ),
        (
            "- Already source-locked at controlled provenance: "
            + ", ".join(report["source_locked_controlled_ids"])
        ),
        "",
        "## Source-provenance unknown",
        "",
    ]
    lines.extend(
        f"- `{dataset_id}`"
        for dataset_id in report["source_provenance_unknown_ids"]
    )
    lines.extend(
        [
            "",
            "## Verification surfaces",
            "",
            "- CasJobs: recovered historical SQL + deterministic DR18 probe",
            "- VizieR: live ALFALFA alpha.100 VOTable re-fetch",
            "- SDSS/MaNGA: direct publisher FITS re-download and SHA-256",
            "- Internal/theory placeholders: construction/reference review required",
            "",
            "**No registry promotion is automatic.**",
        ]
    )
    return "\n".join(lines) + "\n"


def write_receipt(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--live-public-sources", action="store_true")
    parser.add_argument("--casjobs-export", type=Path)
    parser.add_argument(
        "--casjobs-mode",
        choices=["historical-rerun", "deterministic-probe"],
        default="deterministic-probe",
    )
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args(argv)

    static = static_report()

    if args.live_public_sources and args.casjobs_export:
        parser.error("choose either --live-public-sources or --casjobs-export")

    if args.live_public_sources:
        result = {
            "static": static,
            "live_public_sources": verify_live_public_sources(),
        }
    elif args.casjobs_export:
        result = {
            "static": static,
            "casjobs": verify_casjobs_export(args.casjobs_export, args.casjobs_mode),
        }
    else:
        result = static

    if args.receipt_out:
        write_receipt(args.receipt_out, result)

    if args.format == "markdown" and not args.live_public_sources and not args.casjobs_export:
        sys.stdout.write(markdown(static))
    else:
        json.dump(result, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")

    if args.live_public_sources:
        return 0 if result["live_public_sources"]["all_passed"] else 3
    if args.casjobs_export:
        return 0 if result["casjobs"]["passed"] else 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
