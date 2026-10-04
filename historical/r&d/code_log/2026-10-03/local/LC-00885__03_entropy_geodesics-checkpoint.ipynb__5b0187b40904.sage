import sys, os
sys.path.append('src')
sys.path.append('../src')
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

import numpy as np, pandas as pd, matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

np.random.seed(123)
os.makedirs('results', exist_ok=True)

from src.data.load_sky_surveys import load_sky_surveys

sky_2mass_gaia, sky_sdss_desi_simbad = load_sky_surveys()
