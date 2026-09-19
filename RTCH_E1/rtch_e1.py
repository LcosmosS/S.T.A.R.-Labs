#!/usr/bin/env python3
"""
RTCH-E1: Arithmetic–Geodesic–Cohomological Test

Complete local experiment.

Modes:
  demo      synthetic sanity check
  download  query LMFDB ec_curvedata API
  analyze   run topology/null/geodesic/scalar/prediction pipeline

The program is deliberately conservative:
- rank is NOT part of the primary topology metric;
- topology is compared with matched nulls;
- H1/H2/H3 are reported as persistent features of the sampled metric space;
- graph shortest paths are used as empirical geodesics;
- scalar coordinates are treated as candidate coordinates, not "invariants",
  unless they survive the stated validation tests.
"""

from __future__ import annotations
import argparse
import json
import math
import os
import sys
import time
import hashlib
import warnings
from dataclasses import dataclass, asdict, replace
from pathlib import Path
from typing import Iterable, Optional

import numpy as np
import pandas as pd
import requests

from sklearn.preprocessing import RobustScaler
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline

from scipy import sparse
from scipy.sparse.csgraph import dijkstra, connected_components, shortest_path
from scipy.spatial.distance import pdist, squareform
from scipy.stats import spearmanr, pearsonr

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    from ripser import ripser
    HAVE_RIPSER = True
except Exception:
    HAVE_RIPSER = False

warnings.filterwarnings("ignore")


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

FEATURE_SETS = {
    "intrinsic": [
        "log_conductor",
        "signed_log_discriminant",
        "log_abs_j",
        "faltings_height",
        "log_regulator",
    ],
    "no_regulator": [
        "log_conductor",
        "signed_log_discriminant",
        "log_abs_j",
        "faltings_height",
    ],
    "minimal": [
        "log_conductor",
        "signed_log_discriminant",
        "log_abs_j",
    ],
}

LMFDB_API = "https://www.lmfdb.org/api/ec_curvedata/"

RAW_COLUMNS = [
    "lmfdb_label", "lmfdb_iso", "conductor", "absD", "signD", "jinv",
    "rank", "analytic_rank", "regulator", "faltings_height", "torsion",
    "cm", "semistable", "potential_good_reduction", "abc_quality",
    "szpiro_ratio", "manin_constant", "intrinsic_torsion",
    "class_size", "class_deg", "isogeny_degrees", "bad_primes"
]


@dataclass
class Config:
    max_conductor: int = 500000
    download_limit: int = 20000
    page_size: int = 1000
    sample_size: int = 6000
    k_neighbors: int = 12
    maxdim: int = 3
    n_nulls: int = 100
    n_resamples: int = 30
    alpha: float = 0.01
    seed: int = 20260917
    max_homology_edges: int = 120000
    n_geodesic_pairs: int = 100
    geodesic_k: int = 12
    max_dense_topology_points: int = 1800
    demo_mode: bool = False
    demo_topology_points: int = 350
    demo_nulls: int = 2
    demo_resamples: int = 2
    demo_maxdim: int = 2
    demo_vr_thresh: float = 1.8


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def stable_json(obj):
    return json.dumps(obj, sort_keys=True, default=str)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def ensure_dirs(root: Path):
    (root / "results" / "figures").mkdir(parents=True, exist_ok=True)
    (root / "data").mkdir(parents=True, exist_ok=True)


def log_abs(x):
    x = pd.to_numeric(x, errors="coerce")
    return np.log1p(np.abs(x))


def signed_log(x):
    x = pd.to_numeric(x, errors="coerce")
    return np.sign(x) * np.log1p(np.abs(x))


# ---------------------------------------------------------------------------
# LMFDB acquisition
# ---------------------------------------------------------------------------

def normalize_lmfdb_records(records):
    rows = []
    for r in records:
        row = {}
        for c in RAW_COLUMNS:
            v = r.get(c, np.nan)
            if isinstance(v, (list, dict)):
                v = json.dumps(v, sort_keys=True)
            row[c] = v
        rows.append(row)
    return pd.DataFrame(rows)


def parse_api_payload(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("data", "results", "records"):
            if key in payload and isinstance(payload[key], list):
                return payload[key]
    raise ValueError("Unrecognized LMFDB API response format")


def download_lmfdb(out_csv: Path, cfg: Config):
    all_rows = []
    offset = 0
    fields = ",".join(RAW_COLUMNS)

    print("Querying LMFDB:", LMFDB_API)
    print(f"Conductor range: 1-{cfg.max_conductor}")
    print(f"Maximum downloaded records: {cfg.download_limit}")

    while len(all_rows) < cfg.download_limit:
        params = {
            "_format": "json",
            "_offset": offset,
            "_limit": min(cfg.page_size, cfg.download_limit - len(all_rows)),
            "conductor": f"1-{cfg.max_conductor}",
            "_fields": fields,
        }
        r = requests.get(LMFDB_API, params=params, timeout=90,
                         headers={"User-Agent": "RTCH-E1 research experiment"})
        r.raise_for_status()
        payload = r.json()
        records = parse_api_payload(payload)
        if not records:
            break

        all_rows.extend(records)
        print(f"  received {len(all_rows)} records")

        if len(records) < params["_limit"]:
            break
        offset += len(records)
        time.sleep(0.25)

    df = normalize_lmfdb_records(all_rows)
    df.to_csv(out_csv, index=False)
    print("Saved:", out_csv)
    print("SHA256:", sha256_file(out_csv))
    return df


# ---------------------------------------------------------------------------
# Data preparation
# ---------------------------------------------------------------------------

def load_input(path: Path):
    df = pd.read_csv(path, low_memory=False)
    if len(df) == 0:
        raise ValueError("Input CSV is empty")
    return df


def prepare_features(df):
    """Normalize LMFDB-style inputs while preserving precomputed demo features."""
    out = df.copy()

    # Accept common alternate names from manually downloaded LMFDB tables.
    aliases = {
        "conductor": ["conductor", "N"],
        "absD": ["absD", "abs_disc", "discriminant_abs"],
        "signD": ["signD", "discriminant_sign"],
        "jinv": ["jinv", "j_invariant", "j"],
        "faltings_height": ["faltings_height", "Faltings height", "faltingsHeight"],
        "regulator": ["regulator", "Regulator"],
        "rank": ["rank", "Rank"],
        "analytic_rank": ["analytic_rank", "analytic rank"],
    }

    for target, candidates in aliases.items():
        if target not in out.columns:
            for c in candidates:
                if c in out.columns:
                    out[target] = out[c]
                    break

    def numeric_series(name, default=np.nan):
        if name in out.columns:
            return pd.to_numeric(out[name], errors="coerce")
        return pd.Series(default, index=out.index, dtype=float)

    out["conductor"] = numeric_series("conductor")
    out["absD"] = numeric_series("absD")
    if "signD" in out.columns:
        out["signD"] = pd.to_numeric(out["signD"], errors="coerce").fillna(1.0)
    else:
        out["signD"] = pd.Series(1.0, index=out.index)
    out["rank"] = numeric_series("rank")
    out["analytic_rank"] = numeric_series("analytic_rank")
    out["regulator"] = numeric_series("regulator")
    out["faltings_height"] = numeric_series("faltings_height")

    # j may be a rational string; use floating conversion where possible.
    if "jinv" in out.columns:
        out["j_numeric"] = pd.to_numeric(out["jinv"], errors="coerce")
    else:
        out["j_numeric"] = pd.Series(np.nan, index=out.index, dtype=float)

    # Do not overwrite precomputed coordinates. This is required by the
    # synthetic torus control and is also useful for externally transformed
    # LMFDB tables.
    if "log_conductor" not in out.columns:
        out["log_conductor"] = np.log1p(out["conductor"])
    if "signed_log_discriminant" not in out.columns:
        out["signed_log_discriminant"] = out["signD"] * np.log1p(out["absD"].abs())
    if "log_abs_j" not in out.columns:
        out["log_abs_j"] = np.log1p(out["j_numeric"].abs())
    if "log_regulator" not in out.columns:
        out["log_regulator"] = np.log1p(out["regulator"].clip(lower=0))

    return out


def choose_sample(df, n, seed):
    rng = np.random.default_rng(seed)
    if n is None or n >= len(df):
        return df.copy().reset_index(drop=True)
    idx = rng.choice(len(df), size=n, replace=False)
    return df.iloc[idx].copy().reset_index(drop=True)


def choose_topology_sample(df, max_points, seed):
    """Bound VR computation while preserving the full analysis dataframe.

    The positive-control demo is below this limit.  Real LMFDB analyses can
    contain thousands of curves, so topology is evaluated on a deterministic
    subset and geodesic/scalar analyses can still use the broader sample.
    """
    if max_points is None or len(df) <= max_points:
        return df.copy().reset_index(drop=True)
    return choose_sample(df, max_points, seed)


def make_matrix(df, feature_names):
    X = df[feature_names].replace([np.inf, -np.inf], np.nan).copy()

    # Median imputation is fit only on the supplied analysis sample.
    med = X.median(numeric_only=True)
    X = X.fillna(med)
    X = X.fillna(0.0)

    scaler = RobustScaler(quantile_range=(10, 90))
    Xs = scaler.fit_transform(X.values)

    return Xs, scaler, X


# ---------------------------------------------------------------------------
# Persistent homology
# ---------------------------------------------------------------------------

def knn_sparse_distance(X, k):
    """Build a symmetric weighted kNN graph for geodesic calculations.

    This graph is deliberately kept separate from the Vietoris--Rips
    distance matrix.  Missing graph edges mean "not directly connected",
    rather than distance zero.
    """
    if len(X) < 2:
        return sparse.csr_matrix((len(X), len(X)), dtype=float)

    k = max(1, min(int(k), len(X) - 1))
    nn = NearestNeighbors(n_neighbors=k + 1, metric="euclidean")
    nn.fit(X)
    dist, ind = nn.kneighbors(X)

    rows, cols, vals = [], [], []
    for i in range(len(X)):
        for jpos in range(1, k + 1):
            j = int(ind[i, jpos])
            if j == i:
                continue
            rows.append(i)
            cols.append(j)
            vals.append(float(dist[i, jpos]))

    A = sparse.coo_matrix((vals, (rows, cols)), shape=(len(X), len(X))).tocsr()
    # Undirected union: Euclidean distance is symmetric, so the union of
    # the directed neighbor lists can safely retain the observed edge.
    A = A.maximum(A.T)
    A.eliminate_zeros()
    A.setdiag(0.0)
    A.eliminate_zeros()
    return A.tocsr()


def euclidean_distance_matrix(X):
    """Return the complete pairwise Euclidean distance matrix."""
    return squareform(pdist(X, metric="euclidean"))


def ripser_diagrams(X, maxdim, k_neighbors, max_edges, vr_thresh=np.inf):
    """Compute VR persistent homology from a genuine metric matrix.

    For the synthetic control, and for manageable samples, Ripser receives
    the complete Euclidean distance matrix.  The old implementation passed
    a sparse adjacency matrix with ``distance_matrix=False``; that is not a
    valid way to represent the point-cloud metric and can erase the expected
    H1/H2 torus signal.

    For large real-data samples, a dense matrix may be too expensive.  In
    that case this routine constructs a sparse geodesic distance matrix from
    the kNN graph and passes it explicitly as a distance matrix.  This keeps
    the topology/geodesic concepts distinct while retaining the existing
    memory guard.
    """
    if not HAVE_RIPSER:
        raise RuntimeError(
            "ripser is required for the real experiment. "
            "Install it with: pip install ripser persim"
        )

    n = len(X)
    if n < 4:
        raise ValueError("At least four observations are required for topology")

    # Dense VR is the validated positive-control path.  2000 points require
    # about 32 MB for float64 distances, before Ripser's internal work.
    dense_limit = 1800
    if n <= dense_limit:
        D = euclidean_distance_matrix(X)
        result = ripser(D, distance_matrix=True, maxdim=maxdim,
                        thresh=vr_thresh, do_cocycles=False)
        return result["dgms"], knn_sparse_distance(X, k_neighbors)

    # A complete VR metric is required by this implementation.  Do not silently
    # substitute a sparse adjacency matrix: that was the original topology bug.
    raise RuntimeError(
        f"VR topology received {n} points, exceeding the dense limit of "
        f"{dense_limit}. Subsample before calling ripser_diagrams."
    )

def persistence_summary(dgms):
    records = []
    for dim, dgm in enumerate(dgms):
        if dgm is None or len(dgm) == 0:
            continue
        finite = dgm[np.isfinite(dgm[:, 1])]
        if len(finite) == 0:
            continue
        pers = finite[:, 1] - finite[:, 0]
        for i, (birth, death) in enumerate(finite):
            records.append({
                "dimension": dim,
                "feature": i,
                "birth": float(birth),
                "death": float(death),
                "persistence": float(death - birth),
            })
    return pd.DataFrame(records)


def betti_at_scale(dgms, eps):
    out = {}
    for dim, dgm in enumerate(dgms):
        if dgm is None:
            out[dim] = 0
            continue
        alive = (dgm[:, 0] <= eps) & (eps < dgm[:, 1])
        out[dim] = int(np.sum(alive))
    return out


def choose_scale_from_H0(dgms):
    if not dgms or len(dgms[0]) == 0:
        return None
    h0 = dgms[0]
    finite = h0[np.isfinite(h0[:, 1])]
    if len(finite) == 0:
        return None
    deaths = np.sort(finite[:, 1])
    # A conservative connectivity-scale heuristic.
    return float(np.quantile(deaths, 0.90))


# ---------------------------------------------------------------------------
# Null models
# ---------------------------------------------------------------------------

def null_independent_columns(X, rng):
    Y = np.empty_like(X)
    for j in range(X.shape[1]):
        Y[:, j] = X[rng.permutation(X.shape[0]), j]
    return Y


def null_row_permutation(X, rng):
    return X[rng.permutation(X.shape[0])]


def persistence_maxima(dgms, maxdim=3):
    vals = {}
    for d in range(maxdim + 1):
        if d >= len(dgms) or dgms[d] is None or len(dgms[d]) == 0:
            vals[d] = 0.0
            continue
        finite = dgms[d][np.isfinite(dgms[d][:, 1])]
        if len(finite) == 0:
            vals[d] = 0.0
        else:
            vals[d] = float(np.max(finite[:, 1] - finite[:, 0]))
    return vals


def null_test(X, observed, cfg, rng):
    rows = []
    for b in range(cfg.n_nulls):
        Xn = null_independent_columns(X, rng)
        try:
            dgms, _ = ripser_diagrams(
                Xn, cfg.maxdim, cfg.k_neighbors, cfg.max_homology_edges,
                cfg.demo_vr_thresh if cfg.demo_mode else np.inf
            )
            mx = persistence_maxima(dgms, cfg.maxdim)
            row = {"null_id": b}
            row.update({f"H{d}_max_persistence": mx.get(d, 0.0)
                        for d in range(cfg.maxdim + 1)})
            rows.append(row)
        except Exception as e:
            print("Null", b, "failed:", e)

    null_df = pd.DataFrame(rows)
    if len(null_df):
        for d in range(cfg.maxdim + 1):
            obs = observed.get(d, 0.0)
            vals = null_df[f"H{d}_max_persistence"].values
            empirical_p = (1 + np.sum(vals >= obs)) / (1 + len(vals))
            null_df[f"H{d}_obs_exceed"] = obs
            null_df[f"H{d}_empirical_p"] = empirical_p
    return null_df


# ---------------------------------------------------------------------------
# Geodesics
# ---------------------------------------------------------------------------

def graph_geodesic_analysis(X, A, df, cfg, out_csv):
    """Estimate manifold geodesics with shortest paths on the kNN graph.

    Pair selection excludes direct graph neighbors.  This is important: a
    direct kNN edge has exactly the ambient chord length and therefore cannot
    test whether the graph recovers a longer manifold geodesic.
    """
    rng = np.random.default_rng(cfg.seed + 991)
    D = dijkstra(A, directed=False, return_predecessors=False)

    pairs = []
    n = len(X)
    max_attempts = max(100, cfg.n_geodesic_pairs * 50)

    for _ in range(max_attempts):
        if len(pairs) >= cfg.n_geodesic_pairs:
            break
        i, j = rng.choice(n, 2, replace=False)
        if not np.isfinite(D[i, j]):
            continue

        chord = float(np.linalg.norm(X[i] - X[j]))
        if chord <= 1e-12:
            continue

        # Exclude direct graph edges so that graph_geodesic is a genuine
        # multi-edge path rather than simply the Euclidean chord.
        if A[i, j] != 0:
            continue

        geo = float(D[i, j])
        if geo <= chord * (1.0 + 1e-9):
            continue

        pairs.append({
            "source": int(i),
            "target": int(j),
            "graph_geodesic": geo,
            "euclidean_chord": chord,
            "tortuosity": geo / chord,
            "source_label": str(df.iloc[i].get("lmfdb_label", i)),
            "target_label": str(df.iloc[j].get("lmfdb_label", j)),
        })

    g = pd.DataFrame(pairs)
    g.to_csv(out_csv, index=False)
    return g, D


# ---------------------------------------------------------------------------
# Scalar embeddings
# ---------------------------------------------------------------------------

def scalar_embeddings(X, A, df):
    n = len(X)

    pca = PCA(n_components=min(3, X.shape[1]))
    pc = pca.fit_transform(X)

    # Graph eccentricity is a coordinate-free scalar relative to the
    # empirical graph metric.
    D = dijkstra(A, directed=False, return_predecessors=False)
    finite_D = np.where(np.isfinite(D), D, np.nan)
    eccentricity = np.nanmax(finite_D, axis=1)

    # A simple diffusion coordinate from the normalized graph adjacency.
    deg = np.asarray(A.sum(axis=1)).ravel()
    deg[deg == 0] = 1
    P = sparse.diags(1.0 / deg) @ A
    vals, vecs = sparse.linalg.eigs(P.astype(float), k=min(3, n-1),
                                    which="LR")
    order = np.argsort(-vals.real)
    diffusion = vecs[:, order].real
    if diffusion.shape[1] > 1:
        diffusion1 = diffusion[:, 1]
    else:
        diffusion1 = diffusion[:, 0]

    out = pd.DataFrame({
        "pc1": pc[:, 0],
        "pc2": pc[:, 1] if pc.shape[1] > 1 else 0,
        "pc3": pc[:, 2] if pc.shape[1] > 2 else 0,
        "graph_eccentricity": eccentricity,
        "diffusion1": diffusion1,
    })

    if "rank" in df.columns:
        out["rank"] = df["rank"].values

    for col in ["conductor", "absD", "regulator", "faltings_height",
                "abc_quality", "szpiro_ratio"]:
        if col in df.columns:
            out[col] = pd.to_numeric(df[col], errors="coerce").values

    return out


# ---------------------------------------------------------------------------
# Scalar predictive validation
# ---------------------------------------------------------------------------

def evaluate_scalar_predictions(embed_df, target_cols, seed):
    rows = []
    scalar_cols = [
        c for c in embed_df.columns
        if c in ["pc1", "pc2", "pc3", "graph_eccentricity", "diffusion1"]
    ]

    rng = np.random.default_rng(seed)

    for target in target_cols:
        if target not in embed_df.columns:
            continue
        y = pd.to_numeric(embed_df[target], errors="coerce").values
        ok = np.isfinite(y)
        if ok.sum() < 100:
            continue

        for scalar in scalar_cols:
            x = pd.to_numeric(embed_df[scalar], errors="coerce").values
            ok2 = ok & np.isfinite(x)
            if ok2.sum() < 100:
                continue

            xs = x[ok2].reshape(-1, 1)
            ys = y[ok2]

            kf = KFold(n_splits=5, shuffle=True, random_state=seed)
            preds = np.zeros(len(ys))

            for train, test in kf.split(xs):
                model = make_pipeline(RobustScaler(), Ridge(alpha=1.0))
                model.fit(xs[train], ys[train])
                preds[test] = model.predict(xs[test])

            rows.append({
                "target": target,
                "scalar": scalar,
                "n": int(len(ys)),
                "cv_r2": float(r2_score(ys, preds)),
                "cv_mae": float(mean_absolute_error(ys, preds)),
                "spearman_rho": float(spearmanr(xs[:, 0], ys).statistic),
                "spearman_p": float(spearmanr(xs[:, 0], ys).pvalue),
            })

    return pd.DataFrame(rows)


def rank_label_null(embed_df, scalar, seed, n_nulls=100):
    if "rank" not in embed_df.columns:
        return pd.DataFrame()

    x = pd.to_numeric(embed_df[scalar], errors="coerce").values
    y = pd.to_numeric(embed_df["rank"], errors="coerce").values
    ok = np.isfinite(x) & np.isfinite(y)

    x = x[ok]
    y = y[ok]
    if len(y) < 100:
        return pd.DataFrame()

    rng = np.random.default_rng(seed)
    vals = []
    observed = abs(spearmanr(x, y).statistic)

    for b in range(n_nulls):
        yp = rng.permutation(y)
        vals.append(abs(spearmanr(x, yp).statistic))

    vals = np.asarray(vals)
    p = (1 + np.sum(vals >= observed)) / (1 + len(vals))
    return pd.DataFrame([{
        "scalar": scalar,
        "rank_observed_abs_spearman": observed,
        "rank_null_mean_abs_spearman": float(vals.mean()),
        "rank_null_95pct": float(np.quantile(vals, 0.95)),
        "rank_label_permutation_p": float(p),
    }])


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------

def save_persistence_figures(dgms, root, title_prefix="Observed"):
    figdir = root / "results" / "figures"
    for dim in range(min(3, len(dgms))):
        dgm = dgms[dim]
        if dgm is None or len(dgm) == 0:
            continue
        finite = dgm[np.isfinite(dgm[:, 1])]
        if len(finite) == 0:
            continue

        plt.figure(figsize=(7, 6))
        plt.scatter(finite[:, 0], finite[:, 1], s=12)
        lim = float(np.max(finite[:, 1]))
        if lim <= 0:
            lim = 1
        plt.plot([0, lim], [0, lim], linewidth=1)
        plt.xlabel("Birth")
        plt.ylabel("Death")
        plt.title(f"{title_prefix} persistence diagram H{dim}")
        plt.tight_layout()
        plt.savefig(figdir / f"persistence_H{dim}.png", dpi=180)
        plt.close()


def save_scalar_fig(embed_df, root):
    if not {"pc1", "pc2"}.issubset(embed_df.columns):
        return
    plt.figure(figsize=(8, 6))
    if "rank" in embed_df.columns:
        c = pd.to_numeric(embed_df["rank"], errors="coerce").fillna(0)
        sc = plt.scatter(embed_df["pc1"], embed_df["pc2"], c=c, s=8)
        plt.colorbar(sc, label="Rank")
    else:
        plt.scatter(embed_df["pc1"], embed_df["pc2"], s=8)
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("RTCH-E1 scalar embedding")
    plt.tight_layout()
    plt.savefig(root / "results" / "figures" / "scalar_embedding.png", dpi=180)
    plt.close()


def save_geodesic_fig(geo_df, root):
    if geo_df is None or len(geo_df) == 0:
        return
    plt.figure(figsize=(7, 5))
    plt.hist(geo_df["tortuosity"], bins=30)
    plt.xlabel("Geodesic / chord")
    plt.ylabel("Count")
    plt.title("Empirical arithmetic geodesic tortuosity")
    plt.tight_layout()
    plt.savefig(root / "results" / "figures" / "geodesic_projection.png", dpi=180)
    plt.close()


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

def run_analysis(input_csv: Path, root: Path, cfg: Config):
    ensure_dirs(root)

    # Demo mode is a positive-control benchmark, not a stress test.  Ripser's
    # VR complex can grow combinatorially, especially in H3.  Hard caps here
    # protect the user's machine even when aggressive CLI values are supplied.
    if cfg.demo_mode:
        cfg = replace(
            cfg,
            sample_size=min(cfg.sample_size, cfg.demo_topology_points),
            max_dense_topology_points=min(cfg.max_dense_topology_points, cfg.demo_topology_points),
            maxdim=min(cfg.maxdim, cfg.demo_maxdim),
            n_nulls=min(cfg.n_nulls, cfg.demo_nulls),
            n_resamples=min(cfg.n_resamples, cfg.demo_resamples),
            n_geodesic_pairs=min(cfg.n_geodesic_pairs, 50),
        )
        print("Demo safety caps:", {
            "points": cfg.sample_size,
            "maxdim": cfg.maxdim,
            "nulls": cfg.n_nulls,
            "resamples": cfg.n_resamples,
            "geodesic_pairs": cfg.n_geodesic_pairs,
            "vr_thresh": cfg.demo_vr_thresh,
        })

    print("\n=== RTCH-E1 ===")
    print("Input:", input_csv)
    print("SHA256:", sha256_file(input_csv))

    raw = load_input(input_csv)
    df = prepare_features(raw)
    df = choose_sample(df, cfg.sample_size, cfg.seed)

    manifest = {
        "experiment": "RTCH-E1",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "input": str(input_csv),
        "input_sha256": sha256_file(input_csv),
        "config": asdict(cfg),
        "n_raw": int(len(raw)),
        "n_analysis": int(len(df)),
        "feature_sets": FEATURE_SETS,
        "primary_topology_metric": "intrinsic",
        "rank_excluded_from_primary_metric": True,
        "topology_method": "complete Euclidean Vietoris-Rips metric on a bounded deterministic subset; graph shortest paths are reserved for geodesics",
        "software": {
            "python": sys.version,
            "ripser_available": HAVE_RIPSER,
        },
    }

    (root / "results" / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2, default=str)
    )

    all_topology = []
    all_nulls = []
    all_stability = []

    feature_items = FEATURE_SETS.items()
    if cfg.demo_mode:
        feature_items = [("intrinsic", FEATURE_SETS["intrinsic"])]

    for set_name, features in feature_items:
        available = [f for f in features if f in df.columns]
        if len(available) < 2:
            print("Skipping feature set", set_name, "not enough features")
            continue

        print(f"\n--- Feature set: {set_name} ---")
        print("Features:", available)

        topo_df = choose_topology_sample(
            df, cfg.max_dense_topology_points,
            cfg.seed + {"intrinsic": 1001, "no_regulator": 1002, "minimal": 1003}.get(set_name, 1004)
        )
        X, scaler, Xclean = make_matrix(topo_df, available)

        try:
            dgms, A = ripser_diagrams(
                X, cfg.maxdim, cfg.k_neighbors, cfg.max_homology_edges,
                cfg.demo_vr_thresh if cfg.demo_mode else np.inf
            )
        except Exception as e:
            print("Topology failed:", e)
            continue

        summary = persistence_summary(dgms)
        if len(summary):
            summary["feature_set"] = set_name
            all_topology.append(summary)

        observed = persistence_maxima(dgms, cfg.maxdim)
        null_df = null_test(X, observed, cfg, np.random.default_rng(
            cfg.seed + {"intrinsic": 101, "no_regulator": 202, "minimal": 303}.get(set_name, 404)
        ))
        if len(null_df):
            null_df["feature_set"] = set_name
            all_nulls.append(null_df)

        # Stability by repeated subsampling.
        stab = []
        for b in range(cfg.n_resamples):
            seed_b = cfg.seed + 10000 + b
            sub = choose_topology_sample(df, cfg.max_dense_topology_points, seed_b)
            Xb, _, _ = make_matrix(sub, available)
            try:
                db, _ = ripser_diagrams(
                    Xb, cfg.maxdim, cfg.k_neighbors, cfg.max_homology_edges,
                    cfg.demo_vr_thresh if cfg.demo_mode else np.inf
                )
                mx = persistence_maxima(db, cfg.maxdim)
                stab.append({
                    "resample": b,
                    "feature_set": set_name,
                    **{f"H{d}_max_persistence": mx.get(d, 0.0)
                       for d in range(cfg.maxdim + 1)}
                })
            except Exception as e:
                print("Stability", b, "failed:", e)

        if stab:
            all_stability.append(pd.DataFrame(stab))

        if set_name == "intrinsic":
            save_persistence_figures(dgms, root)

            geo_df, D = graph_geodesic_analysis(
                X, A, topo_df, cfg, root / "results" / "geodesics.csv"
            )
            save_geodesic_fig(geo_df, root)

            embed = scalar_embeddings(X, A, topo_df)
            embed.to_csv(root / "results" / "scalar_embeddings.csv", index=False)
            save_scalar_fig(embed, root)

            targets = [
                c for c in [
                    "rank", "analytic_rank", "conductor", "absD",
                    "regulator", "faltings_height", "abc_quality",
                    "szpiro_ratio"
                ] if c in embed.columns
            ]
            pred = evaluate_scalar_predictions(embed, targets, cfg.seed)
            pred.to_csv(root / "results" / "prediction_tests.csv", index=False)

            rank_nulls = []
            for scalar in ["pc1", "pc2", "pc3",
                           "graph_eccentricity", "diffusion1"]:
                if scalar in embed.columns:
                    rn = rank_label_null(
                        embed, scalar, cfg.seed + 500, cfg.n_nulls
                    )
                    if len(rn):
                        rank_nulls.append(rn)
            if rank_nulls:
                pd.concat(rank_nulls, ignore_index=True).to_csv(
                    root / "results" / "rank_label_nulls.csv", index=False
                )

    if all_topology:
        topo = pd.concat(all_topology, ignore_index=True)
    else:
        topo = pd.DataFrame()
    topo.to_csv(root / "results" / "topology_summary.csv", index=False)

    if all_nulls:
        nulls = pd.concat(all_nulls, ignore_index=True)
    else:
        nulls = pd.DataFrame()
    nulls.to_csv(root / "results" / "null_persistence.csv", index=False)

    if all_stability:
        stab = pd.concat(all_stability, ignore_index=True)
    else:
        stab = pd.DataFrame()
    stab.to_csv(root / "results" / "stability_summary.csv", index=False)

    # Compact machine-readable result.
    result = {
        "n_analysis": int(len(df)),
        "topology": {},
        "nulls": {},
        "stability": {},
    }

    if len(topo):
        for fs in topo["feature_set"].unique():
            sub = topo[topo.feature_set == fs]
            result["topology"][fs] = {}
            for dim in sorted(sub.dimension.unique()):
                result["topology"][fs][f"H{int(dim)}"] = {
                    "max_persistence": float(sub[sub.dimension == dim]
                                             ["persistence"].max()),
                    "n_features": int(np.sum(sub.dimension == dim)),
                }

    if len(nulls):
        for fs in nulls["feature_set"].unique():
            sub = nulls[nulls.feature_set == fs]
            result["nulls"][fs] = {}
            for dim in range(cfg.maxdim + 1):
                pcol = f"H{dim}_empirical_p"
                if pcol in sub.columns:
                    result["nulls"][fs][f"H{dim}"] = float(
                        sub[pcol].iloc[0]
                    )

    (root / "results" / "result.json").write_text(
        json.dumps(result, indent=2)
    )

    print("\n=== RTCH-E1 COMPLETE ===")
    print("Results:", root / "results")
    print("\nInterpretation:")
    print("  H^k evidence = persistent H_k features in the sampled metric space.")
    print("  Treat H1/H2/H3 as candidates until null/stability tests pass.")
    print("  A surviving feature is not automatically a physical invariant.")
    print("  Review topology_summary.csv, null_persistence.csv,")
    print("  stability_summary.csv, prediction_tests.csv and rank_label_nulls.csv.")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def make_demo(path):
    rng = np.random.default_rng(12345)
    n = 350

    # A torus-like synthetic benchmark plus a cloud. This checks that the
    # pipeline can recover known topology before touching arithmetic data.
    u = rng.uniform(0, 2*np.pi, n)
    v = rng.uniform(0, 2*np.pi, n)
    R, r = 2.0, 0.65

    x = (R + r*np.cos(v))*np.cos(u)
    y = (R + r*np.cos(v))*np.sin(u)
    z = r*np.sin(v)

    # Add small measurement noise while retaining a clean embedded torus.
    w1 = rng.normal(0, 0.012, n)
    w2 = rng.normal(0, 0.012, n)

    df = pd.DataFrame({
        "log_conductor": x + w1,
        "signed_log_discriminant": y + w2,
        "log_abs_j": z + rng.normal(0, 0.012, n),
        "faltings_height": np.sin(u) + rng.normal(0, 0.012, n),
        "log_regulator": np.cos(v) + rng.normal(0, 0.012, n),
        "rank": np.floor(np.abs(z)*2).astype(int),
    })
    df.to_csv(path, index=False)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["demo", "download", "analyze"],
                    required=True)
    ap.add_argument("--root", default="RTCH_E1")
    ap.add_argument("--input", default=None)
    ap.add_argument("--max-conductor", type=int, default=500000)
    ap.add_argument("--download-limit", type=int, default=20000)
    ap.add_argument("--page-size", type=int, default=1000)
    ap.add_argument("--n-sample", type=int, default=6000)
    ap.add_argument("--k-neighbors", type=int, default=12)
    ap.add_argument("--maxdim", type=int, choices=[1, 2, 3], default=3)
    ap.add_argument("--n-nulls", type=int, default=100)
    ap.add_argument("--n-resamples", type=int, default=30)
    ap.add_argument("--n-geodesic-pairs", type=int, default=100)
    ap.add_argument("--max-homology-edges", type=int, default=120000)
    ap.add_argument("--max-dense-topology-points", type=int, default=1800)
    ap.add_argument("--seed", type=int, default=20260917)
    args = ap.parse_args()

    root = Path(args.root)
    ensure_dirs(root)

    cfg = Config(
        max_conductor=args.max_conductor,
        download_limit=args.download_limit,
        page_size=args.page_size,
        sample_size=args.n_sample,
        k_neighbors=args.k_neighbors,
        maxdim=args.maxdim,
        n_nulls=args.n_nulls,
        n_resamples=args.n_resamples,
        n_geodesic_pairs=args.n_geodesic_pairs,
        max_homology_edges=args.max_homology_edges,
        max_dense_topology_points=args.max_dense_topology_points,
        seed=args.seed,
        demo_mode=(args.mode == "demo"),
    )

    if args.mode == "demo":
        p = root / "data" / "demo_torus.csv"
        make_demo(p)
        print("Demo data written to", p)
        run_analysis(p, root, cfg)
        return

    if args.mode == "download":
        p = Path(args.input) if args.input else root / "data" / "lmfdb_curves.csv"
        download_lmfdb(p, cfg)
        print("\nNext:")
        print(f"  python rtch_e1.py --mode analyze --input {p}")
        return

    if args.mode == "analyze":
        if not args.input:
            raise SystemExit("--input is required for --mode analyze")
        run_analysis(Path(args.input), root, cfg)
        return


if __name__ == "__main__":
    main()
