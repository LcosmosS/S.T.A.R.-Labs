"""Tests for the preregistered EXP-MAP-A01 protocol and ecdata hygiene."""

import csv
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.experiments import exp_map_a01
from src.control.execution import PreflightError, preflight_controlled_experiment
from src.control.registry import RegistrySnapshot
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
SPEC = ROOT / "controlled_execution" / "specs" / "EXP-MAP-A01.json"


def _config():
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def test_preregistered_config_matches_locked_implementation():
    _require_locked_config(_config())


def test_committed_execution_spec_binds_current_preregistration_records():
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    resolved = RegistrySnapshot.load(ROOT).resolve("EXP-MAP-A01")
    assert spec["registry_bindings"] == resolved.record_hashes


def test_activation_is_execution_only_with_all_support_flags_false():
    resolved = RegistrySnapshot.load(ROOT).resolve("EXP-MAP-A01")
    assert resolved.experiment["Status"] == "preregistered"
    assert resolved.experiment["Controlled_Execution_Eligible"] == "true"
    assert resolved.dataset["Controlled_Execution_Eligible"] == "true"
    for row in (resolved.experiment, resolved.dataset):
        assert row["Controlled_Support_Eligible"] == "false"
        assert row["Physical_Support_Eligible"] == "false"
    assert json.loads(SPEC.read_text(encoding="utf-8"))["registry_bindings"] == resolved.record_hashes
    # Real preflight belongs to the source-hydrated activation CI, not a unit
    # fixture. No hypothesis test is executed here.


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


def _small_output_fixture(monkeypatch):
    """Exercise output publication only, without running the registered cohort."""
    config = _config()
    config["null"]["realizations"] = 3

    def require_fixture_config(value):
        # The short fixture is the only allowed test deviation. Production's
        # locked-config validator is untouched and every other field is checked.
        locked = json.loads(json.dumps(value))
        locked["null"]["realizations"] = 999
        _require_locked_config(locked)
        assert value["null"]["realizations"] == 3

    frame = pd.DataFrame(
        {
            "label": [f"{101 + index}a1" for index in range(12)],
            "isogeny_class": [f"{101 + index}a" for index in range(12)],
            "conductor": list(range(101, 113)),
            "delta": [-value for value in range(37, 49)],
            "rank": [index % 3 for index in range(12)],
            "torsion_order": [1] * 12,
        }
    )
    monkeypatch.setattr(exp_map_a01, "_require_locked_config", require_fixture_config)
    monkeypatch.setattr(exp_map_a01, "load_locked_dataset", lambda *_: frame)
    return config


def _reject_input_loading(*_):
    raise AssertionError("existing outputs must be rejected before input loading")


def test_rerun_preserves_existing_summary_and_csv_bytes(tmp_path, monkeypatch):
    output_dir = tmp_path / "previous-run"
    output_dir.mkdir()
    old_results = {
        "summary.json": b'{"old_run": true}\n',
        "observed_projection.csv": b"label,longitude\nold-label,99\n",
        "null_statistics.csv": b"realization,statistic\n1,-123\n",
    }
    for name, content in old_results.items():
        (output_dir / name).write_bytes(content)
    monkeypatch.setattr(exp_map_a01, "load_locked_dataset", _reject_input_loading)

    with pytest.raises(ProtocolViolation, match="refusing to overwrite existing result"):
        exp_map_a01.run_protocol(tmp_path / "unused-input", output_dir, _config())

    assert {path.name: path.read_bytes() for path in output_dir.iterdir()} == old_results


@pytest.mark.parametrize(
    "existing_name", ["summary.json", "observed_projection.csv", "null_statistics.csv"]
)
def test_any_existing_result_rejects_before_other_output_is_created(
    tmp_path, monkeypatch, existing_name
):
    output_dir = tmp_path / "previous-run"
    output_dir.mkdir()
    old_bytes = b"previous result must survive byte-for-byte\n"
    (output_dir / existing_name).write_bytes(old_bytes)
    monkeypatch.setattr(exp_map_a01, "load_locked_dataset", _reject_input_loading)

    with pytest.raises(ProtocolViolation, match="refusing to overwrite existing result"):
        exp_map_a01.run_protocol(tmp_path / "unused-input", output_dir, _config())

    assert {path.name: path.read_bytes() for path in output_dir.iterdir()} == {
        existing_name: old_bytes
    }


def test_late_output_collision_preserves_raced_file_and_empty_reservations(
    tmp_path, monkeypatch
):
    config = _small_output_fixture(monkeypatch)
    output_dir = tmp_path / "raced-run"
    original_open = Path.open
    raced_bytes = b'{"another_run": true}\n'

    def racing_open(path, mode="r", *args, **kwargs):
        if path == output_dir / "summary.json" and mode == "x":
            with original_open(path, "wb") as stream:
                stream.write(raced_bytes)
        return original_open(path, mode, *args, **kwargs)

    def reject_csv_write(*_, **__):
        raise AssertionError("no output may be written until every target is reserved")

    monkeypatch.setattr(Path, "open", racing_open)
    monkeypatch.setattr(pd.DataFrame, "to_csv", reject_csv_write)
    with pytest.raises(ProtocolViolation, match="reservation failed.*fresh output directory"):
        exp_map_a01.run_protocol(tmp_path / "unused-input", output_dir, config)

    assert {path.name: path.read_bytes() for path in output_dir.iterdir()} == {
        "summary.json": raced_bytes,
        "observed_projection.csv": b"",
        "null_statistics.csv": b"",
    }


def test_failed_reservation_never_deletes_a_competitor_replacement(
    tmp_path, monkeypatch
):
    config = _small_output_fixture(monkeypatch)
    output_dir = tmp_path / "replaced-run"
    original_open = Path.open
    opened = {}
    competitor_bytes = b"competitor result must not be deleted\n"
    raced_summary = b'{"another_run": true}\n'

    def replacing_open(path, mode="r", *args, **kwargs):
        if path == output_dir / "summary.json" and mode == "x":
            # Closing the captured handle permits this replacement on Windows
            # too, modeling a writer whose pathname changes during reservation.
            opened["observed_projection.csv"].close()
            replacement = output_dir / "competitor.tmp"
            with original_open(replacement, "wb") as stream:
                stream.write(competitor_bytes)
            replacement.replace(output_dir / "observed_projection.csv")
            with original_open(path, "wb") as stream:
                stream.write(raced_summary)
        stream = original_open(path, mode, *args, **kwargs)
        if mode == "x":
            opened[path.name] = stream
        return stream

    def reject_csv_write(*_, **__):
        raise AssertionError("failed reservations must not serialize result data")

    monkeypatch.setattr(Path, "open", replacing_open)
    monkeypatch.setattr(pd.DataFrame, "to_csv", reject_csv_write)
    with pytest.raises(ProtocolViolation, match="reservation failed.*fresh output directory"):
        exp_map_a01.run_protocol(tmp_path / "unused-input", output_dir, config)

    assert all(stream.closed for stream in opened.values())
    assert {path.name: path.read_bytes() for path in output_dir.iterdir()} == {
        "summary.json": raced_summary,
        "observed_projection.csv": competitor_bytes,
        "null_statistics.csv": b"",
    }


@pytest.mark.parametrize("runner_owned_files", [False, True])
def test_fresh_results_write_without_changing_controlled_runner_files(
    tmp_path, monkeypatch, runner_owned_files
):
    config = _small_output_fixture(monkeypatch)
    output_dir = tmp_path / "fresh-run"
    existing = {}
    if runner_owned_files:
        output_dir.mkdir()
        existing = {
            "execution_config.json": b'{"locked_runner_config": true}\n',
            "stdout.log": b"runner stdout\n",
            "stderr.log": b"runner stderr\n",
        }
        for name, content in existing.items():
            (output_dir / name).write_bytes(content)

    summary = exp_map_a01.run_protocol(tmp_path / "unused-input", output_dir, config)

    assert set(path.name for path in output_dir.iterdir()) == set(existing) | {
        "summary.json", "observed_projection.csv", "null_statistics.csv"
    }
    for name, content in existing.items():
        assert (output_dir / name).read_bytes() == content
    assert json.loads((output_dir / "summary.json").read_text(encoding="utf-8")) == summary
    projection = pd.read_csv(output_dir / "observed_projection.csv")
    assert len(projection) == 12
    assert projection.loc[1, "elevation"] == 200
    nulls = pd.read_csv(output_dir / "null_statistics.csv")
    assert nulls["realization"].tolist() == [1, 2, 3]
    assert len(nulls) == summary["null_realizations"] == 3
    for name in ("summary.json", "observed_projection.csv", "null_statistics.csv"):
        content = (output_dir / name).read_bytes()
        assert content.endswith(b"\n")
        if name.endswith(".csv"):
            assert b"\r" not in content
        else:
            assert content.endswith(os.linesep.encode("ascii"))
