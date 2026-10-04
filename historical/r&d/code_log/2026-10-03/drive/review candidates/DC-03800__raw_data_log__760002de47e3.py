import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp
from pathlib import Path


SYNTHETIC_FILE = "synthetic_cosmos_final/synthetic_cosmic_catalog_final.csv"
REAL_FILE1 = "JApJ94494_2MASS_GAIADR3_EPOCH.csv"
REAL_FILE2 = "DESIDR8_SDSSDR16_SIMBAD.csv"


CHUNK_SIZE = 50000


print("🔄 Loading synthetic catalog...")
synth = pd.read_csv(SYNTHETIC_FILE)
print(f"   Synthetic galaxies: {len(synth):,} | Ranks: {sorted(synth['exact_rank'].unique())}")


print("\n🔄 Loading real files (chunked)...")
