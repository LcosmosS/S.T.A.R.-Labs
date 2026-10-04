# star_scale_integration.py
from sage.all import *
import pandas as pd

def invariant_scaling(rho, R=3.383, Omega=0.422, T=1, r=3):
    """Compute scaled offset using S.T.A.R. laws"""
    Psi_r = r * (r + 1) / 2
    scale_factor = (Omega * T**2 * exp(Psi_r / Omega)) / R
    offset = floor(rho * scale_factor**r * exp(-1 / Omega))
    return offset

def star_cosmic_recurrence(r, rho, R=3.383, Omega=0.422, T=1, r=3):
    """Invariant-integrated recurrence"""
    num_x = round(r * (R**(1/r) * log(Omega) / log(3)))
    multiplier = T**2 * exp(Psi_r / Omega)
    offset = invariant_scaling(rho, R, Omega, T, r)
    num_y = round(num_x * multiplier) + offset