import numpy as np
from src.symbolic_regression.sr_pipeline import SRPipeline

def test_sr_pipeline_runs():
    SR = SRPipeline()
    X = np.random.rand(20, 3)
    isogeny_pairs = []
    best = SR.run(X, isogeny_pairs)
    assert best is not None
