"""
Symbolic Regression Integration for Cosmology
=============================================

Wraps a symbolic regression model into the Cosmology engine.
Provides numerical stability for MCMC and symbolic models.
"""

from __future__ import annotations
import sympy as sp
import numpy as np
from src.physics.cosmology import Cosmology


class SymbolicCosmology:
    """
    Wraps a symbolic regression model into a Cosmology engine.

    Parameters
    ----------
    H_expr : str or sympy.Expr
        Symbolic expression for H(z).
    params : dict
        Parameter dictionary for the expression.
    """

    def __init__(self, H_expr, params):
        # Convert sympy expression to string if needed
        if isinstance(H_expr, sp.Expr):
            H_expr = str(H_expr)

        self.H_expr = H_expr
        self.params = params

        # Build underlying cosmology engine
        self.cosmo = Cosmology(H_expr, params)

        # Build symbolic H(z) function
        self._build_symbolic_function()

    # ---------------------------------------------------------
    # Build symbolic function
    # ---------------------------------------------------------
    def _build_symbolic_function(self):
        z = sp.symbols("z")
        expr = sp.sympify(self.H_expr)

        # Substitute parameters
        for k, v in self.params.items():
            expr = expr.subs(sp.Symbol(k), v)

        # Lambdify
        self._H_func = sp.lambdify(z, expr, "numpy")

    # ---------------------------------------------------------
    # Safe H(z)
    # ---------------------------------------------------------
    def H(self, z):
        """
        Safe evaluation of H(z) with numerical stability fixes.
        """
        Hz = self._H_func(z)
        Hz = np.asarray(Hz, dtype=float)

        # Replace non-finite values
        Hz = np.where(np.isfinite(Hz), Hz, np.nan)

        # Clamp negative sqrt arguments
        Hz = np.where(Hz < 0, np.nan, Hz)

        # Replace NaNs with a large penalty
        Hz = np.where(np.isnan(Hz), 1e12, Hz)

        return Hz

    # ---------------------------------------------------------
    # Distance functions (delegated to Cosmology)
    # ---------------------------------------------------------
    def distance_modulus(self, z):
        return self.cosmo.distance_modulus(z)

    def luminosity_distance(self, z):
        return self.cosmo.luminosity_distance(z)

    # ---------------------------------------------------------
    # Comoving distance (override with safe H(z))
    # ---------------------------------------------------------
    def comoving_distance(self, z):
        zs = np.linspace(0, z, 200)
        Hz = self.H(zs)
        return np.trapz(299792.458 / Hz, zs)

    # ---------------------------------------------------------
    # Planck compressed likelihood support
    # ---------------------------------------------------------
    def ombh2(self):
        if "Ωb" in self.params:
            return self.params["Ωb"] * (self.params["H0"] / 100)**2
        return 0.0224  # fallback

    def sound_horizon(self):
        return 147.1  # Mpc (Planck 2018)

    def R(self):
        z_star = 1089.0
        r = self.comoving_distance(z_star)
        Om = self.params["Ωm"]
        H0 = self.params["H0"]
        return np.sqrt(Om) * H0 * r / 299792.458

    def lA(self):
        z_star = 1089.0
        r = self.comoving_distance(z_star)
        rs = self.sound_horizon()
        return np.pi * r / rs
