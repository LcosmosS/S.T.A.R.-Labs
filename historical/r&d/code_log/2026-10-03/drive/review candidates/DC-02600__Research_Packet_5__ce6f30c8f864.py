import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from gplearn.genetic import SymbolicRegressor
import optuna
import warnings
from numpy.polynomial import Polynomial
from scipy.spatial import cKDTree


warnings.filterwarnings("ignore")


# Load the original dataset
df = pd.read_csv("merged_data.csv")


# Load the SDSS datasets and merge them
sdss_dr16 = pd.read_csv("V154sdss16.csv")  # V/154: SDSS DR16
sdss_dr12 = pd.read_csv("V147sdss12.csv")  # V/147: SDSS DR12


# Merge V/154 and V/147 on objID
sdss_merged = pd.merge(
