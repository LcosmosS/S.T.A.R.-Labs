import numpy as np
from src.tda.symbolic_persistence import SymbolicPersistence

def test_betti_numbers():
    S = SymbolicPersistence()
    X = np.random.rand(10, 3)
    barcodes = S.barcodes(X)
    bettis = S.betti_numbers(barcodes)
    assert len(bettis) > 0
