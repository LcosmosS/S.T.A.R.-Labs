import numpy as np
from src.tda.witness_complex import WitnessComplex

def test_witness_complex():
    X = np.random.rand(50, 3)
    W = WitnessComplex(num_landmarks=5)
    complex_data = W.build_complex(X)
    assert "landmarks" in complex_data
    assert "edges" in complex_data
