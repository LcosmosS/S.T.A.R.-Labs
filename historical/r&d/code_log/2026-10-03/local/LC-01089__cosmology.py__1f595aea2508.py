"""
Cosmology Engine with Symbolic H(z)
==================================

This module defines a Cosmology class that accepts a symbolic expression
for H(z), parses it with sympy, lambdifies it, and integrates it to compute:

- comoving distance
- luminosity distance
- angular diameter distance
- distance modulus

This architecture supports:
- ΛCDM
- S.T.A.R. Model
- symbolic regression models
- arbitrary expansion histories
"""

from __future__ import annotations
import numpy as np
import sympy as sp
from scipy.integrate import quad


class Cosmology:
    """
    Cosmology engine with pluggable symbolic H(z).

    Parameters
    ----------
    H_expr : str
        A sympy-compatible expression for H(z).
        Example: "H0*sqrt(Ωm*(1+z)**3 + ΩΛ + a*z + b*z**2)"
    params : dict
        Dictionary of parameters appearing in H_expr.
        Example: {"H0": 70, "Ωm": 0.3, "ΩΛ": 0.7, "a": 0.1, "b": -0.02}
    """

    c = 299792.458  # km/s

    def __init__(self, H_expr: str, params: dict):
        self.H_expr = H_expr
        self.params = params

        # Symbolic variable
        z = sp.symbols("z")

        # Parse expression
        self.H_sym = sp.sympify(H_expr)

        # Lambdify for fast evaluation
        self.H = sp.lambdify(
            (z, *params.keys()),
            self.H_sym,
            modules=["numpy"]
        )

    def H_of_z(self, z):
        """Evaluate H(z) numerically."""
        return self.H(z, *self.params.values())

    def comoving_distance(self, z):
        """Compute comoving distance Dc(z) = c ∫ dz / H(z)."""
        integrand = lambda zp: self.c / self.H_of_z(zp)
        return quad(integrand, 0, z)[0]

    def luminosity_distance(self, z):
        """DL = (1+z) * Dc."""
        return (1 + z) * self.comoving_distance(z)

    def angular_diameter_distance(self, z):
        """DA = Dc / (1+z)."""
        return self.comoving_distance(z) / (1 + z)

    def distance_modulus(self, z):
        """μ = 5 log10(DL / 10 pc). DL in Mpc."""
        DL_Mpc = self.luminosity_distance(z)
        DL_pc = DL_Mpc * 1e6
        return 5 * (np.log10(DL_pc) - 1)
