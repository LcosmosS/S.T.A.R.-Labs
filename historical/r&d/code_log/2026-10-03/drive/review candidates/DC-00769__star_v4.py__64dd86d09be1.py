import argparse
import os
import subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import gcd, isqrt, log1p
from scipy.fft import fft
from scipy.stats import wasserstein_distance
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from gplearn.genetic import SymbolicRegressor
import optuna 
from optuna import create_study
import shap
import sage.all as sage
from sage.all import *
from sage.parallel.decorate import parallel
from fastdtw import fastdtw  
pari.allocatemem(8_000_000_000)
import warnings


warnings.filterwarnings("ignore")


CHUNKSIZE = 1
ROW_LIMIT = 50
# ----------------------------------------------------------------------
# PARI memory
# ----------------------------------------------------------------------
pari.allocatemem(8_000_000_000)


# ----------------------------------------------------------------------
# 1. Load CSV
# ----------------------------------------------------------------------
def load_csv(path: str, n_samples: int = 50) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV not found: {path}")
    df = pd.read_csv(path, low_memory=False)
    return df.head(n_samples).copy()


# ----------------------------------------------------------------------
# 2. Sequences (8 families) – for comparison only
# ----------------------------------------------------------------------
def generate_sequences(n: int):
    fib = [0, 1]; luc = [2, 1]; pell = [0, 1]; cat = [1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796]
    ppow = [2**i for i in range(n)]
    tri  = [i*(i+1)//2 for i in range(n)]
