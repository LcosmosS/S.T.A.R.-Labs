import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import shap
import matplotlib.pyplot as plt
import warnings


warnings.filterwarnings("ignore")


# Load your cleaned and merged dataset
df = pd.read_csv("filtered_dataset.csv")


# Drop rows with missing values just in case
df.dropna(inplace=True)


# Define target and features
target = 'log_SFR_Ha'
