# --- 1. Configuration ---
INPUT_FILE = 'merged_galspec_gz2.csv'
OUTPUT_PLOT_PREFIX = 'final_two_tier_synthesis_v19'
CHUNKSIZE = int(100000)
ROW_LIMIT = 300000  # Set to None for the full run.
TARGET_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
REQUIRED_COLUMNS = ['objid', 'ra', 'dec', 'z', 'logmass', 'petrorad_r']

# --- 2. Imports ---
import pandas as pd
import numpy as np
import sys
import warnings
from astropy.cosmology import Planck18 as cosmo
from astropy import units as u
from astropy.constants import G
from sage.all import EllipticCurve, QQ, factor

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score
import lightgbm as lgb
