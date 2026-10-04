# --- 1. Configuration ---
INPUT_FILE = 'merged_galspec_gz2.csv'
OUTPUT_PLOT_PREFIX = 'predictive_analysis'
CHUNKSIZE = 100000
ROW_LIMIT = 300000 # Set to None for the full run.


REQUIRED_COLUMNS = ['objid', 'ra', 'dec', 'z', 'logmass', 'petrorad_r']


# --- 2. Imports ---
import pandas as pd
import numpy as np
import sys
import warnings
from astropy.cosmology import Planck18 as cosmo
from astropy import units as u
from astropy.constants import G
from sage.all import EllipticCurve, QQ


import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score
import lightgbm as lgb


warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid')


# --- 3. Scientific Derivation Functions (unchanged) ---
def calculate_distance_mpc(z):
    if z is None or not np.isfinite(z) or z <= 0: return np.nan
    try: return cosmo.comoving_distance(z).to(u.Mpc).value
    except: return np.nan


def convert_logmass_to_sm(logmass):
    if logmass is None or not np.isfinite(logmass): return np.nan
    return 10**logmass


def estimate_radius_ly(angular_size_arcsec, distance_mpc):
    if not (np.isfinite(angular_size_arcsec) and np.isfinite(distance_mpc) and angular_size_arcsec > 0 and distance_mpc > 0): return np.nan
    angle_rad = (angular_size_arcsec * u.arcsec).to(u.rad).value
    radius_mpc = distance_mpc * angle_rad
    return (radius_mpc * u.Mpc).to(u.lyr).value


def calculate_virial_energy(mass_sm, radius_ly):
    if not (np.isfinite(mass_sm) and np.isfinite(radius_ly) and mass_sm > 0 and radius_ly > 0): return np.nan
    mass_kg = mass_sm * 1.989e30; radius_m = radius_ly * 9.461e15
    potential_energy = -1 * G.value * (mass_kg ** 2) / radius_m
    return potential_energy / 2.0


# --- 4. SageMath Core Hypothesis Functions (unchanged) ---
def map_physics_to_curve_coeffs(distance_mly, density_kg_m3):
    if not (np.isfinite(distance_mly) and np.isfinite(density_kg_m3)): return np.nan, np.nan
    return QQ(-distance_mly), QQ(density_kg_m3)


def estimate_rank_category(E):
    try:
        rank = E.rank()
        if rank >= 3: return '3+'
        elif rank == 2: return '2'
        elif rank == 1: return '1'
        else: return '0'
    except Exception: return 'Unknown'
