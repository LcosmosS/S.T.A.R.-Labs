import pandas as pd
import numpy as np
from sklearn.model_selection import KFold, cross_val_score, GridSearchCV, train_test_split
from sklearn.ensemble import RandomForestRegressor  # Example model; adjust as needed
from sklearn.metrics import mean_squared_error, r2_score
