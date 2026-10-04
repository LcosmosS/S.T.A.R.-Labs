import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


synth = pd.read_csv("synthetic_cosmos_final/synthetic_cosmic_catalog_calibrated.csv")
real1 = pd.concat([chunk for chunk in pd.read_csv("JApJ94494_2MASS_GAIADR3_EPOCH.csv", chunksize=20000, low_memory=False)], ignore_index=True)


fig, axs = plt.subplots(1, 3, figsize=(18, 5))


# Plot 1: Scaling law validation
