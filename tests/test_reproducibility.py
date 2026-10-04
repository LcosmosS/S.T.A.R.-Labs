"""Reproducibility tests for stochastic utilities and MCMC."""

import numpy as np
import pytest

from src.acsc.null_models import generate_null_point_cloud
from src.acsc.robustness import gaussian_jitter_test, subsample_stability
from src.physics.mcmc_cosmology import MCMCCosmologyFitter
from src.physics.mcmc_joint_pipeline import JointMCMCPipeline


def test_null_cloud_repeats_for_declared_seed():
    a = generate_null_point_cloud(10, seed=42)
    b = generate_null_point_cloud(10, seed=42)
    assert np.array_equal(a, b)


def test_robustness_utilities_repeat_for_declared_seed():
    coords = np.arange(30, dtype=float).reshape(10, 3)
    a = subsample_stability(coords, seed=7)
    b = subsample_stability(coords, seed=7)
    assert all(np.array_equal(a[key], b[key]) for key in a)

    ja = gaussian_jitter_test(coords, n_trials=2, seed=9)
    jb = gaussian_jitter_test(coords, n_trials=2, seed=9)
    assert all(np.array_equal(x, y) for x, y in zip(ja, jb))


class _QuadraticLikelihood:
    def __call__(self, model):
        return -0.5 * ((model.H0() - 70.0) / 2.0) ** 2


def _sampler(seed):
    return JointMCMCPipeline(
        "H0",
        ["H0"],
        {"H0": (70.0, 2.0)},
        {"H0": 0.1},
        _QuadraticLikelihood(),
        seed=seed,
    )


def test_mcmc_repeats_for_declared_seed():
    a = _sampler(123).run([70.0], nsteps=20)
    b = _sampler(123).run([70.0], nsteps=20)
    assert np.array_equal(a, b)


def test_mcmc_rejects_invalid_initial_state():
    with pytest.raises(ValueError, match="non-finite posterior"):
        _sampler(1).run([-1.0], nsteps=5)


def test_legacy_cosmology_fitter_now_repeats_for_declared_seed():
    args = (
        "H0",
        ["H0"],
        {"H0": (70.0, 2.0)},
        {"H0": 0.1},
    )
    z = np.array([0.1, 0.2])
    mu = np.array([38.0, 40.0])
    sigma = np.array([1.0, 1.0])

    a = MCMCCosmologyFitter(*args, seed=31).run(
        z, mu, sigma, [70.0], nsteps=12
    )
    b = MCMCCosmologyFitter(*args, seed=31).run(
        z, mu, sigma, [70.0], nsteps=12
    )
    assert np.array_equal(a, b)
