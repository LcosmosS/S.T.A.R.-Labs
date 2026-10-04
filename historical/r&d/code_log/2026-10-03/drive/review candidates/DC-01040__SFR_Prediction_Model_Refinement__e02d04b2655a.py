import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt


# --- Load Datasets ---
print("Loading datasets...")
magphys = pd.read_csv('MagPhys.csv')[['CATAID', 'mass_stellar_best_fit', 'sSFR_0_1Gyr_best_fit',
'L_dust_best_fit', 'tau_V_best_fit', 'mass_dust_best_fit',
'metalicity_Z_Zo_percentile50', 'agem_percentile50',
