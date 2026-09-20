"""Tests for the public acsc projection API."""
import numpy as np
from acsc.projection import ArithmeticProjector, project

def test_project_exercises_production_api():
    """Project one arithmetic record and verify finite 3D output."""
    records = [{"delta": -11, "conductor": 11, "rank": 0}]
    coords = project(records)
    assert coords.shape == (1, 3)
    assert np.isfinite(coords).all()

def test_embedding_is_reproducible_and_default_deterministic():
    """Verify deterministic defaults and reproducible seeded noise."""
    records = [{"delta": -11, "conductor": 11, "rank": 1}]
    p = ArithmeticProjector()
    base = p.project(records)
    deterministic = p.embed_to_cosmic(base)
    assert np.array_equal(deterministic, p.embed_to_cosmic(base))
    noisy = p.embed_to_cosmic(base, seed=7, noise_scale=0.05)
    assert np.array_equal(noisy, p.embed_to_cosmic(base, seed=7, noise_scale=0.05))
    assert not np.array_equal(noisy, deterministic)
