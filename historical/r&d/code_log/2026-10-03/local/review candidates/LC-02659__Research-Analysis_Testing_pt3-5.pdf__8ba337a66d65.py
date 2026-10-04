from sage.all import EllipticCurve, QQ, factor, RealField, prod
import random
import numpy as np
from sklearn.linear_model import LogisticRegression
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Cosmological constants
KAPPA = 1000
SQRT_KAPPA = math.sqrt(KAPPA)  # ≈ 31.6
VIRGO_DISTANCE = 54e6
VIRGO_COMOVING_VOLUME = 1e9
DENSITY_HEIGHT_TARGET = 6320

def generate_fibonacci(n):