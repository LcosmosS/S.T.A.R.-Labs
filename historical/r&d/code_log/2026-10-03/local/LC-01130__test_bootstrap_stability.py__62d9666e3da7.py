import numpy as np
from src.tda.bootstrap_stability import BootstrapStability

def test_bootstrap():
    B = BootstrapStability(num_bootstrap=5)
    X = np.random.rand(20, 3)
    barcode_fn = lambda X: [(0.0, 1.0)]
    landscapes = B.bootstrap_landscapes(barcode_fn, X)
    assert len(landscapes) == 5
