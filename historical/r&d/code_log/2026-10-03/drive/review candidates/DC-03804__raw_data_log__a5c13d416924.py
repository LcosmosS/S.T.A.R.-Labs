import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
import matplotlib.pyplot as plt


SYNTHETIC_FILE = "synthetic_cosmos_final/synthetic_cosmic_catalog_final.csv"
REAL_FILE1 = "JApJ94494_2MASS_GAIADR3_EPOCH.csv"      # JApJ
REAL_FILE2 = "DESIDR8_SDSSDR16_SIMBAD.csv"            # DESI/SDSS


CHUNK_SIZE = 50000


# Load synthetic (already done)
synth = pd.read_csv(SYNTHETIC_FILE)
print(f"Loaded synthetic: {len(synth):,} galaxies")


# Load real files (chunked)
