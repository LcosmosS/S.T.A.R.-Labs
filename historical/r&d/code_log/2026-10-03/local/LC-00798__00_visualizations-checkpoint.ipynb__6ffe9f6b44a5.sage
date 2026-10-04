import sys, os
sys.path.append('src')
sys.path.append('../src')
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import plotly.express as px
import plotly.graph_objects as go

os.makedirs('figures', exist_ok=True)

from src.data.load_sky_surveys import load_sky_surveys

sky_2mass_gaia, sky_sdss_desi_simbad = load_sky_surveys()

