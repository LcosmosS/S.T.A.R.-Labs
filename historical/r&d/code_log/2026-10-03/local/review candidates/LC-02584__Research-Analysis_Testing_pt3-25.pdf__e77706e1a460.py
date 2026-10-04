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

def generate_fibonacci(n):
    """Generate Fibonacci numbers up to index n."""
    fib = [0, 1]
    if n < 2:
        return fib[:n+1]
    for i in range(2, n+1):
        fib.append(fib[i-1] + fib[i-2])
    return fib

def random_fibonacci_pair(n, classifier=None, fib_list=None, X_data=None, force_failure=False):
    """Select Fibonacci pair, heavily biased toward rank ≥ 3."""
    if fib_list is None:
        fib_list = generate_fibonacci(n)
    valid_fibs = [f for f in fib_list if f != 0 and f <= 5000]
    large_fibs = [f for f in fib_list if f > 5000 and f <= 10000]
    if len(valid_fibs) < 2:
        return random.choice(fib_list), random.choice(fib_list)

    if force_failure and large_fibs:
        return random.sample(large_fibs, 2) if len(large_fibs) >= 2 else random.sample(valid_fibs, 2)

    high_rank_pairs = [(2, 144), (2, 233), (2, 377), (5, 144), (34, 144)]  # Include rank 3 variations
    high_rank_fibs = [2, 144, 233, 377, 5, 34, 1]
    if classifier is None or X_data is None or len(X_data) < 10:
        if random.random() < 0.85 and high_rank_pairs:  # Stronger bias
            return random.choice(high_rank_pairs)
        if len(high_rank_fibs) >= 2:
            return random.sample(high_rank_fibs, 2)
        return random.sample(valid_fibs, 2)

    best_score = -float('inf')
    best_pair = None
    attempts = min(50, len(valid_fibs) * (len(valid_fibs) - 1) // 2)
    for _ in range(attempts):