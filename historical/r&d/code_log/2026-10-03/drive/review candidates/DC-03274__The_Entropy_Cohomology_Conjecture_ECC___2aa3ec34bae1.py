# Numerical and scientific computing
import numpy as np
import pandas as pd

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Machine learning models
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
import lightgbm as lgb

# Symbolic regression
from gplearn.genetic import SymbolicRegressor

# Hyperparameter optimization
import optuna

# Model evaluation
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# SHAP explainability
import shap

# Warning suppression for cleaner output
import warnings
warnings.filterwarnings('ignore')
