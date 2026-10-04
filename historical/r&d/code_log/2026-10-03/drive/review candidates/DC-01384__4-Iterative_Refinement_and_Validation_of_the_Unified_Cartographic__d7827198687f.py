# --- Library Imports ---
from sage.all import EllipticCurve, QQ, factor, RealField, prod
import random
import numpy as np
from sklearn.linear_model import LogisticRegression
import math
import matplotlib.pyplot as plt


# --- Cosmological Constants ---
KAPPA = 1000
SQRT_KAPPA = math.sqrt(KAPPA)
VIRGO_DISTANCE = 5.4e7 # 54 million light-years


def generate_fibonacci(n):
    fib = [0, 1]
    if n < 2: return fib[:n+1]
    for i in range(2, n+1): fib.append(fib[i-1] + fib[i-2])
