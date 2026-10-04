# --- 1. Configuration --- 
INPUT_FILE = 'GalSpecExtra.csv'
OUTPUT_PLOT_PREFIX = 'final_two_tier_synthesis_v47' 
CHUNKSIZE = 50000
ROW_LIMIT = 866000
TARGET_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47] 
REQUIRED_COLUMNS = ['objid', 'ra', 'dec', 'z', 'logmass', 'petrorad_r', 'metallicity'] 
T_COSMO = 17.18 
REG_COSMO = 2.51 
KAPPA = 1.0 
SELMER_BOUND = 5 
MAX_CONDUCTOR = 10**8 
KB = 1.380649e-23  # Boltzmann constant (J/K) 
COHOMOLOGY_WEIGHT = 1e-3  # Scaling factor for Betti number 
ENTROPY_GRADIENT_WEIGHT = 1e-2  # Scaling factor for entropy gradient 
MAX_COHOM_POINTS = 1000  # Increased for better cohomology


# --- 2. Imports --- 
import pandas as pd 
import numpy as np 
import warnings 
from astropy.cosmology import Planck18 as cosmo 
from astropy import units as u 
from sage.all import EllipticCurve, QQ, factor, parallel 
import matplotlib.pyplot as plt 
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns 
import altair as alt 
import plotly.express as px 
from sklearn.model_selection import train_test_split, cross_val_score 
from sklearn.preprocessing import StandardScaler 
from sklearn.pipeline import Pipeline 
from sklearn.metrics import r2_score, classification_report 
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, HistGradientBoostingClassifier, HistGradientBoostingRegressor, StackingClassifier, StackingRegressor 
from sklearn.cluster import DBSCAN, KMeans 
from sklearn.impute import KNNImputer 
from sklearn.inspection import permutation_importance 
from sklearn.decomposition import PCA 
from sklearn.manifold import TSNE 
from sklearn.neighbors import KernelDensity 
from datetime import datetime
try: 
    from xgboost import XGBClassifier, XGBRegressor 
