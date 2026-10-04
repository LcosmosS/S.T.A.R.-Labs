# --- 1. Configuration ---
INPUT_FILE = 'merged_galspec_gz2.csv'
OUTPUT_PLOT_PREFIX = 'predictive_analysis'
CHUNKSIZE = int(100000)
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
