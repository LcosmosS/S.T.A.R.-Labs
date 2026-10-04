import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
import seaborn as sns  # Used for correlation heatmap
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import HistGradientBoostingRegressor
from gplearn.genetic import SymbolicRegressor
import optuna
import warnings
from numpy.polynomial import Polynomial  # Used for SFR trend fitting
from scipy.spatial import cKDTree  # Used for clustering
import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostRegressor
from tqdm import tqdm
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.constants import L_sun
from dustmaps.sfd import SFDQuery                       # Key Notes: