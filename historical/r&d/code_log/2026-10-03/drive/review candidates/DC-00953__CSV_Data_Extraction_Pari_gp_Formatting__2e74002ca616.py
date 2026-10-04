import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import powerlaw  # Install with: pip install powerlaw


# Step 1: Load the dataset
try:
    df = pd.read_csv('galaxy_data.csv')
    print("Dataset loaded successfully.")
