"""Tests for the preregistered EXP-MAP-A01 protocol and ecdata hygiene."""

import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.data.cremona_ecdata import (
    CremonaDataError,
    parse_allcurves_line,
    representative_records,
)
from src.experiments.exp_map_a01 import (
    ProtocolViolation,
    SplitMix64,
    _coherence_statistic,
    _discriminant,
    _neighbor_edges,
    _require_locked_config,
    project_locked,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "preregistrations" / "EXP-MAP-A01" / "config.json"
CI_SUBSET = ROOT / "data" / "raw" / "ci_subset.csv"


def _config():
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def test_preregistered_config_matches_locked_implementation():
    _require_locked_config(_config())


def test_allcurves_parser_uses_actual_upstream_schema():
    record = parse_allcurves_line("37 a 1 [0,0,1,-1,0] 1 1\n")
    assert record.label == "37a1"
    assert record.isogeny_class == "37a"
    assert record.conductor == 37
    assert record.number == 1
    assert record.rank == 1
    assert record.a_invariants == (0, 0, 1, -1, 0)


def test_allcurves_parser_rejects_alllabels_mapping_record():
    with pytest.raises(CremonaDataError, match="malformed"):
        parse_allcurves_line("110001 a 2 110001 a 1\n")


def test_representative_selection_removes_isogeny_duplicates():
    records = [
        parse_allcurves_line("11 a 1 [0,-1,1,-10,-20] 0 5"),
        parse_allcurves_line("11 a 2 [0,-1,1,-7820,-263580] 0 1"),
        parse_allcurves_line("37 a 1 [0,0,1,-1,0] 1 1"),
    ]
    reps = representative_records(records)
    assert [record.label for record in reps] == ["11a1", "37a1"]


def test_known_weierstrass_discriminants_are_exact():
    assert _discriminant((0, 0, 1, -1, 0)) == 37
    assert _discriminant((0, -1, 1, 0, 0)) == -11
    assert _discriminant((0, -1, 1, -10, -20)) == -161051


def test_splitmix64_fisher_yates_sequence_is_locked():
    rng = SplitMix64(1729)
    assert rng.permutation(8).tolist() == [6, 1, 3, 2, 5, 0, 7, 4]
    assert rng.permutation(8).tolist() == [2, 0, 6, 5, 3, 1, 4, 7]


def test_projection_uses_locked_historical_constants_without_clipping():
    frame = pd.DataFrame(
        {
            "label": ["11a1", "37a1"],
            "isogeny_class": ["11a", "37a"],
            "conductor": [11, 37],
            "delta": [-11, 37],
            "rank": [0, 1],
            "torsion_order": [5, 1],
        }
    )
    projected = project_locked(frame, _config())
    assert projected.loc[0, "elevation"] == 0.0
    assert projected.loc[1, "elevation"] == 200.0
    assert np.isfinite(projected[["longitude", "latitude", "elevation"]]).all().all()


def test_neighbor_graph_does_not_use_elevation():
    projection = pd.DataFrame(
        {
            "label": ["a", "b", "c", "d"],
            "longitude": [0.0, 1.0, 2.0, 3.0],
            "latitude": [0.0, 0.0, 0.0, 0.0],
            "elevation": [0.0, 10000.0, -10000.0, 5.0],
        }
    )
    first = _neighbor_edges(projection, 1)
    projection["elevation"] = [99999.0, -2.0, 7.0, 12345.0]
    second = _neighbor_edges(projection, 1)
    assert np.array_equal(first, second)


def test_coherence_statistic_is_higher_for_more_local_rank_coherence():
    edges = np.asarray([[0, 1], [1, 2]], dtype=np.int64)
    coherent = np.asarray([0.0, 0.0, 200.0])
    incoherent = np.asarray([0.0, 400.0, 0.0])
    assert _coherence_statistic(coherent, edges) > _coherence_statistic(
        incoherent, edges
    )


def test_locked_config_rejects_post_preregistration_parameter_change():
    config = _config()
    config["endpoint"]["k"] = 11
    with pytest.raises(ProtocolViolation, match="does not exactly match"):
        _require_locked_config(config)


def test_ci_subset_is_real_one_column_cremona_label_csv():
    with CI_SUBSET.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        assert reader.fieldnames == ["label"]
        labels = [row["label"] for row in reader]

    assert len(labels) == 800
    assert len(labels) == len(set(labels))
    assert labels[:8] == [
        "11a1",
        "14a1",
        "15a1",
        "17a1",
        "19a1",
        "20a1",
        "21a1",
        "24a1",
    ]
    assert all(" " not in label and label[-1].isdigit() for label in labels)
