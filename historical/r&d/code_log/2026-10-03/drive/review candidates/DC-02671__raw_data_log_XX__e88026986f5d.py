from sage.all import *
import pandas as pd


# ———————— S.T.A.R. INVARIANT SCALING LAWS ————————
def star_offset(rho, R=3.383, Omega=0.422, T=1, rank=3):
    """Compute density offset using S.T.A.R. scaling"""
    Psi_r = rank * (rank + 1) / 2
    scale = (Omega * T**2 * exp(Psi_r / Omega)) / R
    return floor(rho * scale**rank * exp(-1 / Omega))


def star_multiplier(T=1, rank=3, Omega=0.422):
    """Compute recursive multiplier"""
    Psi_r = rank * (rank + 1) / 2
    return T**2 * exp(Psi_r / Omega)


def star_cosmic_recurrence(distance, rho, R=3.383, Omega=0.422, T=1, rank=3):
    """Generate numerators using S.T.A.R. invariants"""
    # x-numerator: distance-scaled via regulator
    num_x = round(distance * (R**(1/rank) * log(Omega) / log(3)))
    
    # y-numerator: recursive with invariant multiplier + offset
    mult = star_multiplier(T, rank, Omega)
    offset = star_offset(rho, R, Omega, T, rank)
    num_y = round(num_x * mult) + offset
    
    return num_x, num_y


def predict_star_generator(distance, rho, R=3.383, Omega=0.422, T=1, rank=3):
    """Predict full rational generator point"""
    num_x, num_y = star_cosmic_recurrence(distance, rho, R, Omega, T, rank)
    d_x = 3**4  # 81
    d_y = 3**6  # 729
    return (QQ(num_x)/d_x, QQ(num_y)/d_y, 1)


def normalize_point(P):
    """Convert projective [x:y:z] → affine (x/z, y/z, 1)"""
    if P is None: return None
    x, y, z = P
    return (x/z, y/z, 1) if z != 0 else P


# ———————— CLUSTER CORPUS ————————
clusters = [
    ("Virgo",      54,  6200),
    ("Coma",      321, 9980),
