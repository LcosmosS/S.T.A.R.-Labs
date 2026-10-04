"""Regression tests for strict inference orchestration."""

import numpy as np
import pytest
import yaml

import src.pipeline.full_inference as full
from src.physics.symbolic_cosmology import SymbolicCosmology


def test_build_joint_likelihood_consumes_config_mapping(monkeypatch):
    datasets = {
        "PLANCK": {
            "R": 1.7,
            "lA": 300.0,
            "ombh2": 0.022,
            "cov": np.eye(3).tolist(),
        },
        "BAO": {
            "z": [0.1],
            "DM_over_rd": [3.0],
            "sigma_DM": [10.0],
            "H_rd": [10000.0],
            "sigma_H": [10000.0],
        },
        "CC": {"z": [0.1], "H": [73.0], "sigma": [10.0]},
    }
    monkeypatch.setattr(full, "DATASET_REGISTRY", datasets)
    config = {"datasets": {"planck": "PLANCK", "bao": "BAO", "cc": "CC"}}
    joint = full.build_joint_likelihood(config)

    model = SymbolicCosmology(
        "H0*sqrt(Ωm*(1+z)**3 + ΩΛ)",
        {
            "H0": 70.0,
            "Ωm": 0.3,
            "ΩΛ": 0.7,
            "Ωb": 0.04530612244897959,
            "r_s": 147.05,
        },
    )
    assert np.isfinite(joint(model))


def test_repository_placeholder_bao_is_rejected():
    config = {
        "datasets": {
            "planck": "PLANCK_2015",
            "bao": "DESI_BAO_DR1",
            "cc": "COSMIC_CHRONOMETERS",
        }
    }
    with pytest.raises(ValueError, match="DESI BAO dataset is empty"):
        full.build_joint_likelihood(config)


def test_run_full_inference_passes_full_config_to_builder(monkeypatch, tmp_path):
    config = {
        "model": {
            "H_expr": "H0",
            "param_names": ["H0"],
            "fixed_params": {},
        },
        "datasets": {
            "planck": "p",
            "bao": "b",
            "cc": "c",
            "sn": "s",
        },
        "priors": {"H0": [70.0, 2.0]},
        "proposal_widths": {"H0": 0.1},
        "mcmc": {"theta0": [70.0], "nsteps": 2, "seed": 1},
        "output_dir": str(tmp_path / "out"),
    }
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(config), encoding="utf-8")

    sn = {"z": [0.1], "mu": [38.0], "sigma_mu": [0.2]}
    monkeypatch.setattr(
        full,
        "load_dataset",
        lambda name: sn if name == "s" else {"name": name},
    )

    observed = {}

    class DummyJoint:
        def __call__(self, model):
            return 0.0

    def fake_build(arg):
        observed["config"] = arg
        return DummyJoint()

    class DummyMCMC:
        def __init__(self, *args, **kwargs):
            pass

        def run(self, theta0, nsteps):
            return np.asarray([theta0, theta0], dtype=float)

    class DummyFigures:
        def __init__(self, *args, **kwargs):
            pass

        def run(self, output_dir):
            return {"ok": True, "output_dir": output_dir}

    monkeypatch.setattr(full, "build_joint_likelihood", fake_build)
    monkeypatch.setattr(full, "JointMCMCPipeline", DummyMCMC)
    monkeypatch.setattr(full, "PaperFiguresPipeline", DummyFigures)

    result = full.run_full_inference(path)
    assert observed["config"]["datasets"]["planck"] == "p"
    assert result["ok"] is True
