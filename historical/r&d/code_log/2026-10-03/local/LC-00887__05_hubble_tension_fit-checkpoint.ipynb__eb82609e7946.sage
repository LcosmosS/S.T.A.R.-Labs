import sys, os
sys.path.append('src')
sys.path.append('../src')
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

import numpy as np, pandas as pd, matplotlib.pyplot as plt, json
np.random.seed(11)

os.makedirs('results', exist_ok=True)

from src.data.load_sky_surveys import load_sky_surveys

sky_2mass_gaia, sky_sdss_desi_simbad = load_sky_surveys()

from src.data.load_sky_surveys import load_sky_surveys

sky_2mass_gaia, sky_sdss_desi_simbad = load_sky_surveys()
