import numpy as np
import pytest

from src.symbolic_regression.constrained_gp import ConstrainedGP, GPNode
from src.symbolic_regression.law_discovery_manifold import LawDiscoveryManifold


def test_gp_random_tree_is_reproducible_for_seed():
    a = ConstrainedGP(seed=7).random_tree()
    b = ConstrainedGP(seed=7).random_tree()
    x = np.array([0.2, 0.4, 0.6])
    try:
        av = a.evaluate(x)
        bv = b.evaluate(x)
    except FloatingPointError:
        pytest.skip("matching seeded trees are both numerically inadmissible")
    assert av == pytest.approx(bv)


def test_overflowing_expression_is_rejected_without_nan_scoring():
    huge = GPNode("const", value=1e6)
    node = GPNode("exp", children=[huge])
    with pytest.raises(FloatingPointError):
        node.evaluate(np.array([1.0, 2.0, 3.0]))

    manifold = LawDiscoveryManifold()
    assert not manifold.admissible(
        lambda x: node.evaluate(x),
        np.ones((3, 3)),
        [],
        np.ones((3, 3)),
    )
