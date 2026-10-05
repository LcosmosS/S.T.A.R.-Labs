"""Locked implementation for REPO-CSV-v0.2:EXP-MAP-A01.

This module implements the preregistered primary arithmetic projection null test.
It deliberately excludes cosmology, SFR, TDA, and alternative mapping families.
"""

from __future__ import annotations

import argparse
from contextlib import ExitStack, contextmanager
import csv
import json
import math
import os
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

from src.data.cremona_ecdata import (
    CremonaDataError,
    load_allcurves,
    representative_records,
)


MASK64 = (1 << 64) - 1
OUTPUT_FILENAMES = (
    "observed_projection.csv",
    "null_statistics.csv",
    "summary.json",
)


class ProtocolViolation(ValueError):
    """Raised when input/configuration violates the locked preregistration."""


def _require_new_output_targets(output_dir: Path) -> None:
    if output_dir.exists() and not output_dir.is_dir():
        raise ProtocolViolation(f"output directory is not a directory: {output_dir}")
    for name in OUTPUT_FILENAMES:
        path = output_dir / name
        if path.exists() or path.is_symlink():
            raise ProtocolViolation(f"refusing to overwrite existing result: {path}")


@contextmanager
def _exclusive_output_streams(output_dir: Path):
    """Reserve every result before writing, preserving existing runner files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    with ExitStack() as stack:
        streams = {}
        try:
            for name in OUTPUT_FILENAMES:
                path = output_dir / name
                stream = stack.enter_context(
                    path.open(
                        "x",
                        encoding="utf-8",
                        newline="" if name.endswith(".csv") else None,
                    )
                )
                streams[name] = stream
        except OSError as exc:
            # Never unlink reservations: another writer may have replaced a
            # pathname even after an ownership check. Empty reservations mark
            # this failed attempt; no result bytes have been serialized yet.
            stack.close()
            raise ProtocolViolation(
                "output reservation failed before writing result data; "
                "use a fresh output directory. Empty failed reservations may "
                f"remain in {output_dir}"
            ) from exc
        yield streams


def _load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ProtocolViolation("execution config must be a JSON object")
    return value


def _require_locked_config(config: dict) -> None:
    expected = {
        "protocol_version": "EXP-MAP-A01-prereg-v1",
        "input": {
            "source_format": "ecdata-allcurves-v1",
            "source_rows": 64687,
            "analysis_rows": 38042,
            "selection": "curve_number_equals_1_per_isogeny_class",
            "allow_row_exclusion": False,
            "allow_rank_fallback": False,
            "deduplicate": "fail",
        },
        "projection": {
            "logarithm": "natural",
            "delta_max": "1e30",
            "conductor_max": "1e9",
            "longitude_scale_degrees": 360.0,
            "latitude_scale_degrees": 180.0,
            "rank_scale": 200.0,
            "clip": False,
            "regulator_used": False,
        },
        "endpoint": {
            "name": "base_knn_elevation_coherence",
            "k": 10,
            "base_metric": "euclidean",
            "neighbor_coordinates": ["longitude", "latitude"],
            "tie_break": "cremona_label_ascii",
            "undirected_edge_policy": "unique_sorted",
            "statistic": "negative_mean_absolute_elevation_difference",
            "direction": "greater_or_equal_is_more_extreme",
        },
        "null": {
            "name": "rank_permutation_fixed_base",
            "realizations": 999,
            "seed": 1729,
            "prng": "splitmix64-fisher-yates-v1",
            "preserve": [
                "curve_identities",
                "delta",
                "conductor",
                "base_coordinates",
                "rank_multiset",
                "neighbor_graph",
            ],
        },
        "inference": {
            "p_value": "(1 + count(T_null >= T_obs)) / (B + 1)",
            "alpha": 0.01,
            "sidedness": "one-sided",
            "multiple_testing": "none_single_endpoint",
        },
    }
    if config != expected:
        raise ProtocolViolation(
            "execution config does not exactly match EXP-MAP-A01-prereg-v1"
        )


def _discriminant(ainvs: tuple[int, int, int, int, int]) -> int:
    a1, a2, a3, a4, a6 = ainvs
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = (
        a1 * a1 * a6
        + 4 * a2 * a6
        - a1 * a3 * a4
        + a2 * a3 * a3
        - a4 * a4
    )
    delta = -(b2 * b2) * b8 - 8 * (b4**3) - 27 * (b6**2) + 9 * b2 * b4 * b6
    if delta == 0:
        raise ProtocolViolation("singular curve: discriminant is zero")
    return int(delta)


def load_locked_dataset(path: Path, config: dict) -> pd.DataFrame:
    try:
        source = load_allcurves(path)
        representatives = representative_records(source)
    except CremonaDataError as exc:
        raise ProtocolViolation(str(exc)) from exc

    expected_source = int(config["input"]["source_rows"])
    expected_analysis = int(config["input"]["analysis_rows"])
    if len(source) != expected_source:
        raise ProtocolViolation(
            f"unexpected source row count: expected {expected_source}, got {len(source)}"
        )
    if len(representatives) != expected_analysis:
        raise ProtocolViolation(
            "unexpected representative count: "
            f"expected {expected_analysis}, got {len(representatives)}"
        )

    source_labels = [record.label for record in source]
    if len(source_labels) != len(set(source_labels)):
        raise ProtocolViolation("duplicate Cremona curve label in source")

    rows = []
    for record in representatives:
        delta = _discriminant(record.a_invariants)
        rows.append(
            {
                "label": record.label,
                "isogeny_class": record.isogeny_class,
                "conductor": record.conductor,
                "delta": delta,
                "rank": record.rank,
                "torsion_order": record.torsion_order,
            }
        )

    result = pd.DataFrame(rows).sort_values(
        ["conductor", "isogeny_class"], kind="mergesort"
    ).reset_index(drop=True)
    if result["isogeny_class"].duplicated().any():
        raise ProtocolViolation("analysis cohort contains duplicate isogeny classes")
    return result


def project_locked(frame: pd.DataFrame, config: dict) -> pd.DataFrame:
    projection = config["projection"]
    delta_max = float(projection["delta_max"])
    conductor_max = float(projection["conductor_max"])
    rank_scale = float(projection["rank_scale"])

    longitude = np.asarray(
        [
            360.0 * math.log(abs(int(delta))) / math.log(delta_max)
            for delta in frame["delta"]
        ],
        dtype=np.float64,
    )
    latitude = np.asarray(
        [
            180.0 * math.log(int(conductor)) / math.log(conductor_max)
            for conductor in frame["conductor"]
        ],
        dtype=np.float64,
    )
    elevation = frame["rank"].to_numpy(dtype=np.float64) * rank_scale
    if not (
        np.isfinite(longitude).all()
        and np.isfinite(latitude).all()
        and np.isfinite(elevation).all()
    ):
        raise ProtocolViolation("projection produced non-finite coordinates")

    projected = frame.copy()
    projected["longitude"] = longitude
    projected["latitude"] = latitude
    projected["elevation"] = elevation
    return projected


def _neighbor_edges(projection: pd.DataFrame, k: int) -> np.ndarray:
    if k <= 0 or len(projection) <= k:
        raise ProtocolViolation("k must be positive and smaller than the sample size")

    points = projection[["longitude", "latitude"]].to_numpy(dtype=np.float64)
    labels = projection["label"].astype(str).to_numpy()
    tree = cKDTree(points)
    edges = set()

    for index, point in enumerate(points):
        distances, neighbors = tree.query(point, k=k + 1)
        pairs = [
            (float(distance), int(neighbor))
            for distance, neighbor in zip(
                np.atleast_1d(distances), np.atleast_1d(neighbors)
            )
            if int(neighbor) != index
        ]
        if len(pairs) < k:
            raise ProtocolViolation(f"unable to identify {k} neighbors for row {index}")

        kth_distance = sorted(distance for distance, _ in pairs)[k - 1]
        candidates = tree.query_ball_point(
            point, r=float(np.nextafter(kth_distance, np.inf))
        )
        ranked = []
        for neighbor in candidates:
            neighbor = int(neighbor)
            if neighbor == index:
                continue
            distance = float(np.linalg.norm(points[neighbor] - point))
            ranked.append((distance, labels[neighbor], neighbor))
        ranked.sort(key=lambda item: (item[0], item[1]))
        selected = ranked[:k]
        if len(selected) != k:
            raise ProtocolViolation(f"tie-resolved neighbor count failed for row {index}")

        for _, _, neighbor in selected:
            a, b = sorted((index, neighbor))
            edges.add((a, b))

    return np.asarray(sorted(edges), dtype=np.int64)


def _coherence_statistic(elevation: np.ndarray, edges: np.ndarray) -> float:
    if edges.ndim != 2 or edges.shape[1] != 2 or len(edges) == 0:
        raise ProtocolViolation("neighbor graph is empty or malformed")
    differences = np.abs(elevation[edges[:, 0]] - elevation[edges[:, 1]])
    return -float(np.mean(differences, dtype=np.float64))


class SplitMix64:
    def __init__(self, seed: int):
        if seed < 0 or seed > MASK64:
            raise ProtocolViolation("SplitMix64 seed must fit in uint64")
        self.state = int(seed) & MASK64

    def next_u64(self) -> int:
        self.state = (self.state + 0x9E3779B97F4A7C15) & MASK64
        z = self.state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK64
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK64
        return (z ^ (z >> 31)) & MASK64

    def randbelow(self, upper: int) -> int:
        if upper <= 0:
            raise ProtocolViolation("randbelow upper bound must be positive")
        limit = ((1 << 64) // upper) * upper
        while True:
            value = self.next_u64()
            if value < limit:
                return value % upper

    def permutation(self, size: int) -> np.ndarray:
        values = list(range(size))
        for i in range(size - 1, 0, -1):
            j = self.randbelow(i + 1)
            values[i], values[j] = values[j], values[i]
        return np.asarray(values, dtype=np.int64)


def run_protocol(input_path: Path, output_dir: Path, config: dict) -> dict:
    _require_locked_config(config)
    _require_new_output_targets(output_dir)
    frame = load_locked_dataset(input_path, config)
    projection = project_locked(frame, config)
    edges = _neighbor_edges(projection, int(config["endpoint"]["k"]))

    elevation = projection["elevation"].to_numpy(dtype=np.float64)
    observed = _coherence_statistic(elevation, edges)

    null_cfg = config["null"]
    rng = SplitMix64(int(null_cfg["seed"]))
    null_values = np.empty(int(null_cfg["realizations"]), dtype=np.float64)
    for index in range(len(null_values)):
        permutation = rng.permutation(len(elevation))
        null_values[index] = _coherence_statistic(elevation[permutation], edges)

    exceedances = int(np.count_nonzero(null_values >= observed))
    p_value = (1.0 + exceedances) / (len(null_values) + 1.0)
    alpha = float(config["inference"]["alpha"])

    summary = {
        "protocol_version": config["protocol_version"],
        "experiment_id": "EXP-MAP-A01",
        "source_rows": int(config["input"]["source_rows"]),
        "analysis_rows": int(len(frame)),
        "isogeny_policy": "curve_number_equals_1_per_isogeny_class",
        "neighbor_k": int(config["endpoint"]["k"]),
        "undirected_edge_count": int(len(edges)),
        "observed_statistic": observed,
        "null_realizations": int(len(null_values)),
        "null_seed": int(null_cfg["seed"]),
        "null_prng": null_cfg["prng"],
        "null_exceedances": exceedances,
        "p_value": p_value,
        "alpha": alpha,
        "decision": "reject_null" if p_value < alpha else "do_not_reject_null",
        "interpretation_limit": (
            "This endpoint tests local rank/elevation coherence against the locked "
            "rank-permutation null only; it does not establish ACSC or physical support."
        ),
    }
    with _exclusive_output_streams(output_dir) as streams:
        projection.to_csv(
            streams["observed_projection.csv"],
            index=False,
            quoting=csv.QUOTE_MINIMAL,
            lineterminator="\n",
            float_format="%.17g",
        )
        pd.DataFrame(
            {
                "realization": np.arange(1, len(null_values) + 1, dtype=int),
                "statistic": null_values,
            }
        ).to_csv(
            streams["null_statistics.csv"],
            index=False,
            lineterminator="\n",
            float_format="%.17g",
        )
        json.dump(summary, streams["summary.json"], indent=2, sort_keys=True)
        streams["summary.json"].write("\n")
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--config", type=Path)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    config_path = args.config
    if config_path is None:
        env_path = os.environ.get("STAR_EXECUTION_CONFIG")
        if not env_path:
            raise SystemExit("STAR_EXECUTION_CONFIG is not set and --config was omitted")
        config_path = Path(env_path)

    try:
        config = _load_config(config_path)
        run_protocol(args.input.resolve(), args.output_dir.resolve(), config)
    except (OSError, ProtocolViolation, ValueError) as exc:
        print(f"EXP-MAP-A01 protocol failure: {exc}", file=os.sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
