from sage.all import EllipticCurve, QQ, factor, RealField, prod
from sage.schemes.elliptic_curves.sha_tate import Sha
import random
import numpy as np
from sklearn.linear_model import LogisticRegression
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# Cosmological constants
KAPPA = 1000 # Scaling factor for radius of curvature
SQRT_KAPPA = math.sqrt(KAPPA) # ≈ 31.6, for density height scaling
VIRGO_DISTANCE = 54e6 # Light-years to Virgo Cluster
VIRGO_COMOVING_VOLUME = 1e9 # Mly^3
LIGHT_TRAVEL_MARS = 4.33 / 60 / 24 / 365.25 # 4.33 minutes to years
def generate_fibonacci(n):
