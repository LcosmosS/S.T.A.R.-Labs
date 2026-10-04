import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import os


# Ensure plots directory exists
if not os.path.exists('plots'):
    os.makedirs('plots')


def get_model(model_type):
    """
    Return the specified model type.
