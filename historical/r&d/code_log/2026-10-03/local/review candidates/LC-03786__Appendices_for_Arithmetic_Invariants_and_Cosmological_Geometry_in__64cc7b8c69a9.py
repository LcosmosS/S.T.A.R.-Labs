from xgboost import XGBRegressor  # XGBoost

import plotly.graph_objects as go

import matplotlib.pyplot as plt

import seaborn as sns

import os

from matplotlib import cm



os.makedirs("visualizations", exist_ok=True)

chunksize = 10000  # Process in chunks for large CSV



# Function to process chunk

def process_chunk(chunk):
