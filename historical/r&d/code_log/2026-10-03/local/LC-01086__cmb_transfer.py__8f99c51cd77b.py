"""
cmb_transfer.py
----------------
Implements the symbolic Sachs–Wolfe transfer function used in the
S.T.A.R. Model to propagate arithmetic–entropy perturbations into
CMB anisotropies.

ΔT/T = Φ/3 + ∫ (Φ' + Ψ') dη

Here Φ is modified by ACSC projection geometry and ECC entropy curvature.
"""

import numpy as np
from src.data.load_sky_surveys import load_sky_surveys

def test_sky_surveys_load():
    df1, df2 = load_sky_surveys(downsample=100, validate_schema=True)
    assert len(df1) > 0
    assert len(df2) > 0

class CMBTransfer:
    """
    Computes symbolic Sachs–Wolfe and ISW contributions.
    """

    def __init__(self, alpha=0.01):
        self.alpha = alpha  # arithmetic–entropy coupling strength

    def symbolic_potential(self, invariants, entropy_curvature):
        """
        Compute Φ_symbolic = Ω_E * r * (1 + α * tanh(K_entropy)).
        """
        omega = invariants["omega"]
        rank = invariants["rank"]
        return omega * rank * (1 + self.alpha * np.tanh(entropy_curvature))

    def sachs_wolfe(self, potential):
        """
        ΔT/T = Φ/3
        """
        return potential / 3.0

    def integrated_sachs_wolfe(self, potential_history, eta):
        """
        Compute ∫ (Φ') dη using finite differences.
        """
        dphi = np.gradient(potential_history, eta)
        return np.trapz(dphi, eta)

    def cmb_anisotropy(self, invariants, entropy_curvature, potential_history, eta):
        """
        Full symbolic CMB anisotropy prediction.
        """
        phi = self.symbolic_potential(invariants, entropy_curvature)
        sw = self.sachs_wolfe(phi)
        isw = self.integrated_sachs_wolfe(potential_history, eta)
        return sw + isw
