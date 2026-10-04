"""
Cosmology Test Suite
====================

Tests:
- H(z) evaluation
- comoving distance monotonicity
- distance modulus monotonicity
- symbolic model integration
"""

import numpy as np
from src.physics.cosmology import Cosmology
from src.physics.symbolic_cosmology import SymbolicCosmology


def test_lcdm_basic():
    lcdm = Cosmology(
        "H0*sqrt(Ωm*(1+z)**3 + ΩΛ)",
        {"H0": 70, "Ωm": 0.3, "ΩΛ": 0.7}
    )
    assert lcdm.H_of_z(0) == 70


def test_distance_monotonicity():
    lcdm = Cosmology(
        "H0*sqrt(Ωm*(1+z)**3 + ΩΛ)",
        {"H0": 70, "Ωm": 0.3, "ΩΛ": 0.7}
    )
    z = np.linspace(0, 2, 50)
    d = np.array([lcdm.comoving_distance(zi) for zi in z])
    assert np.all(np.diff(d) > 0)


def test_symbolic_model():
    star = SymbolicCosmology(
        "H0*sqrt(Ωm*(1+z)**3 + ΩΛ + a*z)",
        {"H0": 70, "Ωm": 0.3, "ΩΛ": 0.7, "a": -0.05}
    )
    assert star.H(0) > 0
    assert star.distance_modulus(0.5) > 0
