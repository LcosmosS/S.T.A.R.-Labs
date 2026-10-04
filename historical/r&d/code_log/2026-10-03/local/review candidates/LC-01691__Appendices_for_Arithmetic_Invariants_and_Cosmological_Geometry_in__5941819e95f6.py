REQUIRED_COLUMNS = ['objid', 'ra', 'dec', 'z', 'logmass', 'petrorad_r', 'metallicity']
T_COSMO = 17.18
REG_COSMO = 2.51
KAPPA = 1.0
SELMER_BOUND = 5
MAX_CONDUCTOR = 10**8
KB = 1.380649e-23  # Boltzmann constant (J/K)
COHOMOLOGY_WEIGHT = 1e-3  # Scaling factor for Betti number
ENTROPY_GRADIENT_WEIGHT = 1e-2  # Scaling factor for entropy gradient

# --- 2. Imports ---
import pandas as pd
import numpy as np
import warnings
from astropy.cosmology import Planck18 as cosmo
from astropy import units as u
from sage.all import EllipticCurve, QQ, factor, parallel
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px
import ipywidgets as widgets
from IPython.display import display
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, classification_report
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor,
