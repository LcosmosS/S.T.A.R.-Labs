"""Regression tests for A03 validation and execution boundaries."""

import json
from pathlib import Path
import subprocess
import sys

import pytest

from src.control.registry import RegistrySnapshot
from src.experiments import exp_map_a03 as protocol

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "preregistrations" / "EXP-MAP-A03" / "config.json"


def _config():
    return json.loads(CONFIG.read_text(encoding="utf-8"))


@pytest.mark.parametrize("optimized", [False, True])
@pytest.mark.parametrize("mutation", ["config", "hydration"])
def test_validator_rejects_invalid_inputs_under_optimization(
    tmp_path, optimized, mutation
):
    config = _config()
    if mutation == "config":
        config["claim_ids"] = []
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    code = (
        "from pathlib import Path\n"
        "from scripts import validate_exp_map_a03_preregistration as validator\n"
        f"validator.CONFIG = Path({str(config_path)!r})\n"
        f"validator.SOURCE = Path({str(tmp_path / 'missing-source')!r})\n"
        "validator.validate()\n"
    )
    result = subprocess.run(
        [sys.executable, *(["-O"] if optimized else []), "-c", code],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "AssertionError" in result.stderr
    if mutation == "hydration":
        assert "pinned ecdata submodule is not hydrated" in result.stderr
    else:
        assert "pinned ecdata submodule is not hydrated" not in result.stderr


@pytest.mark.parametrize(
    "error",
    [OSError("write failed"), ValueError("serialization failed"), KeyboardInterrupt()],
)
def test_failed_writes_close_streams_and_remove_all_reservations(tmp_path, error):
    unrelated = tmp_path / "keep.txt"
    unrelated.write_text("keep", encoding="utf-8")
    with pytest.raises(type(error)) as caught:
        with protocol._exclusive_output_streams(tmp_path) as streams:
            for stream in streams.values():
                stream.write("partial output")
            raise error
    assert caught.value is error
    assert all(stream.closed for stream in streams.values())
    assert list(tmp_path.iterdir()) == [unrelated]
    assert unrelated.read_text(encoding="utf-8") == "keep"


def test_failed_reservation_preserves_existing_output(tmp_path):
    existing = tmp_path / protocol.OUTPUT_FILENAMES[1]
    existing.write_text("previous run", encoding="utf-8")
    with pytest.raises(protocol.MCJProtocolError, match="output reservation failed"):
        with protocol._exclusive_output_streams(tmp_path):
            pytest.fail("reservation should fail before yielding")
    assert list(tmp_path.iterdir()) == [existing]
    assert existing.read_text(encoding="utf-8") == "previous run"


def test_close_failure_removes_all_outputs(tmp_path, monkeypatch):
    original_open = Path.open
    streams = []

    class FailingClose:
        def __init__(self, stream):
            self.stream = stream

        def __enter__(self):
            return self.stream

        def __exit__(self, *args):
            self.stream.close()
            raise OSError("flush failed")

    def open_with_close_failure(path, *args, **kwargs):
        stream = original_open(path, *args, **kwargs)
        streams.append(stream)
        return FailingClose(stream)

    monkeypatch.setattr(Path, "open", open_with_close_failure)
    with pytest.raises(OSError, match="flush failed"):
        with protocol._exclusive_output_streams(tmp_path) as outputs:
            for stream in outputs.values():
                stream.write("buffered output")
    assert all(stream.closed for stream in streams)
    assert not list(tmp_path.iterdir())


def test_successful_writes_remain_after_close(tmp_path):
    with protocol._exclusive_output_streams(tmp_path) as streams:
        for name, stream in streams.items():
            stream.write(name)
    assert all(stream.closed for stream in streams.values())
    assert {
        path.name: path.read_text(encoding="utf-8") for path in tmp_path.iterdir()
    } == {name: name for name in protocol.OUTPUT_FILENAMES}


@pytest.mark.parametrize(
    "experiment_eligible,dataset_eligible",
    [(False, False), (True, False), (False, True)],
)
@pytest.mark.parametrize("entrypoint", ["run_protocol", "main"])
def test_execution_requires_both_current_registry_flags(
    tmp_path, monkeypatch, capsys, experiment_eligible, dataset_eligible, entrypoint
):
    snapshot = RegistrySnapshot.load(ROOT)
    snapshot.experiments["EXP-MAP-A03"]["Controlled_Execution_Eligible"] = str(
        experiment_eligible
    ).lower()
    snapshot.datasets["DATA-ARITHMETIC"]["Controlled_Execution_Eligible"] = str(
        dataset_eligible
    ).lower()
    monkeypatch.setattr(protocol.RegistrySnapshot, "load", lambda root: snapshot)
    monkeypatch.setattr(
        protocol,
        "load_locked_arithmetic",
        lambda *args: pytest.fail("ineligible run accessed data"),
    )
    output_dir = tmp_path / "outputs"
    if entrypoint == "run_protocol":
        with pytest.raises(
            protocol.MCJProtocolError, match="not controlled-execution eligible"
        ):
            protocol.run_protocol(tmp_path / "input", output_dir, _config())
    else:
        assert (
            protocol.main(
                [
                    "--input",
                    str(tmp_path / "input"),
                    "--output-dir",
                    str(output_dir),
                    "--config",
                    str(CONFIG),
                ]
            )
            == 2
        )
        assert "not controlled-execution eligible" in capsys.readouterr().err
    assert not output_dir.exists()


def test_registry_activation_allows_locked_config_without_changing_controls(
    tmp_path, monkeypatch
):
    snapshot = RegistrySnapshot.load(ROOT)
    snapshot.experiments["EXP-MAP-A03"]["Controlled_Execution_Eligible"] = "true"
    snapshot.datasets["DATA-ARITHMETIC"]["Controlled_Execution_Eligible"] = "true"
    monkeypatch.setattr(protocol.RegistrySnapshot, "load", lambda root: snapshot)

    class ReachedDataLoading(Exception):
        pass

    def stop_before_execution(*args):
        raise ReachedDataLoading

    monkeypatch.setattr(protocol, "load_locked_arithmetic", stop_before_execution)
    config = _config()
    assert config["controls"]["controlled_execution_eligible"] is False
    with pytest.raises(ReachedDataLoading):
        protocol.run_protocol(tmp_path / "input", tmp_path / "outputs", config)
    assert not (tmp_path / "outputs").exists()
