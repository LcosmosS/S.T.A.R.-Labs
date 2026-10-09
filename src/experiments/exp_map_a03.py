"""Locked implementation for REPO-CSV-v0.2:EXP-MAP-A03.

This module implements the preregistered MCJ conditional rank-coherence null
test. Committing it does not authorize execution; controlled eligibility is a
separate registry gate.
"""
from __future__ import annotations

import argparse
from contextlib import ExitStack, contextmanager
import csv
import hashlib
import json
import math
import os
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

from src.data.cremona_ecdata import load_allcurves, representative_records
from src.experiments.exp_map_a01 import SplitMix64, ProtocolViolation, _discriminant


LOCKED_SOURCE_SHA256 = "259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968"
LOCKED_SOURCE_ROWS = 64687
LOCKED_REPRESENTATIVES = 38042
LOCKED_J_ZERO_EXCLUSIONS = 106
LOCKED_ANALYSIS_ROWS = 37936
K = 10
B = 999
SEED = 4103
ALPHA = 0.005
OUTPUT_FILENAMES = (
    "summary.json",
    "observed_mcj_projection.csv",
    "null_statistics.csv",
    "exclusions_j_zero.csv",
)
LOCKED_CONFIG = json.loads(r'''{
  "schema_version": "1.0",
  "protocol_version": "EXP-MAP-A03-prereg-v1",
  "experiment_id": "EXP-MAP-A03",
  "qualified_experiment_id": "REPO-CSV-v0.2:EXP-MAP-A03",
  "claim_ids": [
    "CLAIM-ACSC-002"
  ],
  "dataset_id": "DATA-ARITHMETIC",
  "parameter_set_id": "PAR-MAP-003",
  "null_id": "NULL-MAP-003",
  "scientific_scope": "internal rank-coherence test of a BSD-independent j-invariant/conductor graph; NO cosmological data or physical support",
  "input": {
    "manifest": "preregistrations/EXP-MAP-A03/dataset_manifest.json",
    "source": "data/ecdata/allcurves/allcurves.00000-09999",
    "source_format": "ecdata-allcurves-v1",
    "source_schema": [
      "conductor",
      "isogeny",
      "curve_number",
      "a_invariants",
      "rank",
      "torsion_order"
    ],
    "source_sha256": "259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968",
    "source_rows": 64687,
    "source_gitlink": "25cec5ecfec8b9f016eb1631ac633194c2bed39f",
    "representative_policy": "curve_number_equals_1_per_isogeny_class",
    "representative_rows": 38042,
    "j_zero_exclusions": 106,
    "analysis_rows": 37936,
    "analysis_selection": "curve_number_equals_1_per_isogeny_class_then_exclude_exact_j_equals_zero_before_rank_use",
    "sort": "conductor_ascending_then_ascii_label",
    "nonfinite_policy": "fail",
    "duplicate_labels": "fail",
    "singular_curves": "fail",
    "post_hoc_filtering": false
  },
  "arithmetic": {
    "b2": "a1*a1+4*a2",
    "b4": "a1*a3+2*a4",
    "b6": "a3*a3+4*a6",
    "b8": "a1*a1*a6+4*a2*a6-a1*a3*a4+a2*a3*a3-a4*a4",
    "c4": "b2*b2-24*b4",
    "delta": "-b2*b2*b8-8*b4*b4*b4-27*b6*b6+9*b2*b4*b6",
    "j": "c4^3/delta",
    "exact_until_logs": true
  },
  "mapping": {
    "x": "ln(N)",
    "y": "3*ln(abs(c4))-ln(abs(delta))",
    "z": "0 if j>0 else pi if j<0",
    "logarithm": "natural",
    "complex_branch": "principal_negative_real_argument_plus_pi",
    "units": "dimensionless",
    "numeric_geometry": "IEEE-754-binary64",
    "normalization": "none",
    "clipping": false,
    "jitter": false,
    "fitting": false,
    "regulator_used": false,
    "rank_used_in_embedding": false,
    "j_zero_policy": "exclude_before_graph_and_before_rank_use; require exactly 106",
    "j_negative_policy": "principal complex logarithm with argument +pi"
  },
  "endpoint": {
    "name": "mcj_knn_rank_coherence",
    "k": 10,
    "metric": "euclidean_xyz_binary64",
    "neighbor_coordinates": [
      "x",
      "y",
      "z"
    ],
    "ties": "ascending squared_euclidean_distance_binary64 then ASCII_Cremona_label",
    "coordinate_duplicates": "retain_and_resolve_by_same_tie_rule",
    "self_neighbors": "exclude",
    "undirected_edges": "unique_sorted_pairs",
    "statistic": "T_obs = - mean_over_edges(abs(rank_i-rank_j))",
    "direction": "greater_is_more_rank_coherence"
  },
  "null": {
    "name": "conductor_decile_stratified_rank_permutation_fixed_graph",
    "strata": 10,
    "stratification": "accepted rows sorted by (conductor,label_ASCII); stratum=floor(10*i/n), i zero-based",
    "preserved": [
      "curve_identity",
      "conductor",
      "c4",
      "delta",
      "j_status",
      "embedding",
      "graph_edges",
      "rank_multiset_within_each_stratum"
    ],
    "seed": 4103,
    "algorithm": "splitmix64-fisher-yates-v1",
    "splitmix64": {
      "word_bits": 64,
      "increment_hex": "0x9E3779B97F4A7C15",
      "multiplier_1_hex": "0xBF58476D1CE4E5B9",
      "multiplier_2_hex": "0x94D049BB133111EB",
      "randbelow": "rejection_below_floor_2^64_over_upper_times_upper_then_mod_upper",
      "fisher_yates": "for i=size-1 down to 1 draw j=randbelow(i+1) and swap i,j"
    },
    "draw_order": "b=1..999; within each b strata 0..9; original observed ranks permuted independently within each stratum; one continuing RNG stream; no reset between strata or draws",
    "realizations": 999,
    "rerolls": false
  },
  "inference": {
    "alpha": 0.005,
    "sidedness": "one_sided_greater",
    "pvalue": "(1 + count(T_b>=T_obs))/(999+1)",
    "decision": "reject_null_iff_p_value_less_than_alpha",
    "primary_endpoint_count": 1,
    "multiple_testing": "none_single_endpoint",
    "report_effect": "T_obs - median(T_null)",
    "interpretation": "conditional internal arithmetic evidence only; no cosmological or physical-support inference"
  },
  "outputs": [
    "summary.json",
    "observed_mcj_projection.csv",
    "null_statistics.csv",
    "exclusions_j_zero.csv"
  ],
  "controls": {
    "controlled_execution_eligible": false,
    "controlled_support_eligible": false,
    "physical_support_eligible": false,
    "no_run_without_separate_activation": true
  }
}''')


class MCJProtocolError(ValueError):
    """Input, arithmetic, configuration, or output violates A03 preregistration."""


def _load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise MCJProtocolError("execution config must be a JSON object")
    return value


def _require_locked_config(config: dict) -> None:
    if config != LOCKED_CONFIG:
        raise MCJProtocolError(
            "execution config does not exactly match EXP-MAP-A03-prereg-v1"
        )


def _require_new_output_targets(output_dir: Path) -> None:
    if output_dir.exists() and not output_dir.is_dir():
        raise MCJProtocolError(f"output directory is not a directory: {output_dir}")
    for name in OUTPUT_FILENAMES:
        path = output_dir / name
        if path.exists() or path.is_symlink():
            raise MCJProtocolError(f"refusing to overwrite existing result: {path}")


@contextmanager
def _exclusive_output_streams(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    with ExitStack() as stack:
        streams = {}
        try:
            for name in OUTPUT_FILENAMES:
                streams[name] = stack.enter_context(
                    (output_dir / name).open(
                        "x",
                        encoding="utf-8",
                        newline="" if name.endswith(".csv") else None,
                    )
                )
        except OSError as exc:
            stack.close()
            raise MCJProtocolError(
                "output reservation failed before writing result data; "
                "use a fresh output directory. Empty failed reservations may remain."
            ) from exc
        yield streams


def c4_from_ainvariants(ainvs: tuple[int, int, int, int, int]) -> int:
    a1, a2, a3, a4, _a6 = (int(x) for x in ainvs)
    b2 = a1 * a1 + 4 * a2
    b4 = a1 * a3 + 2 * a4
    return int(b2 * b2 - 24 * b4)


def project_arithmetic(ainvs: tuple[int, int, int, int, int], conductor: int):
    try:
        delta = _discriminant(ainvs)
    except ProtocolViolation as exc:
        raise MCJProtocolError("zero discriminant: singular elliptic curve") from exc
    if conductor <= 0:
        raise MCJProtocolError("conductor must be positive")
    c4 = c4_from_ainvariants(ainvs)
    if c4 == 0:
        return None
    x = math.log(int(conductor))
    y = 3 * math.log(abs(c4)) - math.log(abs(delta))
    z = 0.0 if (c4 > 0) == (delta > 0) else math.pi
    if not all(math.isfinite(v) for v in (x, y, z)):
        raise MCJProtocolError("nonfinite MCJ projection")
    return x, y, z


def load_locked_arithmetic(path: Path, config: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    _require_locked_config(config)
    source = Path(path)
    if hashlib.sha256(source.read_bytes()).hexdigest() != LOCKED_SOURCE_SHA256:
        raise MCJProtocolError("source SHA-256 mismatch")
    records = load_allcurves(source)
    if len(records) != LOCKED_SOURCE_ROWS:
        raise MCJProtocolError("source row-count mismatch")
    labels = [record.label for record in records]
    if len(labels) != len(set(labels)):
        raise MCJProtocolError("duplicate curve label")
    reps = representative_records(records)
    if len(reps) != LOCKED_REPRESENTATIVES:
        raise MCJProtocolError("source representative count mismatch")

    kept, excluded = [], []
    for rec in reps:
        point = project_arithmetic(rec.a_invariants, rec.conductor)
        if point is None:
            excluded.append({
                "label": rec.label,
                "isogeny_class": rec.isogeny_class,
                "conductor": rec.conductor,
                "reason": "j_exactly_zero",
            })
            continue
        kept.append({
            "label": rec.label,
            "isogeny_class": rec.isogeny_class,
            "conductor": rec.conductor,
            "delta": _discriminant(rec.a_invariants),
            "c4": c4_from_ainvariants(rec.a_invariants),
            "x": point[0],
            "y": point[1],
            "z": point[2],
            "rank": rec.rank,
        })

    frame = pd.DataFrame(kept).sort_values(
        ["conductor", "label"], kind="mergesort"
    ).reset_index(drop=True)
    exclusions = pd.DataFrame(
        excluded, columns=["label", "isogeny_class", "conductor", "reason"]
    ).sort_values(["conductor", "label"], kind="mergesort").reset_index(drop=True)

    if len(exclusions) != LOCKED_J_ZERO_EXCLUSIONS:
        raise MCJProtocolError("unexpected j=0 exclusion count")
    if len(frame) != LOCKED_ANALYSIS_ROWS:
        raise MCJProtocolError("unexpected analysis row count")
    if len(frame) + len(exclusions) != LOCKED_REPRESENTATIVES:
        raise MCJProtocolError("representative accounting mismatch")
    if frame["label"].duplicated().any() or frame["isogeny_class"].duplicated().any():
        raise MCJProtocolError("accepted cohort contains duplicate identity")
    if not np.isfinite(frame[["x", "y", "z"]].to_numpy(dtype=np.float64)).all():
        raise MCJProtocolError("accepted cohort contains nonfinite coordinate")
    return frame, exclusions


def mcj_neighbor_edges(frame: pd.DataFrame, k: int = K) -> np.ndarray:
    if k != K:
        raise MCJProtocolError("MCJ k=10 is locked")
    points = frame[["x", "y", "z"]].to_numpy(dtype=np.float64)
    labels = frame["label"].astype(str).tolist()
    if len(points) <= k or len(set(labels)) != len(labels) or not np.isfinite(points).all():
        raise MCJProtocolError("invalid MCJ graph input")
    tree = cKDTree(points)
    edges = set()
    for i, point in enumerate(points):
        distances, ids = tree.query(point, k=k + 1)
        initial = sorted(
            float(distance)
            for distance, neighbor in zip(np.atleast_1d(distances), np.atleast_1d(ids))
            if int(neighbor) != i
        )
        if len(initial) < k or not math.isfinite(initial[k - 1]):
            raise MCJProtocolError("missing neighbors")
        candidates = tree.query_ball_point(
            point, r=float(np.nextafter(initial[k - 1], np.inf))
        )
        ranked = []
        for neighbor in candidates:
            neighbor = int(neighbor)
            if neighbor == i:
                continue
            diff = points[neighbor] - point
            distance2 = float(np.dot(diff, diff))
            if not math.isfinite(distance2):
                raise MCJProtocolError("nonfinite squared distance")
            ranked.append((distance2, labels[neighbor], neighbor))
        ranked.sort(key=lambda item: (item[0], item[1]))
        if len(ranked) < k:
            raise MCJProtocolError("incomplete neighbor enumeration")
        for _, _, neighbor in ranked[:k]:
            edges.add(tuple(sorted((i, neighbor))))
    result = np.asarray(sorted(edges), dtype=np.int64)
    if result.ndim != 2 or result.shape[1] != 2 or len(result) == 0:
        raise MCJProtocolError("empty MCJ graph")
    return result


def rank_coherence(ranks: np.ndarray, edges: np.ndarray) -> float:
    if edges.ndim != 2 or edges.shape[1] != 2 or len(edges) == 0:
        raise MCJProtocolError("invalid edges")
    ranks = np.asarray(ranks, dtype=np.int64)
    value = -float(
        np.mean(np.abs(ranks[edges[:, 0]] - ranks[edges[:, 1]]), dtype=np.float64)
    )
    if not math.isfinite(value):
        raise MCJProtocolError("nonfinite coherence statistic")
    return value


def decile_groups(frame: pd.DataFrame) -> list[np.ndarray]:
    if len(frame) < 10:
        raise MCJProtocolError("too few curves for ten strata")
    keys = list(zip(frame["conductor"].astype(int), frame["label"].astype(str)))
    if keys != sorted(keys):
        raise MCJProtocolError("input not in frozen conductor-label order")
    size = len(frame)
    groups = [
        np.asarray([i for i in range(size) if 10 * i // size == s], dtype=np.int64)
        for s in range(10)
    ]
    if any(len(group) == 0 for group in groups):
        raise MCJProtocolError("empty conductor-order stratum")
    return groups


def _null_statistics_core(ranks, edges, groups, *, draws: int, seed: int) -> np.ndarray:
    rng = SplitMix64(seed)
    observed_ranks = np.asarray(ranks, dtype=np.int64)
    values = np.empty(draws, dtype=np.float64)
    for draw in range(draws):
        trial = observed_ranks.copy()
        for group in groups:
            trial[group] = observed_ranks[group][rng.permutation(len(group))]
        values[draw] = rank_coherence(trial, edges)
    return values


def full_null_statistics(frame: pd.DataFrame, edges: np.ndarray, config: dict) -> np.ndarray:
    _require_locked_config(config)
    return _null_statistics_core(
        frame["rank"].to_numpy(dtype=np.int64),
        edges,
        decile_groups(frame),
        draws=B,
        seed=SEED,
    )


def fixture_null_statistics(frame: pd.DataFrame, *, k: int = K, draws: int = 3, seed: int = SEED):
    if draws < 1 or draws > 3 or seed != SEED:
        raise MCJProtocolError("only a short fixed-seed fixture is permitted")
    edges = mcj_neighbor_edges(frame, k)
    ranks = frame["rank"].to_numpy(dtype=np.int64)
    return (
        rank_coherence(ranks, edges),
        _null_statistics_core(ranks, edges, decile_groups(frame), draws=draws, seed=seed),
    )


def run_protocol(input_path: Path, output_dir: Path, config: dict) -> dict:
    _require_locked_config(config)
    _require_new_output_targets(output_dir)
    frame, exclusions = load_locked_arithmetic(input_path, config)
    edges = mcj_neighbor_edges(frame, K)
    ranks = frame["rank"].to_numpy(dtype=np.int64)
    observed = rank_coherence(ranks, edges)
    null_values = full_null_statistics(frame, edges, config)
    groups = decile_groups(frame)
    exceedances = int(np.count_nonzero(null_values >= observed))
    p_value = (1.0 + exceedances) / (B + 1.0)
    summary = {
        "protocol_version": "EXP-MAP-A03-prereg-v1",
        "experiment_id": "EXP-MAP-A03",
        "source_rows": LOCKED_SOURCE_ROWS,
        "representative_rows": LOCKED_REPRESENTATIVES,
        "j_zero_exclusion_count": len(exclusions),
        "analysis_rows": len(frame),
        "neighbor_k": K,
        "undirected_edge_count": len(edges),
        "observed_statistic": observed,
        "null_realizations": B,
        "null_seed": SEED,
        "null_prng": "splitmix64-fisher-yates-v1",
        "null_strata": 10,
        "stratum_sizes": [len(group) for group in groups],
        "null_exceedances": exceedances,
        "p_value": p_value,
        "alpha": ALPHA,
        "sidedness": "one_sided_greater",
        "decision_rule": "reject_null_iff_p_value_less_than_alpha",
        "decision": "reject_null" if p_value < ALPHA else "do_not_reject_null",
        "effect_t_obs_minus_null_median": observed - float(np.median(null_values)),
        "interpretation_limit": (
            "Internal arithmetic conditional-permutation evidence only; "
            "no cosmological correspondence, ACSC physical support, or BSD claim."
        ),
    }
    with _exclusive_output_streams(output_dir) as streams:
        frame[
            ["label","isogeny_class","conductor","delta","c4","x","y","z","rank"]
        ].to_csv(
            streams["observed_mcj_projection.csv"],
            index=False, quoting=csv.QUOTE_MINIMAL, lineterminator="\n",
            float_format="%.17g",
        )
        pd.DataFrame({
            "realization": np.arange(1, B + 1, dtype=int),
            "statistic": null_values,
        }).to_csv(
            streams["null_statistics.csv"],
            index=False, lineterminator="\n", float_format="%.17g",
        )
        exclusions.to_csv(
            streams["exclusions_j_zero.csv"],
            index=False, quoting=csv.QUOTE_MINIMAL, lineterminator="\n",
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
        run_protocol(args.input.resolve(), args.output_dir.resolve(), _load_config(config_path))
    except (OSError, MCJProtocolError, ValueError) as exc:
        print(f"EXP-MAP-A03 protocol failure: {exc}", file=os.sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
