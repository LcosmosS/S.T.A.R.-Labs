"""Regression tests for strict inference orchestration."""

import numpy as np
import pytest
import yaml

import src.pipeline.full_inference as full
from src.physics.symbolic_cosmology import SymbolicCosmology


def _base_config(datasets):
    return {
        "model": {
            "H_expr": "H0*sqrt(Ωm*(1+z)**3 + ΩΛ)",
            "param_names": ["H0", "Ωm", "ΩΛ"],
            "fixed_params": {"Ωb": 0.04530612244897959, "r_s": 147.05},
        },
        "datasets": datasets,
        "likelihoods": {
            "shoes_H0": 73.04,
            "shoes_sigma": 1.04,
            "bao_r_d": 147.1,
        },
        "priors": {
            "H0": [70.0, 2.0],
            "Ωm": [0.3, 0.05],
            "ΩΛ": [0.7, 0.05],
        },
        "proposal_widths": {"H0": 0.1, "Ωm": 0.01, "ΩΛ": 0.01},
        "mcmc": {"theta0": [70.0, 0.3, 0.7], "nsteps": 2, "seed": 1},
        "output_dir": "unused",
    }


def test_build_joint_likelihood_includes_supernova_term(monkeypatch):
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
        "SN": {"z": [0.1], "mu": [38.0], "sigma_mu": [0.2]},
    }
    monkeypatch.setattr(full, "DATASET_REGISTRY", datasets)
    config = _base_config(
        {"planck": "PLANCK", "bao": "BAO", "cc": "CC", "sn": "SN"}
    )
    joint = full.build_joint_likelihood(config)

    model = SymbolicCosmology(
        config["model"]["H_expr"],
        {
            "H0": 70.0,
            "Ωm": 0.3,
            "ΩΛ": 0.7,
            "Ωb": 0.04530612244897959,
            "r_s": 147.05,
        },
    )
    total = joint(model)
    without_sn = (
        joint.planck_like.log_likelihood(model)
        + joint.bao_like.log_likelihood(model)
        + joint.cc_like.log_likelihood(model)
    )
    assert np.isfinite(total)
    assert total == pytest.approx(without_sn + joint.sn_like.log_likelihood(model))


def test_repository_placeholder_bao_is_rejected():
    config = _base_config(
        {
            "planck": "PLANCK_2015",
            "bao": "DESI_BAO_DR1",
            "cc": "COSMIC_CHRONOMETERS",
            "sn": "PANTHEON_PLUS_FULL",
        }
    )
    with pytest.raises(ValueError, match="DESI BAO dataset is empty"):
        full.build_joint_likelihood(config)


def test_run_full_inference_passes_full_config_to_builder(monkeypatch, tmp_path):
    config = {
        "model": {
            "H_expr": "H0",
            "param_names": ["H0"],
            "fixed_params": {},
        },
        "datasets": {"planck": "p", "bao": "b", "cc": "c", "sn": "s"},
        "likelihoods": {
            "shoes_H0": 73.04,
            "shoes_sigma": 1.04,
            "bao_r_d": 147.1,
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


def test_inference_config_requires_explicit_likelihood_assumptions():
    config = _base_config({"planck": "p", "bao": "b", "cc": "c", "sn": "s"})
    del config["likelihoods"]["bao_r_d"]
    with pytest.raises(KeyError, match="likelihoods.bao_r_d"):
        full._validate_config(config)


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("shoes_H0", np.inf),
        ("shoes_H0", np.nan),
        ("shoes_H0", 0.0),
        ("shoes_sigma", np.inf),
        ("shoes_sigma", np.nan),
        ("shoes_sigma", 0.0),
        ("bao_r_d", np.inf),
        ("bao_r_d", np.nan),
        ("bao_r_d", 0.0),
    ],
)
def test_inference_config_rejects_nonfinite_or_nonpositive_likelihood_values(
    key, value
):
    config = _base_config({"planck": "p", "bao": "b", "cc": "c", "sn": "s"})
    config["likelihoods"][key] = value

    with pytest.raises(ValueError, match=f"likelihoods.{key}"):
        full._validate_config(config)
