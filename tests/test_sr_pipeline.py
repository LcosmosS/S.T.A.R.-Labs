import numpy as np

from src.symbolic_regression.sr_pipeline import SRPipeline


def test_scramble_is_reproducible_for_seed():
    x = np.arange(60, dtype=float).reshape(20, 3)
    a = SRPipeline(seed=42).scramble(x)
    b = SRPipeline(seed=42).scramble(x)
    assert np.array_equal(a, b)


def test_sr_pipeline_runs_on_finite_fixture():
    rng = np.random.default_rng(11)
    x = rng.random((20, 3))
    sr = SRPipeline(seed=11)
    best = sr.run(x, [])
    assert best is not None
