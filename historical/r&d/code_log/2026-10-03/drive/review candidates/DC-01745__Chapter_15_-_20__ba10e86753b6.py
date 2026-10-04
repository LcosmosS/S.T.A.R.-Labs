import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import xgboost as xgb
import lightgbm as lgb
import shap
import matplotlib.pyplot as plt

# --- Block 1: Data Loading and Preprocessing ---
def load_and_clean_data(filepath):
