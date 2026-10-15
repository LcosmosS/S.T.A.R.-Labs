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
import os
import shutil
import sys
import tempfile
import time
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "verification/datasets/dataset_verification_matrix_v0.1.csv"
DATASETS = ROOT / "registry/dataset_registry_v0.1.csv"
PROVENANCE = ROOT / "registry/data_provenance_registry_v0.1.csv"
OBSERVATIONAL_MANIFEST = (
    ROOT / "data/provenance/observational_dataset_intake_2026-10-09.json"
)
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
MEMBERSHIP_BACKCHECK_SQL = (
    ROOT
    / "verification/datasets/casjobs/DATA-SDSS18-200K_membership_backcheck.sql"
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
PUBLIC_PUBLISHER_IDS = (
    "DATA-MANGA-HI-ALL",
    "DATA-SFR-MANGA-PIP3D",
    "DATA-COSMIC-ENV",
)
EXPECTED_INDEPENDENT_IDS = {
    "DATA-SDSS18-200K",
    "DATA-MANGA-HI-ALL",
    "DATA-PROVENANCE-ALL",
    "DATA-SFR-MANGA-PIP3D",
    "DATA-VIZIER-ALFALFA100",
    "DATA-COSMIC-ENV",
    "DATA-PHYS-CONSTRAINTS",
    "DATA-ECC-THEORY",
}
ALLOWED_CANONICAL_PROVENANCE_STATUSES = {
    "unknown",
    "partially_verified",
    "verified",
}
MAX_LIVE_BYTES = 256 * 1024 * 1024
LIVE_TRANSFER_DEADLINE_SECONDS = 300
LIVE_SOCKET_TIMEOUT_SECONDS = 30


class DownloadError(RuntimeError):
    """Live download failure with a preserved partial-file receipt."""

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.details = details or {}


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


def _integrity_fields(value: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for item in value.split(";"):
        if "=" not in item:
            continue
        key, raw = item.split("=", 1)
        fields[key.strip()] = raw.strip()
    return fields


def _publisher_pins(
    matrix_by_id: dict[str, dict[str, str]],
    provenance_by_id: dict[str, dict[str, str]],
) -> dict[str, dict[str, object]]:
    """Build live-source pins from canonical provenance, cross-checked to matrix."""
    pins: dict[str, dict[str, object]] = {}
    for dataset_id in PUBLIC_PUBLISHER_IDS:
        provenance = provenance_by_id[dataset_id]
        matrix = matrix_by_id[dataset_id]
        integrity = _integrity_fields(provenance["Integrity_Check"])
        sha256 = integrity.get("SHA256", "")
        size_text = integrity.get("size_bytes", "")
        if not provenance["Source_URL"] or not sha256 or not size_text:
            raise ValueError(f"{dataset_id}: incomplete canonical publisher pin")
        if matrix["Public_Source"] != provenance["Source_URL"]:
            raise ValueError(f"{dataset_id}: matrix publisher URL drift")
        if matrix["Expected_SHA256"] != sha256:
            raise ValueError(f"{dataset_id}: matrix publisher SHA-256 drift")
        try:
            size = int(size_text)
        except ValueError as exc:
            raise ValueError(f"{dataset_id}: invalid publisher size pin") from exc
        pins[dataset_id] = {
            "url": provenance["Source_URL"],
            "sha256": sha256,
            "bytes": size,
        }
    return pins


def _observational_sdss_pin() -> dict[str, object]:
    manifest = json.loads(OBSERVATIONAL_MANIFEST.read_text(encoding="utf-8"))
    entry = manifest["datasets"]["DATA-SDSS18-200K"]
    return {
        "sha256": entry["sha256"],
        "bytes": int(entry["size_bytes"]),
        "rows": int(entry["rows"]),
    }


def static_report() -> dict:
    datasets = canonical_dataset_rows()
    provenance = canonical_provenance_rows()
    matrix = matrix_rows()

    dataset_ids = [row["Dataset_ID"] for row in datasets]
    provenance_ids = [row["Dataset_ID"] for row in provenance]
    matrix_ids = [row["Dataset_ID"] for row in matrix]

    if len(dataset_ids) != len(set(dataset_ids)):
        raise ValueError("duplicate canonical Dataset_ID")
    if len(provenance_ids) != len(set(provenance_ids)):
        raise ValueError("duplicate canonical provenance Dataset_ID")
    if len(matrix_ids) != len(set(matrix_ids)):
        raise ValueError("duplicate independent-verification matrix Dataset_ID")
    if set(dataset_ids) != set(provenance_ids):
        raise ValueError("canonical dataset/provenance IDs differ")
    if set(dataset_ids) != set(matrix_ids):
        raise ValueError(
            "independent-verification matrix does not cover canonical datasets"
        )

    by_provenance = {row["Dataset_ID"]: row for row in provenance}
    by_dataset = {row["Dataset_ID"]: row for row in datasets}
    by_matrix = {row["Dataset_ID"]: row for row in matrix}

    for dataset_id, provenance_row in by_provenance.items():
        status = provenance_row["Provenance_Status"]
        if status not in ALLOWED_CANONICAL_PROVENANCE_STATUSES:
            raise ValueError(
                f"{dataset_id}: unrecognized canonical provenance status {status!r}"
            )

    for row in matrix:
        dataset_id = row["Dataset_ID"]
        actual_status = by_provenance[dataset_id]["Provenance_Status"]
        if row["Canonical_Provenance_Status"] != actual_status:
            raise ValueError(
                f"{dataset_id}: matrix provenance status drift "
                f"({row['Canonical_Provenance_Status']} != {actual_status})"
            )
        if by_dataset[dataset_id]["Controlled_Support_Eligible"] != "false":
            raise ValueError(
                f"{dataset_id}: controlled support unexpectedly enabled"
            )
        if by_dataset[dataset_id]["Physical_Support_Eligible"] != "false":
            raise ValueError(
                f"{dataset_id}: physical support unexpectedly enabled"
            )

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
    if set(needs_independent) != EXPECTED_INDEPENDENT_IDS:
        raise ValueError(
            "independent-verification set drift: "
            f"{needs_independent!r}"
        )

    publisher_pins = _publisher_pins(by_matrix, by_provenance)

    historical_upper = sql_code(
        HISTORICAL_SQL.read_text(encoding="utf-8")
    ).upper()
    historical_rerun_upper = sql_code(
        HISTORICAL_RERUN_SQL.read_text(encoding="utf-8")
    ).upper()
    deterministic_upper = sql_code(
        DETERMINISTIC_SQL.read_text(encoding="utf-8")
    ).upper()

    common_sql = [
        "SELECT TOP 200000",
        "FROM PHOTOOBJ AS P",
        "JOIN SPECOBJ AS S",
        "S.BESTOBJID = P.OBJID",
        "P.U BETWEEN 0 AND 19.6",
    ]
    for token in common_sql:
        for label, sql in (
            ("historical", historical_upper),
            ("historical rerun", historical_rerun_upper),
            ("deterministic", deterministic_upper),
        ):
            if token not in sql:
                raise ValueError(f"{label} CasJobs SQL missing {token}")

    if "G BETWEEN 0 AND 20" not in historical_upper:
        raise ValueError("historical CasJobs SQL missing recovered g predicate")
    if "G BETWEEN 0 AND 20" not in historical_rerun_upper:
        raise ValueError("historical rerun SQL missing recovered g predicate")
    if "P.G BETWEEN 0 AND 20" not in deterministic_upper:
        raise ValueError("deterministic CasJobs SQL missing qualified g predicate")

    if "ORDER BY" in historical_upper or "ORDER BY" in historical_rerun_upper:
        raise ValueError("historical SQL must preserve the no-ORDER-BY condition")
    if "ORDER BY" not in deterministic_upper:
        raise ValueError("deterministic probe must have ORDER BY")
    if " INTO " in f" {historical_rerun_upper} ":
        raise ValueError(
            "historical rerun recipe must use the CasJobs Table field, not a fixed INTO"
        )
    if " INTO " in f" {deterministic_upper} ":
        raise ValueError(
            "deterministic probe must use the CasJobs Table field, not a fixed INTO"
        )
    if (
        "CLASS = 'GALAXY'" in historical_upper
        or "CLASS='GALAXY'" in historical_upper
    ):
        raise ValueError("historical SQL was silently changed to galaxy-only")

    backcheck_upper = sql_code(
        MEMBERSHIP_BACKCHECK_SQL.read_text(encoding="utf-8")
    ).upper()
    for token in (
        "MYDB.STAR_SDSS18_200K_IDS",
        "LEFT JOIN PHOTOOBJ AS P",
        "LEFT JOIN SPECOBJ AS S",
        "S.SPECOBJID = H.SPECOBJID",
        "S.BESTOBJID = P.OBJID",
        "P.U BETWEEN 0 AND 19.6",
        "P.G BETWEEN 0 AND 20",
    ):
        if token not in backcheck_upper:
            raise ValueError(f"membership backcheck SQL missing {token}")

    vizier = json.loads(VIZIER_REQUEST.read_text(encoding="utf-8"))
    if vizier["dataset_id"] != "DATA-VIZIER-ALFALFA100":
        raise ValueError("VizieR request has wrong dataset ID")
    if vizier["catalogue"] != "J/ApJ/861/49/table2":
        raise ValueError("VizieR catalogue identifier drift")
    if vizier["expected_rows"] != 31_502 or vizier["expected_fields"] != 25:
        raise ValueError("VizieR expected shape drift")

    alf_provenance = by_provenance["DATA-VIZIER-ALFALFA100"]
    alf_integrity = _integrity_fields(alf_provenance["Integrity_Check"])
    if vizier["url"] != alf_provenance["Source_URL"]:
        raise ValueError("VizieR URL differs from canonical provenance")
    if vizier["expected_frozen_sha256"] != alf_integrity.get("source_SHA256"):
        raise ValueError("VizieR source SHA-256 differs from canonical provenance")
    if int(vizier["expected_frozen_bytes"]) != int(
        alf_integrity.get("size_bytes", "0")
    ):
        raise ValueError("VizieR source byte count differs from canonical provenance")

    sdss_pin = _observational_sdss_pin()
    sdss_matrix = by_matrix["DATA-SDSS18-200K"]
    if sdss_matrix["Expected_SHA256"] != sdss_pin["sha256"]:
        raise ValueError("SDSS frozen SHA-256 differs from intake manifest")
    if int(sdss_matrix["Expected_Rows"]) != sdss_pin["rows"]:
        raise ValueError("SDSS frozen row count differs from intake manifest")

    return {
        "schema_version": "star-independent-dataset-verification-static-v0.2",
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
        "publisher_pins": publisher_pins,
        "casjobs": {
            "historical_sql": HISTORICAL_SQL.relative_to(ROOT).as_posix(),
            "historical_rerun_sql": HISTORICAL_RERUN_SQL.relative_to(ROOT).as_posix(),
            "historical_order_by_present": False,
            "deterministic_probe_sql": DETERMINISTIC_SQL.relative_to(ROOT).as_posix(),
            "membership_backcheck_sql": MEMBERSHIP_BACKCHECK_SQL.relative_to(
                ROOT
            ).as_posix(),
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


def _preserve_download(
    path: Path,
    preserve_dir: Path | None,
    label: str,
    suffix: str,
) -> str | None:
    if preserve_dir is None or not path.exists():
        return None
    preserve_dir.mkdir(parents=True, exist_ok=True)
    safe = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in label)
    digest = sha256_file(path) if path.stat().st_size else "empty"
    target = preserve_dir / f"{safe}.{digest[:16]}.{suffix}"
    if target.exists():
        target = preserve_dir / f"{safe}.{digest[:16]}.{time.time_ns()}.{suffix}"
    shutil.move(str(path), str(target))
    return str(target)


def _download_to_temp(
    url: str,
    *,
    max_bytes: int,
    preserve_dir: Path | None,
    label: str,
) -> tuple[Path, str, int]:
    if max_bytes <= 0 or max_bytes > MAX_LIVE_BYTES:
        raise ValueError(f"invalid live-response limit for {label}: {max_bytes}")
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "STAR-Labs-independent-dataset-verifier/0.2"},
    )
    digest = hashlib.sha256()
    count = 0
    started = time.monotonic()
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp_path = Path(temp.name)
    try:
        with urllib.request.urlopen(
            request, timeout=LIVE_SOCKET_TIMEOUT_SECONDS
        ) as response, temp:
            content_length = response.headers.get("Content-Length")
            if content_length:
                try:
                    declared = int(content_length)
                except ValueError:
                    declared = None
                if declared is not None and declared > max_bytes:
                    raise DownloadError(
                        f"{label}: declared response exceeds {max_bytes} bytes"
                    )
            while True:
                if time.monotonic() - started > LIVE_TRANSFER_DEADLINE_SECONDS:
                    raise DownloadError(
                        f"{label}: overall transfer deadline exceeded"
                    )
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                count += len(chunk)
                if count > max_bytes:
                    raise DownloadError(
                        f"{label}: response exceeded {max_bytes} bytes"
                    )
                digest.update(chunk)
                temp.write(chunk)
    except Exception as exc:
        temp.close()
        preserved = _preserve_download(
            temp_path, preserve_dir, label, "partial"
        )
        details = {
            "dataset_id": label,
            "download_bytes_before_failure": count,
            "partial_preserved_path": preserved,
        }
        if isinstance(exc, DownloadError):
            exc.details.update(details)
            raise
        raise DownloadError(str(exc), details) from exc
    return temp_path, digest.hexdigest(), count


def _publisher_live_limit(expected_bytes: int) -> int:
    return min(
        MAX_LIVE_BYTES,
        max(expected_bytes * 2, expected_bytes + 16 * 1024 * 1024),
    )


def verify_publisher_source(
    dataset_id: str,
    source: dict[str, object],
    preserve_dir: Path | None,
) -> dict:
    expected_bytes = int(source["bytes"])
    temp_path, digest, size = _download_to_temp(
        str(source["url"]),
        max_bytes=_publisher_live_limit(expected_bytes),
        preserve_dir=preserve_dir,
        label=dataset_id,
    )
    match = digest == source["sha256"] and size == expected_bytes
    preserved = None
    if match:
        temp_path.unlink(missing_ok=True)
    else:
        preserved = _preserve_download(
            temp_path, preserve_dir, dataset_id, "mismatch"
        )
    return {
        "dataset_id": dataset_id,
        "method": "publisher_https_refetch",
        "url": source["url"],
        "download_sha256": digest,
        "download_bytes": size,
        "expected_sha256": source["sha256"],
        "expected_bytes": expected_bytes,
        "sha256_match": digest == source["sha256"],
        "size_match": size == expected_bytes,
        "preserved_mismatch_path": preserved,
        "passed": match,
    }


def local_name(element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def _stream_votable(path: Path, spec: dict) -> dict:
    try:
        from defusedxml import ElementTree as SafeET
    except ImportError as exc:
        raise RuntimeError(
            "live VizieR verification requires defusedxml; install "
            "verification/datasets/requirements.txt"
        ) from exc

    fields: list[dict[str, str]] = []
    names: list[str] = []
    by_name: dict[str, int] | None = None
    agcs: set[str] = set()
    duplicate_agc_ids = 0
    blank_agc_ids = 0
    optical_missing = 0
    optical_partial = 0
    quality: Counter = Counter()
    row_count = 0

    for _, element in SafeET.iterparse(str(path), events=("end",)):
        name = local_name(element)
        if name == "FIELD":
            fields.append(dict(element.attrib))
            element.clear()
            continue
        if name != "TR":
            continue

        if not names:
            names = [field.get("name", "") for field in fields]
            by_name = {field_name: i for i, field_name in enumerate(names)}
        cells = [
            (child.text or "").strip()
            for child in element
            if local_name(child) == "TD"
        ]
        if len(cells) != len(fields):
            raise ValueError("live VOTable row width differs from FIELD count")
        row_count += 1

        required = set(spec["required_fields"])
        if by_name is not None and required.issubset(by_name):
            agc = cells[by_name["AGC"]]
            if not agc:
                blank_agc_ids += 1
            elif agc in agcs:
                duplicate_agc_ids += 1
            else:
                agcs.add(agc)

            rao = cells[by_name["RAO"]]
            deo = cells[by_name["DEO"]]
            if bool(rao) != bool(deo):
                optical_partial += 1
            elif not rao and not deo:
                optical_missing += 1

            quality[cells[by_name["HI"]]] += 1

        element.clear()

    if not names:
        names = [field.get("name", "") for field in fields]
    field_by_name = {
        field.get("name", ""): field for field in fields if field.get("name")
    }
    return {
        "fields": fields,
        "names": names,
        "field_by_name": field_by_name,
        "rows": row_count,
        "duplicate_agc_ids": duplicate_agc_ids,
        "blank_agc_ids": blank_agc_ids,
        "paired_missing_optical_coordinates": optical_missing,
        "partial_optical_coordinate_rows": optical_partial,
        "hi_quality_code_counts": dict(sorted(quality.items())),
    }


def verify_vizier_live(preserve_dir: Path | None) -> dict:
    spec = json.loads(VIZIER_REQUEST.read_text(encoding="utf-8"))
    temp_path, digest, size = _download_to_temp(
        spec["url"],
        max_bytes=int(spec["max_response_bytes"]),
        preserve_dir=preserve_dir,
        label=spec["dataset_id"],
    )
    try:
        parsed = _stream_votable(temp_path, spec)
    except Exception as exc:
        preserved = _preserve_download(
            temp_path, preserve_dir, spec["dataset_id"], "parse-failure"
        )
        return {
            "dataset_id": spec["dataset_id"],
            "method": "vizier_votable_refetch",
            "url": spec["url"],
            "download_sha256": digest,
            "download_bytes": size,
            "parse_error": f"{type(exc).__name__}: {exc}",
            "preserved_mismatch_path": preserved,
            "passed": False,
        }

    names = parsed["names"]
    required = set(spec["required_fields"])
    missing = sorted(required - set(names))
    coordinate_contract = spec["coordinate_contract"]
    coordinate_metadata_match = True
    coordinate_metadata_observed: dict[str, dict[str, str | None]] = {}
    for field_name, expected in coordinate_contract.items():
        observed = parsed["field_by_name"].get(field_name, {})
        coordinate_metadata_observed[field_name] = {
            "ucd": observed.get("ucd"),
            "ref": observed.get("ref"),
        }
        if (
            observed.get("ucd") != expected["ucd"]
            or observed.get("ref") != expected["ref"]
        ):
            coordinate_metadata_match = False

    expected = spec["expected_invariants"]
    semantic_match = (
        parsed["rows"] == spec["expected_rows"]
        and len(parsed["fields"]) == spec["expected_fields"]
        and not missing
        and parsed["blank_agc_ids"] == 0
        and parsed["duplicate_agc_ids"] == expected["duplicate_agc_ids"]
        and parsed["paired_missing_optical_coordinates"]
        == expected["paired_missing_optical_coordinates"]
        and parsed["partial_optical_coordinate_rows"]
        == expected["partial_optical_coordinate_rows"]
        and parsed["hi_quality_code_counts"]
        == expected["hi_quality_code_counts"]
        and coordinate_metadata_match
    )
    raw_match = (
        digest == spec["expected_frozen_sha256"]
        and size == int(spec["expected_frozen_bytes"])
    )
    passed = raw_match and semantic_match
    preserved = None
    if passed:
        temp_path.unlink(missing_ok=True)
    else:
        preserved = _preserve_download(
            temp_path, preserve_dir, spec["dataset_id"], "mismatch"
        )

    return {
        "dataset_id": spec["dataset_id"],
        "method": "vizier_votable_refetch",
        "url": spec["url"],
        "download_sha256": digest,
        "download_bytes": size,
        "expected_frozen_sha256": spec["expected_frozen_sha256"],
        "expected_frozen_bytes": spec["expected_frozen_bytes"],
        "raw_sha256_match": digest == spec["expected_frozen_sha256"],
        "raw_size_match": size == int(spec["expected_frozen_bytes"]),
        "rows": parsed["rows"],
        "fields": len(parsed["fields"]),
        "missing_required_fields": missing,
        "blank_agc_ids": parsed["blank_agc_ids"],
        "duplicate_agc_ids": parsed["duplicate_agc_ids"],
        "paired_missing_optical_coordinates": parsed[
            "paired_missing_optical_coordinates"
        ],
        "partial_optical_coordinate_rows": parsed[
            "partial_optical_coordinate_rows"
        ],
        "hi_quality_code_counts": parsed["hi_quality_code_counts"],
        "coordinate_metadata_match": coordinate_metadata_match,
        "coordinate_metadata_observed": coordinate_metadata_observed,
        "semantic_invariants_match": semantic_match,
        "preserved_mismatch_path": preserved,
        "passed": passed,
        "disposition": (
            "byte_and_semantic_match" if passed else "requires_manual_review"
        ),
    }


def _failed_live_result(dataset_id: str, method: str, exc: Exception) -> dict:
    result = {
        "dataset_id": dataset_id,
        "method": method,
        "passed": False,
        "error": f"{type(exc).__name__}: {exc}",
    }
    if isinstance(exc, DownloadError):
        result.update(exc.details)
    return result


def verify_live_public_sources(
    publisher_pins: dict[str, dict[str, object]],
    preserve_dir: Path | None,
) -> dict:
    results: list[dict] = []
    for dataset_id in PUBLIC_PUBLISHER_IDS:
        try:
            results.append(
                verify_publisher_source(
                    dataset_id, publisher_pins[dataset_id], preserve_dir
                )
            )
        except Exception as exc:
            results.append(
                _failed_live_result(
                    dataset_id, "publisher_https_refetch", exc
                )
            )
    try:
        results.append(verify_vizier_live(preserve_dir))
    except Exception as exc:
        results.append(
            _failed_live_result(
                "DATA-VIZIER-ALFALFA100",
                "vizier_votable_refetch",
                exc,
            )
        )
    return {
        "schema_version": "star-independent-live-source-receipt-v0.2",
        "generated_at_utc": utc_now(),
        "results": results,
        "all_passed": all(item.get("passed") is True for item in results),
        "automatic_registry_promotion": False,
    }


def _stable_snapshot(path: Path) -> tuple[Path, str, int]:
    """Copy and hash one stable view of a file; reject in-place mutation."""
    path = path.resolve()
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp_path = Path(temp.name)
    digest = hashlib.sha256()
    copied = 0
    try:
        with path.open("rb") as source, temp:
            before = os.fstat(source.fileno())
            while True:
                chunk = source.read(1024 * 1024)
                if not chunk:
                    break
                copied += len(chunk)
                digest.update(chunk)
                temp.write(chunk)
            after = os.fstat(source.fileno())
        if (
            before.st_size != after.st_size
            or before.st_mtime_ns != after.st_mtime_ns
            or copied != before.st_size
        ):
            raise ValueError("input changed while verification snapshot was created")
        return temp_path, digest.hexdigest(), copied
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise


def _read_csv_profile(path: Path) -> dict:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.reader(stream, strict=True)
        try:
            header = next(reader)
        except StopIteration as exc:
            raise ValueError("CasJobs export is empty") from exc
        if header != SDSS_COLUMNS:
            raise ValueError(f"CasJobs export header mismatch: {header!r}")

        classes: Counter = Counter()
        pairs: set[tuple[str, str]] = set()
        row_count = 0
        row_width_errors = 0
        blank_id_rows = 0
        duplicate_pair_rows = 0
        numeric_errors = 0
        coordinate_errors = 0
        predicate_violations = 0
        negative_redshift = 0

        for raw in reader:
            row_count += 1
            if len(raw) != len(SDSS_COLUMNS):
                row_width_errors += 1
                continue
            row = dict(zip(SDSS_COLUMNS, raw))
            objid = row["objid"].strip()
            specobjid = row["specobjid"].strip()
            if not objid or not specobjid:
                blank_id_rows += 1
            pair = (objid, specobjid)
            if pair in pairs:
                duplicate_pair_rows += 1
            else:
                pairs.add(pair)

            classes[row["class"].strip()] += 1
            try:
                ra = float(row["ra"])
                dec = float(row["dec"])
                u = float(row["u"])
                g = float(row["g"])
                redshift = float(row["redshift"])
            except ValueError:
                numeric_errors += 1
                continue

            if not (0.0 <= ra < 360.0 and -90.0 <= dec <= 90.0):
                coordinate_errors += 1
            if not (0.0 <= u <= 19.6 and 0.0 <= g <= 20.0):
                predicate_violations += 1
            if redshift < 0:
                negative_redshift += 1

    semantic_valid = (
        row_width_errors == 0
        and blank_id_rows == 0
        and duplicate_pair_rows == 0
        and numeric_errors == 0
        and coordinate_errors == 0
        and predicate_violations == 0
        and "" not in classes
    )
    return {
        "header": header,
        "rows": row_count,
        "class_counts": dict(sorted(classes.items())),
        "negative_redshift_rows": negative_redshift,
        "pairs": pairs,
        "unique_objid_specobjid_pairs": len(pairs),
        "row_width_errors": row_width_errors,
        "blank_id_rows": blank_id_rows,
        "duplicate_pair_rows": duplicate_pair_rows,
        "numeric_errors": numeric_errors,
        "coordinate_errors": coordinate_errors,
        "predicate_violations": predicate_violations,
        "semantic_valid": semantic_valid,
    }


def _frozen_sdss_profile() -> tuple[dict, str, int] | None:
    if not FROZEN_SDSS.is_file() or is_lfs_pointer(FROZEN_SDSS):
        return None
    pin = _observational_sdss_pin()
    snapshot, digest, size = _stable_snapshot(FROZEN_SDSS)
    try:
        if digest != pin["sha256"] or size != pin["bytes"]:
            raise ValueError(
                "frozen SDSS baseline does not match its pinned SHA-256/size"
            )
        profile = _read_csv_profile(snapshot)
        if profile["rows"] != pin["rows"] or not profile["semantic_valid"]:
            raise ValueError("frozen SDSS baseline fails pinned row/semantic checks")
        return profile, digest, size
    finally:
        snapshot.unlink(missing_ok=True)


def verify_casjobs_export(path: Path, mode: str) -> dict:
    path = path.resolve()
    if not path.is_file():
        raise ValueError(f"CasJobs export is missing: {path}")

    snapshot, digest, size = _stable_snapshot(path)
    try:
        profile = _read_csv_profile(snapshot)
    finally:
        snapshot.unlink(missing_ok=True)

    result = {
        "schema_version": "star-independent-casjobs-receipt-v0.2",
        "generated_at_utc": utc_now(),
        "mode": mode,
        "export_path": str(path),
        "export_sha256": digest,
        "export_bytes": size,
        "rows": profile["rows"],
        "columns": profile["header"],
        "class_counts": profile["class_counts"],
        "negative_redshift_rows": profile["negative_redshift_rows"],
        "unique_objid_specobjid_pairs": profile["unique_objid_specobjid_pairs"],
        "row_width_errors": profile["row_width_errors"],
        "blank_id_rows": profile["blank_id_rows"],
        "duplicate_pair_rows": profile["duplicate_pair_rows"],
        "numeric_errors": profile["numeric_errors"],
        "coordinate_errors": profile["coordinate_errors"],
        "predicate_violations": profile["predicate_violations"],
        "schema_match": profile["header"] == SDSS_COLUMNS,
        "row_count_match": profile["rows"] == 200_000,
        "semantic_profile_valid": profile["semantic_valid"],
        "historical_exact_membership_reproducible": False,
        "historical_identity_verified": False,
        "automatic_registry_promotion": False,
    }

    frozen = _frozen_sdss_profile()
    if frozen is None:
        result["frozen_comparison"] = {
            "available": False,
            "reason": "frozen Git LFS object is absent or not hydrated",
        }
        result["passed"] = False
        return result

    frozen_profile, frozen_digest, frozen_size = frozen
    intersection = len(profile["pairs"] & frozen_profile["pairs"])
    union = len(profile["pairs"] | frozen_profile["pairs"])
    byte_identical = digest == frozen_digest and size == frozen_size
    exact_profile_match = (
        profile["class_counts"] == frozen_profile["class_counts"]
        and profile["negative_redshift_rows"]
        == frozen_profile["negative_redshift_rows"]
    )
    exact_pair_match = profile["pairs"] == frozen_profile["pairs"]
    class_domain_match = (
        set(profile["class_counts"]) == set(frozen_profile["class_counts"])
    )
    negative_redshift_presence_match = (
        (profile["negative_redshift_rows"] > 0)
        == (frozen_profile["negative_redshift_rows"] > 0)
    )
    nonzero_overlap = intersection > 0

    result["frozen_comparison"] = {
        "available": True,
        "frozen_sha256": frozen_digest,
        "frozen_bytes": frozen_size,
        "frozen_rows": frozen_profile["rows"],
        "frozen_class_counts": frozen_profile["class_counts"],
        "frozen_negative_redshift_rows": frozen_profile[
            "negative_redshift_rows"
        ],
        "pair_intersection": intersection,
        "pair_union": union,
        "pair_jaccard": intersection / union if union else 1.0,
        "nonzero_pair_overlap": nonzero_overlap,
        "class_domain_match": class_domain_match,
        "negative_redshift_presence_match": negative_redshift_presence_match,
        "exact_profile_match": exact_profile_match,
        "exact_pair_match": exact_pair_match,
        "byte_identical": byte_identical,
    }

    structural = (
        result["schema_match"]
        and result["row_count_match"]
        and result["semantic_profile_valid"]
    )
    if mode == "historical-rerun":
        result["passed"] = (
            structural
            and byte_identical
            and exact_profile_match
            and exact_pair_match
        )
        result["historical_identity_verified"] = result["passed"]
    else:
        result["passed"] = (
            structural
            and nonzero_overlap
            and class_domain_match
            and negative_redshift_presence_match
        )
        result["historical_identity_verified"] = False
    return result


def markdown(report: dict) -> str:
    lines = [
        "# Independent dataset verification",
        "",
        f"- Canonical datasets: **{report['canonical_dataset_count']}**",
        (
            "- Canonical source provenance still \`unknown\`: "
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
        f"- \`{dataset_id}\`"
        for dataset_id in report["source_provenance_unknown_ids"]
    )
    lines.extend(
        [
            "",
            "## Verification surfaces",
            "",
            "- CasJobs: recovered SQL, rerun wrapper, deterministic DR18 probe, and row-membership backcheck",
            "- VizieR: bounded streaming ALFALFA alpha.100 VOTable re-fetch",
            "- SDSS/MaNGA: bounded direct publisher FITS re-download and SHA-256",
            "- Internal/theory placeholders: construction/reference review required",
            "",
            "**No registry promotion is automatic.**",
        ]
    )
    return "\n".join(lines) + "\n"


def _validate_receipt_path(
    path: Path,
    *,
    casjobs_export: Path | None = None,
) -> Path:
    resolved = path.resolve()
    protected = {
        DATASETS.resolve(),
        PROVENANCE.resolve(),
        MATRIX.resolve(),
        HISTORICAL_SQL.resolve(),
        HISTORICAL_RERUN_SQL.resolve(),
        DETERMINISTIC_SQL.resolve(),
        MEMBERSHIP_BACKCHECK_SQL.resolve(),
        VIZIER_REQUEST.resolve(),
    }
    if casjobs_export is not None:
        protected.add(casjobs_export.resolve())
    if resolved in protected or (ROOT / "registry").resolve() in resolved.parents:
        raise ValueError(f"receipt path is a protected input: {resolved}")
    return resolved


def write_receipt(path: Path, value: dict) -> None:
    """Atomically create a receipt; never overwrite an existing receipt."""
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"receipt already exists: {path}")

    payload = (
        json.dumps(value, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    temp = tempfile.NamedTemporaryFile(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    )
    temp_path = Path(temp.name)
    try:
        with temp:
            temp.write(payload)
            temp.flush()
            os.fsync(temp.fileno())
        os.link(temp_path, path)
    finally:
        temp_path.unlink(missing_ok=True)


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
    parser.add_argument(
        "--mismatch-dir",
        type=Path,
        help="preserve mismatching/partial live downloads for reviewer inspection",
    )
    args = parser.parse_args(argv)

    static = static_report()

    if args.live_public_sources and args.casjobs_export:
        parser.error("choose either --live-public-sources or --casjobs-export")

    matrix = {row["Dataset_ID"]: row for row in matrix_rows()}
    provenance = {
        row["Dataset_ID"]: row for row in canonical_provenance_rows()
    }
    publisher_pins = _publisher_pins(matrix, provenance)

    if args.live_public_sources:
        result = {
            "static": static,
            "live_public_sources": verify_live_public_sources(
                publisher_pins,
                args.mismatch_dir.resolve() if args.mismatch_dir else None,
            ),
        }
    elif args.casjobs_export:
        result = {
            "static": static,
            "casjobs": verify_casjobs_export(
                args.casjobs_export, args.casjobs_mode
            ),
        }
    else:
        result = static

    if args.receipt_out:
        receipt_path = _validate_receipt_path(
            args.receipt_out,
            casjobs_export=args.casjobs_export,
        )
        write_receipt(receipt_path, result)

    if (
        args.format == "markdown"
        and not args.live_public_sources
        and not args.casjobs_export
    ):
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
