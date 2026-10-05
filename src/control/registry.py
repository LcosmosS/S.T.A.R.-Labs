"""Resolve controlled-experiment registry records and execution gates."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path


ALLOWED_READY_EVIDENCE_STATUSES = {"controlled", "derived"}
ALLOWED_PREREGISTRATION_STATUSES = {"preregistered", "locked"}
_SHA256_RE = re.compile(r"(?i)\bsha256\s*[:=]\s*([0-9a-f]{64})\b")


class RegistryError(ValueError):
    """Raised when controlled registry state is missing or inconsistent."""


def canonical_json_bytes(value) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def record_sha256(record: dict[str, str]) -> str:
    return hashlib.sha256(canonical_json_bytes(record)).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def extract_integrity_sha256s(value: str) -> set[str]:
    return {match.lower() for match in _SHA256_RE.findall(value or "")}


def _truth(value) -> bool:
    return str(value).strip().lower() == "true"


def _rows(
    path: Path, required_fields: tuple[str, ...] = ()
) -> list[dict[str, str]]:
    try:
        with path.open(newline="", encoding="utf-8-sig") as stream:
            reader = csv.DictReader(stream, strict=True)
            fields = reader.fieldnames
            if (
                not fields
                or any(not field.strip() for field in fields)
                or len(fields) != len(set(fields))
                or not set(required_fields).issubset(fields)
            ):
                raise RegistryError(f"{path.name} has invalid registry headers")
            rows = []
            for row in reader:
                if None in row or any(value is None for value in row.values()):
                    raise RegistryError(
                        f"{path.name} has a malformed row at line {reader.line_num}"
                    )
                rows.append(row)
            return rows
    except (OSError, UnicodeError, csv.Error) as exc:
        raise RegistryError(
            f"cannot read controlled registry {path.name}: {exc}"
        ) from exc


def _index_unique(
    rows: list[dict[str, str]],
    key: str,
    source_name: str,
) -> dict[str, dict[str, str]]:
    result = {}
    for row in rows:
        value = row.get(key, "").strip()
        if not value:
            raise RegistryError(f"{source_name} contains an empty {key}")
        if value in result:
            raise RegistryError(f"{source_name} contains duplicate {key}: {value}")
        result[value] = row
    return result


def _crosswalk_pairs(
    rows: list[dict[str, str]],
    source_name: str,
    claims: dict[str, dict[str, str]],
    experiments: dict[str, dict[str, str]],
) -> frozenset[tuple[str, str]]:
    pairs = set()
    for row in rows:
        claim_id = row["Claim_ID"].strip()
        experiment_id = row["Experiment_ID"].strip()
        if not claim_id or not experiment_id:
            raise RegistryError(
                f"{source_name} contains an empty Claim_ID/Experiment_ID"
            )
        if claim_id not in claims:
            raise RegistryError(f"{source_name} contains unknown Claim_ID: {claim_id}")
        if experiment_id not in experiments:
            raise RegistryError(
                f"{source_name} contains unknown Experiment_ID: {experiment_id}"
            )
        pair = (claim_id, experiment_id)
        if pair in pairs:
            raise RegistryError(
                f"{source_name} contains duplicate claim/experiment pair: "
                f"{claim_id}/{experiment_id}"
            )
        pairs.add(pair)
    return frozenset(pairs)


@dataclass(frozen=True)
class ResolvedExperiment:
    experiment: dict[str, str]
    dataset: dict[str, str]
    provenance: dict[str, str]
    parameter: dict[str, str]
    null: dict[str, str]
    claims: dict[str, dict[str, str]]
    claim_experiments: frozenset[tuple[str, str]]

    @property
    def records(self) -> dict[str, dict[str, str]]:
        # Claim registries are bound by snapshot file hashes outside this schema.
        return {
            "experiment": self.experiment,
            "dataset": self.dataset,
            "provenance": self.provenance,
            "parameter": self.parameter,
            "null": self.null,
        }

    @property
    def record_hashes(self) -> dict[str, str]:
        return {
            name: record_sha256(record)
            for name, record in self.records.items()
        }


@dataclass(frozen=True)
class RegistrySnapshot:
    root: Path
    registry_dir: Path
    experiments: dict[str, dict[str, str]]
    datasets: dict[str, dict[str, str]]
    provenance: dict[str, dict[str, str]]
    parameters: dict[str, dict[str, str]]
    nulls: dict[str, dict[str, str]]
    claims: dict[str, dict[str, str]]
    claim_experiments: frozenset[tuple[str, str]]
    file_hashes: dict[str, str]

    FILES = {
        "experiments": "experiment_registry_v0.2.csv",
        "datasets": "dataset_registry_v0.1.csv",
        "provenance": "data_provenance_registry_v0.1.csv",
        "parameters": "parameter_registry_v0.1.csv",
        "nulls": "null_registry_v0.1.csv",
        "claims": "claim_evidence_v0.2.csv",
        "claim_experiments": "claim_experiment_crosswalk_v0.2.csv",
    }

    @classmethod
    def load(cls, root: Path | str = ".") -> "RegistrySnapshot":
        root = Path(root).resolve()
        registry_dir = root / "registry"
        paths = {
            name: registry_dir / filename
            for name, filename in cls.FILES.items()
        }
        missing = [str(path) for path in paths.values() if not path.is_file()]
        if missing:
            raise RegistryError(
                "missing controlled registry file(s): " + ", ".join(missing)
            )

        experiment_rows = _rows(paths["experiments"])
        dataset_rows = _rows(paths["datasets"])
        provenance_rows = _rows(paths["provenance"])
        parameter_rows = _rows(paths["parameters"])
        null_rows = _rows(paths["nulls"])
        claim_rows = _rows(paths["claims"], ("Claim_ID",))
        crosswalk_rows = _rows(
            paths["claim_experiments"], ("Claim_ID", "Experiment_ID")
        )
        experiments = _index_unique(
            experiment_rows, "Experiment_ID", cls.FILES["experiments"]
        )
        claims = _index_unique(claim_rows, "Claim_ID", cls.FILES["claims"])

        return cls(
            root=root,
            registry_dir=registry_dir,
            experiments=experiments,
            datasets=_index_unique(
                dataset_rows,
                "Dataset_ID",
                cls.FILES["datasets"],
            ),
            provenance=_index_unique(
                provenance_rows,
                "Dataset_ID",
                cls.FILES["provenance"],
            ),
            parameters=_index_unique(
                parameter_rows,
                "Parameter_Set_ID",
                cls.FILES["parameters"],
            ),
            nulls=_index_unique(
                null_rows,
                "Null_ID",
                cls.FILES["nulls"],
            ),
            claims=claims,
            claim_experiments=_crosswalk_pairs(
                crosswalk_rows,
                cls.FILES["claim_experiments"],
                claims,
                experiments,
            ),
            file_hashes={
                cls.FILES[name]: file_sha256(path)
                for name, path in paths.items()
            },
        )

    def resolve(self, experiment_id: str) -> ResolvedExperiment:
        try:
            experiment = self.experiments[experiment_id]
        except KeyError as exc:
            raise RegistryError(
                f"unknown controlled Experiment_ID: {experiment_id}"
            ) from exc

        dataset_id = experiment.get("Dataset_ID", "").strip()
        parameter_id = experiment.get("Parameter_Set_ID", "").strip()
        null_id = experiment.get("Null_ID", "").strip()

        try:
            dataset = self.datasets[dataset_id]
        except KeyError as exc:
            raise RegistryError(
                f"{experiment_id}: unknown Dataset_ID {dataset_id!r}"
            ) from exc
        try:
            provenance = self.provenance[dataset_id]
        except KeyError as exc:
            raise RegistryError(
                f"{experiment_id}: missing provenance for {dataset_id!r}"
            ) from exc
        try:
            parameter = self.parameters[parameter_id]
        except KeyError as exc:
            raise RegistryError(
                f"{experiment_id}: unknown Parameter_Set_ID {parameter_id!r}"
            ) from exc
        try:
            null = self.nulls[null_id]
        except KeyError as exc:
            raise RegistryError(
                f"{experiment_id}: unknown Null_ID {null_id!r}"
            ) from exc

        return ResolvedExperiment(
            experiment=experiment,
            dataset=dataset,
            provenance=provenance,
            parameter=parameter,
            null=null,
            claims=self.claims,
            claim_experiments=self.claim_experiments,
        )


def execution_gate_failures(resolved: ResolvedExperiment) -> list[str]:
    """Return reasons an experiment may not enter the controlled runner."""
    failures = []
    experiment = resolved.experiment
    dataset = resolved.dataset
    provenance = resolved.provenance
    parameter = resolved.parameter
    null = resolved.null
    experiment_id = experiment.get("Experiment_ID", "<unknown>")

    if experiment.get("Mode") != "controlled":
        failures.append(f"{experiment_id}: Mode must be controlled")
    if not experiment.get("Claim_IDs", "").strip():
        failures.append(f"{experiment_id}: Claim_IDs must be explicitly bound")
    else:
        seen_claims = set()
        for value in experiment["Claim_IDs"].split(";"):
            claim_id = value.strip()
            if not claim_id:
                failures.append(
                    f"{experiment_id}: Claim_IDs contains an empty Claim_ID"
                )
            elif claim_id in seen_claims:
                failures.append(f"{experiment_id}: duplicate Claim_ID {claim_id!r}")
            elif claim_id not in resolved.claims:
                failures.append(f"{experiment_id}: unknown Claim_ID {claim_id!r}")
            elif (claim_id, experiment_id) not in resolved.claim_experiments:
                failures.append(
                    f"{experiment_id}: missing claim/experiment crosswalk pair "
                    f"{claim_id}/{experiment_id}"
                )
            seen_claims.add(claim_id)
    namespace_resolution = experiment.get("Namespace_Resolution", "").strip()
    if not namespace_resolution or "pending" in namespace_resolution.lower():
        failures.append(f"{experiment_id}: namespace resolution is not closed")
    if not _truth(experiment.get("Controlled_Execution_Eligible", "false")):
        failures.append(
            f"{experiment_id}: experiment is not controlled-execution eligible"
        )
    if not _truth(dataset.get("Controlled_Execution_Eligible", "false")):
        failures.append(
            f"{experiment_id}: dataset is not controlled-execution eligible"
        )
    if provenance.get("Provenance_Status") != "verified":
        failures.append(f"{experiment_id}: provenance is not verified")
    if provenance.get("Evidence_Status") not in ALLOWED_READY_EVIDENCE_STATUSES:
        failures.append(
            f"{experiment_id}: provenance evidence status "
            f"{provenance.get('Evidence_Status')!r} is not accepted"
        )
    if parameter.get("Preregistration_Status") not in ALLOWED_PREREGISTRATION_STATUSES:
        failures.append(
            f"{experiment_id}: parameter set is not preregistered/locked"
        )
    if null.get("Preregistration_Status") not in ALLOWED_PREREGISTRATION_STATUSES:
        failures.append(
            f"{experiment_id}: null model is not preregistered/locked"
        )

    integrity = extract_integrity_sha256s(
        provenance.get("Integrity_Check", "")
    )
    if not integrity:
        failures.append(
            f"{experiment_id}: verified provenance has no explicit SHA256 "
            "integrity digest"
        )

    return failures
