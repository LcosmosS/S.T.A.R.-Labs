import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import os


# Ensure plots directory exists
if not os.path.exists('plots'):
    os.makedirs('plots')


def create_features(df, high_mass_threshold, low_mass_threshold, additional_features=None):
    """
    Generate feature matrix with non-linear terms and mass-specific adjustments.
