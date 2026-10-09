#!/usr/bin/env python3
"""Build and verify frozen Pipe3D and ALFALFA provenance-only intake.

The default mode is read-only and fail-closed. ``--refresh`` is an explicit
maintainer operation that rewrites only the deterministic ALFALFA derivatives
and machine manifest from already-preserved raw inputs.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import struct
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALF_DIR = ROOT / "data/intake/vizier/alfalfa100/2026-10-09-cds-corrected-2019"
PIPE_DIR = ROOT / "data/intake/sdss/pipe3d/dr17-v3_1_1-2026-10-09"
GEMA_DIR = ROOT / "data/intake/sdss/gema/dr17-2.0.2-2026-10-09"
RAW_VOT = ALF_DIR / "table2.vot"
README = ALF_DIR / "ReadMe.html"
VOT_HEADERS = ALF_DIR / "table2.response-headers.txt"
README_HEADERS = ALF_DIR / "ReadMe.response-headers.txt"
REQUEST = ALF_DIR / "request.json"
PIPE_FITS = PIPE_DIR / "SDSS17Pipe3D_v3_1_1.fits"
GEMA_FITS = GEMA_DIR / "GEMA_2.0.2.fits"
DERIVED_DIR = ROOT / "data/derived/vizier/alfalfa100/2026-10-09-cds-corrected-2019"
FULL_COORDS = DERIVED_DIR / "alfalfa100_hi_centroids_full.csv"
DISPLAY_COORDS = DERIVED_DIR / "alfalfa100_hi_centroids_display_2000.csv"
MANIFEST = ROOT / "data/provenance/observational_dataset_intake_2026-10-09.json"
PROTOCOL = ROOT / "research/acquisition/vizier_alfalfa100/matching_protocol_v1.md"
CANDIDATE = ROOT / "web_tool/content/sky-overlay-candidates.v1.json"

EXPECTED = {
    "pipe_sha256": "ac714809044c02dcb2cc8b5007d02981d9316c34dc398a79f4c07bde4d3496fc",
    "pipe_bytes": 55_889_280,
    "pipe_rows": 10_220,
    "pipe_fields": 536,
    "gema_sha256": "244e9286f225b9e1dbef73bb93e1101d840a2a62ec5dabf3aa16ec88cfef1597",
    "gema_bytes": 7_223_040,
    "gema_tables": 15,
    "alf_sha256": "654217f9b3414856c1a8b09071c81eb834a0b0fbc6ec3aea9777e01fdaea1079",
    "alf_bytes": 10_981_088,
    "readme_sha256": "6aa40d3e1552c104e5197a330bb30f440f87206d4763a52322a6c02afd43b9d4",
    "readme_bytes": 24_714,
    "alf_rows": 31_502,
    "alf_fields": 25,
    "display_rows": 2_000,
}
DISPLAY_SALT = b"ALFALFA-A100-DISPLAY-v1\0"
PR_LINKS = [
    "https://github.com/LcosmosS/S.T.A.R.-Labs/pull/78",
    "https://github.com/LcosmosS/S.T.A.R.-Labs/pull/80",
    "https://github.com/LcosmosS/S.T.A.R.-Labs/pull/81",
]


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def read_bytes(path: Path) -> bytes:
    value = path.read_bytes()
    if value.startswith(b"version https://git-lfs.github.com/spec/v1"):
        raise ValueError(f"{path.relative_to(ROOT)} is an unhydrated Git LFS pointer")
    return value


def digest(path: Path) -> tuple[str, int]:
    value = read_bytes(path)
    return sha256_bytes(value), len(value)


def _fits_value(card: str):
    if card[8:10] != "= ":
        return None
    raw = card[10:].split("/", 1)[0].strip()
    if raw.startswith("'"):
        return raw.strip().strip("'").strip()
    if raw in {"T", "F"}:
        return raw == "T"
    try:
        return int(raw)
    except ValueError:
        try:
            return float(raw.replace("D", "E"))
        except ValueError:
            return raw


def fits_hdus(path: Path) -> list[dict[str, object]]:
    data = read_bytes(path)
    offset = 0
    hdus: list[dict[str, object]] = []
    while offset < len(data):
        cards: list[str] = []
        header_end = None
        for card_offset in range(offset, len(data), 80):
            card = data[card_offset : card_offset + 80].decode("ascii")
            cards.append(card)
            if card.startswith("END"):
                header_end = card_offset + 80
                break
        if header_end is None:
            raise ValueError("unterminated FITS header")
        header_size = math.ceil((header_end - offset) / 2880) * 2880
        values = {card[:8].strip(): _fits_value(card) for card in cards if card[8:10] == "= "}
        naxis = int(values.get("NAXIS", 0))
        if values.get("XTENSION") in {"BINTABLE", "TABLE"}:
            logical_size = (
                int(values.get("NAXIS1", 0)) * int(values.get("NAXIS2", 0))
                + int(values.get("PCOUNT", 0))
            ) * int(values.get("GCOUNT", 1))
        else:
            logical_size = 0 if naxis == 0 else abs(int(values.get("BITPIX", 8))) // 8
            for index in range(1, naxis + 1):
                logical_size *= int(values.get(f"NAXIS{index}", 0))
            if logical_size:
                logical_size = (logical_size + int(values.get("PCOUNT", 0))) * int(values.get("GCOUNT", 1))
        hdus.append(values)
        offset += header_size + (math.ceil(logical_size / 2880) * 2880 if logical_size else 0)
        if offset == len(data):
            break
        if offset > len(data):
            raise ValueError("FITS HDU extends beyond file")
    return hdus


def local_name(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def parse_votable(path: Path) -> tuple[list[dict[str, str]], list[list[str]]]:
    root = ET.fromstring(read_bytes(path))
    fields = [dict(element.attrib) for element in root.iter() if local_name(element) == "FIELD"]
    rows = [
        [(child.text or "").strip() for child in element if local_name(child) == "TD"]
        for element in root.iter()
        if local_name(element) == "TR"
    ]
    if any(len(row) != len(fields) for row in rows):
        raise ValueError("VOTable row width differs from FIELD count")
    return fields, rows


def ra_degrees(value: str) -> float:
    h, m, s = (float(part) for part in value.replace(":", " ").split())
    result = 15.0 * (h + m / 60.0 + s / 3600.0)
    if not 0.0 <= result < 360.0:
        raise ValueError(f"RA outside [0,360): {value}")
    return result


def dec_degrees(value: str) -> float:
    parts = value.replace(":", " ").split()
    sign = -1.0 if parts[0].startswith("-") else 1.0
    d, m, s = abs(float(parts[0])), float(parts[1]), float(parts[2])
    result = sign * (d + m / 60.0 + s / 3600.0)
    if not -90.0 <= result <= 90.0:
        raise ValueError(f"Dec outside [-90,90]: {value}")
    return result


def csv_bytes(rows: list[tuple[str, float, float]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(["source_id", "ra_deg", "dec_deg"])
    for source_id, ra, dec in rows:
        writer.writerow([source_id, f"{ra:.8f}", f"{dec:.8f}"])
    return stream.getvalue().encode("utf-8")


def analyze() -> tuple[dict[str, object], bytes, bytes]:
    pipe_sha, pipe_size = digest(PIPE_FITS)
    if (pipe_sha, pipe_size) != (EXPECTED["pipe_sha256"], EXPECTED["pipe_bytes"]):
        raise ValueError("Pipe3D bytes differ from the publisher-verified object")
    tables = [hdu for hdu in fits_hdus(PIPE_FITS) if hdu.get("XTENSION") in {"BINTABLE", "TABLE"}]
    if len(tables) != 1:
        raise ValueError(f"expected one Pipe3D binary table; found {len(tables)}")
    table = tables[0]
    if (table.get("NAXIS2"), table.get("TFIELDS")) != (EXPECTED["pipe_rows"], EXPECTED["pipe_fields"]):
        raise ValueError("Pipe3D FITS row/field count drift")

    gema_sha, gema_size = digest(GEMA_FITS)
    if (gema_sha, gema_size) != (EXPECTED["gema_sha256"], EXPECTED["gema_bytes"]):
        raise ValueError("GEMA bytes differ from the publisher-verified object")
    gema_tables = [hdu for hdu in fits_hdus(GEMA_FITS) if hdu.get("XTENSION") in {"BINTABLE", "TABLE"}]
    if len(gema_tables) != EXPECTED["gema_tables"]:
        raise ValueError("GEMA FITS table-count drift")
    gema_schema = [
        {"extname": str(hdu.get("EXTNAME", "")), "rows": int(hdu.get("NAXIS2", 0)), "fields": int(hdu.get("TFIELDS", 0))}
        for hdu in gema_tables
    ]

    raw_sha, raw_size = digest(RAW_VOT)
    readme_sha, readme_size = digest(README)
    if (raw_sha, raw_size) != (EXPECTED["alf_sha256"], EXPECTED["alf_bytes"]):
        raise ValueError("ALFALFA VOTable bytes differ from frozen acquisition")
    if (readme_sha, readme_size) != (EXPECTED["readme_sha256"], EXPECTED["readme_bytes"]):
        raise ValueError("ALFALFA ReadMe bytes differ from frozen acquisition")
    fields, rows = parse_votable(RAW_VOT)
    if (len(fields), len(rows)) != (EXPECTED["alf_fields"], EXPECTED["alf_rows"]):
        raise ValueError("ALFALFA field/row count drift or truncation")
    names = [field.get("name", "") for field in fields]
    required = {"AGC", "RAJ2000", "DEJ2000", "RAO", "DEO", "Vhel", "W50", "e_W50", "HIflux", "e_HIflux", "SNR", "rms", "Dist", "logMHI", "HI"}
    if not required.issubset(names):
        raise ValueError(f"missing required ALFALFA fields: {sorted(required - set(names))}")
    by_name = {name: index for index, name in enumerate(names)}
    field_by_name = {field["name"]: field for field in fields}
    if field_by_name["RAJ2000"].get("ucd") != "pos.eq.ra;meta.main" or field_by_name["RAJ2000"].get("ref") != "J2000":
        raise ValueError("RAJ2000 is not the VizieR main J2000 right ascension")
    if field_by_name["DEJ2000"].get("ucd") != "pos.eq.dec;meta.main" or field_by_name["DEJ2000"].get("ref") != "J2000":
        raise ValueError("DEJ2000 is not the VizieR main J2000 declination")

    agcs = [row[by_name["AGC"]] for row in rows]
    duplicates = sorted(key for key, count in Counter(agcs).items() if count > 1)
    if "" in agcs or duplicates:
        raise ValueError(f"blank or duplicate AGC identifiers: {duplicates[:5]}")
    coords: list[tuple[str, float, float]] = []
    optical_missing = 0
    optical_partial = 0
    quality = Counter()
    for row in rows:
        source_id = "AGC-" + row[by_name["AGC"]]
        coords.append((source_id, ra_degrees(row[by_name["RAJ2000"]]), dec_degrees(row[by_name["DEJ2000"]])))
        rao, deo = row[by_name["RAO"]], row[by_name["DEO"]]
        if not rao and not deo:
            optical_missing += 1
        elif not rao or not deo:
            optical_partial += 1
        else:
            ra_degrees(rao)
            dec_degrees(deo)
        quality[row[by_name["HI"]]] += 1
    if optical_partial:
        raise ValueError("RAO/DEO paired-missingness violation")
    ranked = sorted(range(len(coords)), key=lambda index: (hashlib.sha256(DISPLAY_SALT + agcs[index].encode("ascii")).hexdigest(), agcs[index]))
    selected_indexes = set(ranked[: EXPECTED["display_rows"]])
    display = [row for index, row in enumerate(coords) if index in selected_indexes]
    full_bytes, display_bytes = csv_bytes(coords), csv_bytes(display)
    selected_ids = "".join(row[0] + "\n" for row in display).encode("utf-8")
    info: dict[str, object] = {
        "pipe3d": {"sha256": pipe_sha, "size_bytes": pipe_size, "fits_rows": int(table["NAXIS2"]), "fits_fields": int(table["TFIELDS"])},
        "gema": {"sha256": gema_sha, "size_bytes": gema_size, "fits_table_count": len(gema_tables), "fits_tables": gema_schema},
        "alfalfa": {
            "source_sha256": raw_sha,
            "source_size_bytes": raw_size,
            "readme_sha256": readme_sha,
            "readme_size_bytes": readme_size,
            "source_rows": len(rows),
            "field_count": len(fields),
            "agc_duplicate_count": len(duplicates),
            "optical_coordinate_missing_rows": optical_missing,
            "optical_coordinate_partial_rows": optical_partial,
            "hi_quality_code_counts": dict(sorted(quality.items())),
            "full_coordinate_sha256": sha256_bytes(full_bytes),
            "full_coordinate_size_bytes": len(full_bytes),
            "display_coordinate_sha256": sha256_bytes(display_bytes),
            "display_coordinate_size_bytes": len(display_bytes),
            "display_rows": len(display),
            "selected_ids_sha256": sha256_bytes(selected_ids),
        },
    }
    return info, full_bytes, display_bytes


def build_manifest(info: dict[str, object]) -> dict[str, object]:
    request = json.loads(REQUEST.read_text(encoding="utf-8"))
    return {
        "schema_version": "star-observational-dataset-intake-v1",
        "acquisition_date": "2026-10-09",
        "governing_authority": "charter/STAR_Research_Charter_v0-2.pdf",
        "generator": "scripts/validate_observational_datasets.py",
        "datasets": {
            "DATA-SFR-MANGA-PIP3D": {
                **info["pipe3d"],
                "publisher": "SDSS",
                "version_or_release": "SDSS DR17; MANGADRP_VER v3_1_1; PIPE3D_VER 3.1.1",
                "source_url": "https://data.sdss.org/sas/dr17/env/MANGA_PIPE3D/v3_1_1/3.1.1/SDSS17Pipe3D_v3_1_1.fits",
                "repository_path": PIPE_FITS.relative_to(ROOT).as_posix(),
                "provenance_status": "verified",
                "evidence_status": "unknown",
            },
            "DATA-VIZIER-ALFALFA100": {
                **info["alfalfa"],
                "publisher": "CDS VizieR",
                "version_or_release": "J/ApJ/861/49/table2 corrected August 2019",
                "catalogue_doi": "10.26093/cds/vizier.18610049",
                "article_doi": "10.3847/1538-4357/aac956",
                "request": request,
                "source_path": RAW_VOT.relative_to(ROOT).as_posix(),
                "source_headers_path": VOT_HEADERS.relative_to(ROOT).as_posix(),
                "readme_path": README.relative_to(ROOT).as_posix(),
                "readme_headers_path": README_HEADERS.relative_to(ROOT).as_posix(),
                "full_coordinate_path": FULL_COORDS.relative_to(ROOT).as_posix(),
                "display_coordinate_path": DISPLAY_COORDS.relative_to(ROOT).as_posix(),
                "coordinate_role": "hi_centroid",
                "coordinate_frame": "J2000 equatorial; VizieR main-coordinate UCDs",
                "selection_policy": "2000 lowest SHA256(ALFALFA-A100-DISPLAY-v1\\0 + AGC); output in source order",
                "matching_protocol_path": PROTOCOL.relative_to(ROOT).as_posix(),
                "matching_protocol_sha256": digest(PROTOCOL)[0],
                "provenance_status": "verified",
                "evidence_status": "unknown",
                "web_admission_status": "pending_independent_review",
            },
            "DATA-COSMIC-ENV": {
                **info["gema"],
                "publisher": "SDSS / MaNGA GEMA",
                "version_or_release": "SDSS DR17; GEMA 2.0.2",
                "source_url": "https://data.sdss.org/sas/dr17/env/MANGA_GEMA/2.0.2/GEMA_2.0.2.fits",
                "repository_path": GEMA_FITS.relative_to(ROOT).as_posix(),
                "provenance_status": "verified",
                "evidence_status": "unknown",
            },
        },
        "eligibility": {"controlled_execution": False, "controlled_support": False, "physical_support": False},
        "independent_review_references": PR_LINKS,
    }


def check_candidate(manifest: dict[str, object]) -> None:
    candidate = json.loads(CANDIDATE.read_text(encoding="utf-8"))
    if candidate.get("schemaVersion") != "star-sky-overlay-candidates-v1" or len(candidate.get("candidates", [])) != 1:
        raise ValueError("invalid sky-overlay candidate manifest")
    item = candidate["candidates"][0]
    source = manifest["datasets"]["DATA-VIZIER-ALFALFA100"]
    expected = {
        "datasetId": "DATA-VIZIER-ALFALFA100",
        "qualifiedDatasetId": "REPO-CSV-v0.2:DATA-VIZIER-ALFALFA100",
        "sourcePath": source["source_path"],
        "sourceSha256": source["source_sha256"],
        "coordinatePath": source["display_coordinate_path"],
        "coordinateSha256": source["display_coordinate_sha256"],
        "selectedIdsSha256": source["selected_ids_sha256"],
        "coordinateRole": "hi_centroid",
        "sourceRows": 31_502,
        "displayRows": 2_000,
        "approvalStatus": "pending_independent_review",
    }
    for key, value in expected.items():
        if item.get(key) != value:
            raise ValueError(f"sky candidate {key} is not bound to frozen intake")
    if item.get("reviewReferences") != PR_LINKS or item.get("controlledSupportEligible") is not False or item.get("physicalSupportEligible") is not False:
        raise ValueError("sky candidate review/eligibility gate drift")


def verify_registry(manifest: dict[str, object]) -> None:
    def rows(name: str) -> dict[str, dict[str, str]]:
        with (ROOT / "registry" / name).open(encoding="utf-8", newline="") as stream:
            return {row["Dataset_ID"]: row for row in csv.DictReader(stream, strict=True)}
    datasets, provenance = rows("dataset_registry_v0.1.csv"), rows("data_provenance_registry_v0.1.csv")
    for dataset_id in ("DATA-SFR-MANGA-PIP3D", "DATA-COSMIC-ENV", "DATA-VIZIER-ALFALFA100"):
        ds, pv = datasets[dataset_id], provenance[dataset_id]
        source = manifest["datasets"][dataset_id]
        if ds["Status"] != "planned" or not (ds["Provenance_Status"] == pv["Provenance_Status"] == "verified"):
            raise ValueError(f"{dataset_id} registry status is not provenance-only verified/planned")
        if ds["Achieved_Evidence_Status"] != pv["Evidence_Status"] or ds["Achieved_Evidence_Status"] != "unknown":
            raise ValueError(f"{dataset_id} evidence status was promoted")
        if any(ds[field] != "false" for field in ("Controlled_Execution_Eligible", "Controlled_Support_Eligible", "Physical_Support_Eligible")):
            raise ValueError(f"{dataset_id} eligibility was promoted")
        digest_key = "source_sha256" if dataset_id == "DATA-VIZIER-ALFALFA100" else "sha256"
        if source[digest_key] not in pv["Integrity_Check"]:
            raise ValueError(f"{dataset_id} canonical provenance does not bind raw SHA-256")


def markdown(manifest: dict[str, object]) -> str:
    pipe = manifest["datasets"]["DATA-SFR-MANGA-PIP3D"]
    gema = manifest["datasets"]["DATA-COSMIC-ENV"]
    alf = manifest["datasets"]["DATA-VIZIER-ALFALFA100"]
    return "\n".join([
        "# Observational dataset lineage and Aladin review gate",
        "",
        "This CI report verifies repository bytes and registry bindings. It does not supply independent scientific authorization.",
        "",
        "| Dataset | Preserved source | Validation | Status |",
        "|---|---|---|---|",
        f"| DATA-SFR-MANGA-PIP3D | `{pipe['sha256']}` ({pipe['size_bytes']} bytes) | {pipe['fits_rows']} FITS rows; {pipe['fits_fields']} fields | provenance verified; evidence unknown; all eligibility false |",
        f"| DATA-COSMIC-ENV | `{gema['sha256']}` ({gema['size_bytes']} bytes) | {gema['fits_table_count']} FITS tables | provenance verified; evidence unknown; all eligibility false |",
        f"| DATA-VIZIER-ALFALFA100 | `{alf['source_sha256']}` ({alf['source_size_bytes']} bytes) | {alf['source_rows']} VOTable rows; {alf['field_count']} fields; {alf['agc_duplicate_count']} duplicate AGC IDs | provenance verified; Aladin admission pending independent review; all eligibility false |",
        "",
        f"ALFALFA full H I-centroid derivative: `{alf['full_coordinate_sha256']}` ({alf['source_rows']} rows). Display candidate: `{alf['display_coordinate_sha256']}` ({alf['display_rows']} deterministically selected rows); selected-ID chain `{alf['selected_ids_sha256']}`.",
        "",
        "Independent verification and authorization references (open review records; a link alone is not approval):",
        *[f"- [PR #{url.rsplit('/', 1)[-1]}]({url})" for url in PR_LINKS],
        "",
        "Admission requires an off-author review receipt bound to these exact hashes and a reviewed commit before the candidate can move into `web_tool/content/sky-overlay-releases.v1.json`.",
        "",
    ])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="rewrite deterministic derivatives and manifest")
    parser.add_argument("--format", choices=("text", "markdown"), default="text")
    args = parser.parse_args()
    info, full_bytes, display_bytes = analyze()
    if args.refresh:
        DERIVED_DIR.mkdir(parents=True, exist_ok=True)
        FULL_COORDS.write_bytes(full_bytes)
        DISPLAY_COORDS.write_bytes(display_bytes)
        MANIFEST.write_text(json.dumps(build_manifest(info), indent=2) + "\n", encoding="utf-8")
    manifest = build_manifest(info)
    committed = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if committed != manifest:
        raise ValueError("committed observational intake manifest is stale")
    if read_bytes(FULL_COORDS) != full_bytes or read_bytes(DISPLAY_COORDS) != display_bytes:
        raise ValueError("committed ALFALFA derivative differs from deterministic conversion")
    verify_registry(manifest)
    check_candidate(manifest)
    if args.format == "markdown":
        sys.stdout.write(markdown(manifest))
    else:
        print("observational dataset intake verified")
        print(json.dumps(info, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
