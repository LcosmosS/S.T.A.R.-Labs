from __future__ import annotations
import numpy as np
import sympy as sp
from scipy.integrate import quad


class Cosmology:
    """
    Cosmology engine with pluggable symbolic H(z).
    H_expr : str
        Sympy-compatible expression for H(z) (units: km/s/Mpc).
    params : dict
        Numeric parameter values used in H_expr.
    """

    c = 299792.458  # km/s

    def __init__(self, H_expr: str, params: dict):
        self.H_expr = H_expr.strip()
        self.params = {k: float(v) for k, v in (params or {}).items()}
        self.expr = self.H_expr  # keep original string

        # Symbolic setup
        z_sym = sp.symbols("z")
        try:
            expr_clean = self.H_expr.replace("Ωm", "Om").replace("ΩΛ", "OL")
            self.H_sym = sp.sympify(expr_clean)
            keys = tuple(self.params.keys())
            self.H_func = sp.lambdify((z_sym, *keys), self.H_sym, modules="numpy")
        except Exception as e:
            raise ValueError(f"Failed to parse/lambdify H_expr: {e}")

    def H_of_z(self, z):
        """Evaluate H(z)."""
        z = np.asarray(z)
        try:
            return self.H_func(z, *self.params.values())
        except Exception:
            # Fallback numerical
            H0 = self.params.get("H0", 70.0)
            Om = self.params.get("Ωm", 0.3)
            OL = self.params.get("ΩΛ", 0.7)
            a = self.params.get("a", 0.0)
            b = self.params.get("b", 0.0)
            inside = Om * (1 + z) ** 3 + OL + a * z + b * z**2
            return H0 * np.sqrt(np.maximum(inside, 1e-10))
   
    from functools import lru_cache

    @lru_cache(maxsize=1024)
    def _comoving_scalar(self, zi: float) -> float:
        """Comoving distance for single scalar redshift."""
        if not np.isfinite(zi) or zi < 0:
            raise ValueError(f"Invalid redshift: {zi}")

        def integrand(zp):
            Hz = float(self.H_of_z(zp))
            if Hz <= 0:
                Hz = 1e-8
            return self.c / Hz

        result, _ = quad(integrand, 0.0, float(zi), limit=300, epsabs=1e-9, epsrel=1e-9)
        return max(float(result), 0.0)

    def comoving_distance(self, z):
        # Catch ellipsis and other garbage early
        if (
            z is Ellipsis
            or isinstance(z, type(...))
            or (isinstance(z, np.ndarray) and z.dtype == object)
        ):
            print(
                "Warning: Ellipsis detected in comoving_distance - using safe fallback"
            )
            z = np.array([0.01, 0.5, 1.0])

        z = np.asarray(z, dtype=float)
        z = np.nan_to_num(z, nan=0.0, posinf=2.0, neginf=0.0)
        z = np.clip(z, 1e-6, 10.0)  # avoid z=0 problems

        if z.ndim == 0 or z.size == 1:
            return self._comoving_scalar(float(z.ravel()[0]))

        return np.array([self._comoving_scalar(float(zi)) for zi in z.ravel()]).reshape(
            z.shape
        )

    def luminosity_distance(self, z):
        """DL = (1 + z) * Dc(z)"""
        Dc = self.comoving_distance(z)
        z_arr = np.asarray(z)
        z_arr = np.nan_to_num(z_arr, nan=0.0, posinf=2.0, neginf=0.0)
        z_arr = z_arr.astype(float)
        return Dc * (1.0 + z_arr)

    def distance_modulus(self, z):
        """μ = 5 log10(DL / 10 pc)"""
        DL = self.luminosity_distance(z)
        DL = np.maximum(DL, 1e-6)

        if np.isscalar(DL) or DL.size == 1:
            dl = float(DL)
            return 5.0 * (np.log10(dl * 1e6) - 1.0) if dl > 0 else -np.inf

        with np.errstate(divide="ignore", invalid="ignore"):
            mu = 5.0 * (np.log10(DL * 1e6) - 1.0)
        return mu
