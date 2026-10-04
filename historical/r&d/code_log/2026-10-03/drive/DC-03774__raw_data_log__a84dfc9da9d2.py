import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
import matplotlib.pyplot as plt


CALIBRATED_FILE = "synthetic_cosmos_final/synthetic_cosmic_catalog_calibrated.csv"
REAL_FILE1 = "JApJ94494_2MASS_GAIADR3_EPOCH.csv"


print("🔄 Loading calibrated synthetic data...")
synth = pd.read_csv(CALIBRATED_FILE)


# Load real data (chunked)
real1 = pd.concat([chunk for chunk in pd.read_csv(REAL_FILE1, chunksize=50000, low_memory=False)], ignore_index=True)


print(f"Loaded calibrated synthetic: {len(synth):,} galaxies")
print(f"Loaded real1 (JApJ): {len(real1):,} rows")


# KS-test (fixed with plain int)
sample_size = 5000
ks_before = ks_2samp(
    synth['V_comove'].sample(int(sample_size), random_state=int(42)),
    real1['DM'].dropna().sample(int(sample_size), random_state=int(42)) * 100
