from sage.all import EllipticCurve, QQ, factor, RealField, prod
import random
import numpy as np
from sklearn.linear_model import LogisticRegression
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Cosmological constants
KAPPA = 1000  # Radius of curvature scaling
SQRT_KAPPA = math.sqrt(KAPPA)  # ≈ 31.6
COSMO_SCALE = 1e6  # Additional scale to reach 54 Mly
VIRGO_DISTANCE = 54e6  # Light-years
VIRGO_COMOVING_VOLUME = 1e9  # Mly^3

def generate_fibonacci(n):
    """Generate Fibonacci numbers up to index n."""
    fib = [0, 1]
    if n < 2:
        return fib[:n+1]
    for i in range(2, n+1):
        fib.append(fib[i-1] + fib[i-2])
    return fib

def random_fibonacci_pair(n, classifier=None, fib_list=None, X_data=None, force_failure=False):
    """Select Fibonacci pair, biased toward rank ≥ 3."""
    if fib_list is None:
        fib_list = generate_fibonacci(n)
    valid_fibs = [f for f in fib_list if f != 0 and f <= 5000]
    large_fibs = [f for f in fib_list if f > 5000 and f <= 10000]
    if len(valid_fibs) < 2:
        return random.choice(fib_list), random.choice(fib_list)
