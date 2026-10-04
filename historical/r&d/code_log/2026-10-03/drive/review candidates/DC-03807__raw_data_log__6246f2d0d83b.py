import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
import matplotlib.pyplot as plt


CALIBRATED_FILE = "synthetic_cosmos_final/synthetic_cosmic_catalog_calibrated.csv"
REAL_FILE1 = "JApJ94494_2MASS_GAIADR3_EPOCH.csv"


print("🔄 Loading calibrated synthetic data...")
synth = pd.read_csv(CALIBRATED_FILE)


# Load real data (chunked)
