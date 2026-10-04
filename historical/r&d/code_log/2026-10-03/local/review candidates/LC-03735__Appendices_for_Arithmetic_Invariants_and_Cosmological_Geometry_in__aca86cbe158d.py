# --- 1. Configuration ---
# Edit these variables to control the script's behavior.
INPUT_FILE = 'merged_galspec_gz2.csv'
OUTPUT_FILE = 'sagemath_run_results.csv'
CHUNKSIZE = int(100000)  # Number of rows to process at a time
ROW_LIMIT = 500000  # Set to None to process the full file, or a number for testing.

# --- 2. Imports ---
# Standard scientific libraries
import pandas as pd
import numpy as np
import sys
from astropy.cosmology import Planck18 as cosmo
from astropy import units as u
from astropy.constants import G

# SageMath specific imports
# These will be available when running in a SageMath environment.
from sage.all import EllipticCurve, QQ

# --- 3. Scientific Derivation Functions ---

def calculate_distance_mpc(z):
    """Calculates comoving distance from redshift using Planck18 cosmology."""
    if z is None or not np.isfinite(z) or z <= 0:
        return np.nan
    try:
        return cosmo.comoving_distance(z).to(u.Mpc).value
    except (ValueError, TypeError):
        return np.nan

def convert_logmass_to_sm(logmass):
    """Converts logarithmic mass to stellar mass in solar mass units."""
    if logmass is None or not np.isfinite(logmass):
        return np.nan
    return 10**logmass

def estimate_radius_ly(angular_size_arcsec, distance_mpc):
