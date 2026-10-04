from sage.all import *
import pandas as pd
import numpy as np


# ————————————————————————
# 1. S.T.A.R. SCALING LAW: b → ρ (Inverse)
# ————————————————————————
def inverse_b_to_rho(b, mass_solar, v_disp_km_s, r_virial_mpc, log_base=10):
    """
    Inverse of S.T.A.R. b-coefficient law:
