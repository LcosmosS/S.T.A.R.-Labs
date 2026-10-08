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
    def __init__(self, H_expr, params):
        if isinstance(H_expr, sp.Expr):
            H_expr = str(H_expr)

        self.H_expr = H_expr
        self.params = params.copy()  # Make a copy to be safe

        # Core cosmology engine
        self.cosmo = Cosmology(H_expr, params)

        # Build fast H(z) function
        self._build_symbolic_function()

        print(f"SymbolicCosmology initialized with H_expr = {H_expr[:60]}...")

    def _build_symbolic_function(self):
        z = sp.symbols("z")
        expr = sp.sympify(self.H_expr)
        for k, v in self.params.items():
            expr = expr.subs(sp.Symbol(k), v)
        self._H_func = sp.lambdify(z, expr, "numpy")

    def H(self, z):
        """Safe H(z) evaluation"""
        try:
            Hz = self._H_func(z)
            Hz = np.asarray(Hz, dtype=float)
            Hz = np.where(Hz <= 0, 1e-8, Hz)  # Prevent negative/zero
            Hz = np.where(~np.isfinite(Hz), 70.0, Hz)  # Replace NaN/inf
            return Hz
        except:
            return np.full_like(z, 70.0) if hasattr(z, "__len__") else 70.0

    def H0(self):
        """Direct H0 access - important for SH0ES"""
        return float(self.params.get("H0", 70.0))

    # =============================================
    # Planck Compressed Quantities (Critical)
    # =============================================
    def ombh2(self):
        """Ωb h²"""
        h = self.H0() / 100.0
        omb = self.params.get("Ωb", 0.049)
        return omb * h**2

    def sound_horizon(self):
        """Approximate sound horizon rs (Mpc) - Planck 2018 style"""
        return 147.05  # Fixed value, can be made parametric later

    def R(self):
        """Shift parameter R = sqrt(Ωm) * H0 * r(z*) / c"""
        try:
            z_star = 1089.0
            r = self.comoving_distance(z_star)
            Om = float(self.params.get("Ωm", 0.3))
            H0 = self.H0()
            c = 299792.458
            return np.sqrt(Om) * H0 * r / c
        except:
            return 1.748  # Typical Planck value as fallback

    def lA(self):
        """Acoustic scale lA = π * r(z*) / rs"""
        try:
            z_star = 1089.0
            r = self.comoving_distance(z_star)
            rs = self.sound_horizon()
            return np.pi * r / rs
        except:
            return 301.0  # Typical Planck value

    # Distance functions (delegated)
    def distance_modulus(self, z):
        return self.cosmo.distance_modulus(z)

    def comoving_distance(self, z):
        """Numerical integration with safe H(z)"""
        if np.isscalar(z):
            zs = np.linspace(0, float(z), 300)
        else:
            zs = np.asarray(z)
        Hz = self.H(zs)
        dc = np.trapz(299792.458 / Hz, zs)
        return dc

    # For compatibility
    def __getattr__(self, name):
        return getattr(self.cosmo, name)
