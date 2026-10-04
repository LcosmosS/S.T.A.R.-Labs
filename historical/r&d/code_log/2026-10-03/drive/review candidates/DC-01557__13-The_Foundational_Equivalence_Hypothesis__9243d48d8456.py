from sage.all import EllipticCurve, QQ
import pandas as pd
from math import log10


def calculate_b_coefficient(mass, vel_disp, radius_mpc):
    """
    Calculates the 'b' coefficient (rho) using the refined mapping formula
