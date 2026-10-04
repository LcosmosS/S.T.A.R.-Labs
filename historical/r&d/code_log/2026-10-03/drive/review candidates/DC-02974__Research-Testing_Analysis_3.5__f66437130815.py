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
    """Generate Fibonacci numbers up to index n."""
    fib = [0, 1]
    if n < 2:
        return fib[:n+1]
    for i in range(2, n+1):
        fib.append(fib[i-1] + fib[i-2])
    return fib


def random_fibonacci_pair(n, classifier=None, fib_list=None, X_data=None, force_failure=False, seen_pairs=None):
    """Select Fibonacci pair, heavily biased toward rank ≥ 3, no repetition."""
    if fib_list is None:
        fib_list = generate_fibonacci(n)
