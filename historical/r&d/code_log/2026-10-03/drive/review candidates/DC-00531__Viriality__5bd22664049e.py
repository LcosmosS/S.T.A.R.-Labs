import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from astropy import cosmology, units as u, constants as const
from gplearn.genetic import SymbolicRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from math import log10


# Step 1: Define Initial Dataset from Appendix XII + Additions
initial_data = [
