import numpy as np
from src.acsc.projection import ArithmeticProjector, project

def test_project_exercises_production_api():
    records = [{"delta": -11, "conductor": 11, "rank": 0}]
    coords = project(records)
    assert coords.shape == (1, 3)
    assert np.isfinite(coords).all()

def test_embedding_is_reproducible_and_default_deterministic():
    records = [{"delta": -11, "conductor": 11, "rank": 1}]
    p = ArithmeticProjector()
    base = p.project(records)
    assert np.array_equal(p.embed_to_cosmic(base), p.embed_to_cosmic(base))
    assert np.array_equal(
        p.embed_to_cosmic(base, seed=7, noise_scale=0.05),
        p.embed_to_cosmic(base, seed=7, noise_scale=0.05),
    )
