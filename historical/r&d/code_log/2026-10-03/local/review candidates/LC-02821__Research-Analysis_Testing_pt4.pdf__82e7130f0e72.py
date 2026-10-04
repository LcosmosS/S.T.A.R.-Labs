import random
import numpy as np
from sklearn.linear_model import LogisticRegression
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Cosmological constants
KAPPA = 1000
SQRT_KAPPA = math.sqrt(KAPPA)
VIRGO_DISTANCE = 54e6
VIRGO_COMOVING_VOLUME = 1e9
DENSITY_HEIGHT_TARGET = 6320

def generate_fibonacci(n):
    fib = [0, 1]
    for i in range(2, n+1):
        fib.append(fib[i-1] + fib[i-2])
    return fib

def random_fibonacci_pair(n, classifier=None, fib_list=None, X_data=None, force_failure=False,
seen_pairs=None):
    if fib_list is None:
        fib_list = generate_fibonacci(n)
    valid_fibs = [f for f in fib_list if f != 0 and f <= 5000]
    large_fibs = [f for f in fib_list if f > 5000 and f <= 10000]
    seen_pairs = seen_pairs or {}

    if force_failure and large_fibs:
        # Select largest Fibonacci numbers to increase likelihood of conductor exceeding limit
        pair = random.sample(large_fibs, 2) if len(large_fibs) >= 2 else random.sample(valid_fibs, 2)
        if seen_pairs.get(tuple(pair), 0) < 1:
            return pair
        return random.sample(valid_fibs, 2)

    high_rank_pairs = [(2, 144), (233, 377), (144, 233), (89, 233), (34, 144), (21, 377), (5, 144), (3, 144),
