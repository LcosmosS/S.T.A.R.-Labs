import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split, KFold 
from sklearn.ensemble import RandomForestRegressor 
from sklearn.metrics import mean_squared_error import joblib
def calculate_k(masses): """ Calculates the normalization constant K.
