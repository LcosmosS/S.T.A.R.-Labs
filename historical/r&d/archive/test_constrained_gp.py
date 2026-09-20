import numpy as np
from src.symbolic_regression.constrained_gp import ConstrainedGP

def test_gp_initialization():
    GP = ConstrainedGP()
    tree = GP.random_tree()
    assert tree is not None
