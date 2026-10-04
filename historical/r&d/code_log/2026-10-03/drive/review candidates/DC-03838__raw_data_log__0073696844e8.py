import pandas as pd
import numpy as np
from xgboost import XGBRegressor
import warnings
warnings.filterwarnings('ignore')


print("🚀 Generating requested outputs (hall_of_fame, feature_importance, predictions)")


# Load data
synth = pd.read_csv("synthetic_cosmos_final/synthetic_cosmic_catalog_calibrated.csv")
