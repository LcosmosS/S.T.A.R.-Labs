# Import necessary libraries
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


from sage.all import EllipticCurve, QQ, pari, RR, factor, Integer, sqrt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr
import math
import random


# Define foundational constants from your research
# KAPPA is the geometric scaling factor derived from the Virgo Cluster and
# later validated as a data-driven constant from the statistical model.
# [1, 1]
DATA_DRIVEN_KAPPA = 31.5926


# Cosmological constants from the "Natural Normalization" study [1]
T_H = 1.44e10  # Hubble Time in years
AGE_UNIVERSE = 1.38e10 # Age of the Universe in years
OMEGA_TILDE = AGE_UNIVERSE / T_H # Dimensionless age ratio
SHA_COSMO = 0.315 # Matter density parameter (Omega_M)


# --- Core Analysis Function ---
def analyze_curve(a, b, is_original=False):
    """
    Analyzes an elliptic curve, computes its invariants, and handles potential
