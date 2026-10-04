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
    return num_x, num_y


def predict_star_generator(r, rho, R=3.383, Omega=0.422, T=1, r=3):
    num_x, num_y = star_cosmic_recurrence(r, rho, R, Omega, T, r)
    d_x = 3**4  # 81
    d_y = 3**6  # 729
    return (QQ(num_x)/d_x, QQ(num_y)/d_y, 1)


# Cluster corpus
clusters = [
    ("Virgo", 54, 6200),
    ("Coma", 321, 9980),
