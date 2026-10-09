"""Prospective MCJ computation; CONTROLLED EXPERIMENT IS NOT ACTIVATED.

Internal arithmetic only. This module has deliberately no runnable full-cohort
CLI while EXP-MAP-A03 is planned. Test helpers use synthetic or known curves.
"""
from __future__ import annotations

import hashlib
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

from src.data.cremona_ecdata import load_allcurves, representative_records
from src.experiments.exp_map_a01 import SplitMix64, ProtocolViolation, _discriminant


LOCKED_SOURCE_SHA256 = "259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968"
LOCKED_SOURCE_ROWS = 64687
LOCKED_REPRESENTATIVES = 38042
K = 10
B = 999
SEED = 4103
ALPHA = 0.005


class MCJProtocolError(ValueError):
    """Invalid source, arithmetic or prospective protocol state."""


def c4_from_ainvariants(ainvs: tuple[int, int, int, int, int]) -> int:
    a1, a2, a3, a4, _a6 = (int(x) for x in ainvs)
    b2 = a1 * a1 + 4 * a2
    b4 = a1 * a3 + 2 * a4
    return b2 * b2 - 24 * b4


def project_arithmetic(ainvs: tuple[int, int, int, int, int], conductor: int):
    """Return (ln N, Re log j, Im log j), or None for exactly j=0.

    c4 and Delta are exact Python integers, so a very large j never needs to
    be converted to float. For real rational nonzero j the principal argument
    is precisely 0 or +pi, never a fitted phase.
    """
    # A singular curve must abort, never be classified as a j=0 exclusion.
    # Validate N even when c4=0, to avoid silently omitting invalid inputs.
    # The shared A01 exact discriminant helper already rejects singular curves.
    # Translate its abort into this module's explicitly declared failure type.
    try:
        delta = _discriminant(ainvs)
    except ProtocolViolation as exc:
        raise MCJProtocolError("zero discriminant: singular elliptic curve") from exc
    if delta == 0:  # Defensive invariant if the shared helper changes.
        raise MCJProtocolError("zero discriminant: singular elliptic curve")
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


def load_locked_arithmetic(path: Path):
    source = Path(path)
    if hashlib.sha256(source.read_bytes()).hexdigest() != LOCKED_SOURCE_SHA256:
        raise MCJProtocolError("source SHA-256 mismatch")
    records = load_allcurves(source)
    if len(records) != LOCKED_SOURCE_ROWS:
        raise MCJProtocolError("source row-count mismatch")
    labels = [r.label for r in records]
    if len(labels) != len(set(labels)):
        raise MCJProtocolError("duplicate curve label")
    reps = representative_records(records)
    if len(reps) != LOCKED_REPRESENTATIVES:
        raise MCJProtocolError("source representative count mismatch")
    kept = []
    excluded = []
    for rec in reps:
        # This exclusion is decided by a-invariants, conductor and exact Delta,
        # before this function ever inspects rec.rank.
        point = project_arithmetic(rec.a_invariants, rec.conductor)
        if point is None:
            excluded.append({"label": rec.label, "reason": "j_exactly_zero"})
            continue
        kept.append({"label": rec.label, "conductor": rec.conductor,
                     "delta": _discriminant(rec.a_invariants),
                     "c4": c4_from_ainvariants(rec.a_invariants),
                     "x": point[0], "y": point[1], "z": point[2],
                     "rank": rec.rank})
    frame = pd.DataFrame(kept).sort_values(
        ["conductor", "label"], kind="mergesort").reset_index(drop=True)
    exclusions = pd.DataFrame(excluded, columns=["label", "reason"])
    if len(frame) + len(exclusions) != LOCKED_REPRESENTATIVES or len(frame) <= K:
        raise MCJProtocolError("unexpected eligible cohort")
    return frame, exclusions


def mcj_neighbor_edges(frame: pd.DataFrame, k: int = K) -> np.ndarray:
    """Exact stated tie policy on the binary64 3D coordinates; rank-blind."""
    if k != K:
        raise MCJProtocolError("MCJ k=10 is locked")
    p = frame[["x", "y", "z"]].to_numpy(dtype=np.float64)
    labels = frame["label"].astype(str).tolist()
    if len(p) <= k or len(set(labels)) != len(labels) or not np.isfinite(p).all():
        raise MCJProtocolError("invalid MCJ graph input")
    tree = cKDTree(p)
    edges = set()
    for i, point in enumerate(p):
        distances, ids = tree.query(point, k=k+1)
        initial = sorted(float(d) for d,j in zip(np.atleast_1d(distances),np.atleast_1d(ids)) if int(j) != i)
        if len(initial) < k or not math.isfinite(initial[k-1]):
            raise MCJProtocolError("missing neighbors")
        candidates = tree.query_ball_point(point, r=float(np.nextafter(initial[k-1], np.inf)))
        ranks = []
        for j in candidates:
            j = int(j)
            if j == i: continue
            diff = p[j] - point
            d2 = float(np.dot(diff, diff))
            if not math.isfinite(d2): raise MCJProtocolError("nonfinite squared distance")
            ranks.append((d2, labels[j], j))
        ranks.sort(key=lambda x: (x[0], x[1]))
        if len(ranks) < k:
            raise MCJProtocolError("incomplete neighbor enumeration")
        for _, _, j in ranks[:k]:
            edges.add(tuple(sorted((i,j))))
    result = np.asarray(sorted(edges), dtype=np.int64)
    if result.ndim != 2 or result.shape[1] != 2:
        raise MCJProtocolError("empty MCJ graph")
    return result


def rank_coherence(ranks: np.ndarray, edges: np.ndarray) -> float:
    if edges.ndim != 2 or edges.shape[1] != 2 or len(edges) == 0:
        raise MCJProtocolError("invalid edges")
    return -float(np.mean(np.abs(ranks[edges[:, 0]] - ranks[edges[:, 1]])))


def decile_groups(frame: pd.DataFrame) -> list[np.ndarray]:
    """Groups require ascending (N, ASCII label) ordering, not rank sorting."""
    if len(frame) < 10:
        raise MCJProtocolError("too few curves for ten strata")
    keys = list(zip(frame["conductor"].astype(int), frame["label"].astype(str)))
    if keys != sorted(keys):
        raise MCJProtocolError("input not in frozen conductor-label order")
    size = len(frame)
    return [np.asarray([i for i in range(size) if 10*i//size == j], dtype=np.int64)
            for j in range(10)]


def controlled_calculation_is_disabled(*_args, **_kwargs):
    raise MCJProtocolError(
        "EXP-MAP-A03 remains planned. Canonical preregistration, code/spec "
        "hash binding and an independent activation PR are required before "
        "running all 999 null realizations or publishing an experiment result."
    )


def fixture_null_statistics(frame: pd.DataFrame, *, k: int = K,
                            draws: int = 3, seed: int = SEED):
    """Test-only null fixture, NOT a reportable or controlled experiment."""
    if draws < 1 or draws > 3 or seed != SEED:
        raise MCJProtocolError("only a short fixed-seed fixture is permitted")
    edges = mcj_neighbor_edges(frame, k)
    ranks = frame["rank"].to_numpy(dtype=np.float64)
    groups = decile_groups(frame)
    rng = SplitMix64(seed)
    observed = rank_coherence(ranks, edges)
    null = []
    for _ in range(draws):
        trial = ranks.copy()
        for group in groups:
            trial[group] = ranks[group][rng.permutation(len(group))]
        null.append(rank_coherence(trial, edges))
    return observed, np.asarray(null, dtype=np.float64)


def main() -> int:
    controlled_calculation_is_disabled()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
