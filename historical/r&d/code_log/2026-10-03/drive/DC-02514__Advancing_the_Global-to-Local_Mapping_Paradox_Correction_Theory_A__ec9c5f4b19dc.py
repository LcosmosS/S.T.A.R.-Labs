# Suppress warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


from sage.all import EllipticCurve, QQ, factor, RealField, prod, pari, fundamental_discriminant
from sage.arith.misc import kronecker_symbol
import numpy as np
import math
import gc
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


# Print SageMath version for debugging
import sage
print(f"SageMath version: {sage.version.version}")


# Cosmological constants
KAPPA = 1000
SQRT_KAPPA = math.sqrt(KAPPA)
VIRGO_DISTANCE = 54e6  # light-years
VIRGO_COMOVING_VOLUME = 1e9  # Mly^3
VIRGO_DENSITY_HEIGHT = 6320


# Golden ratio
PHI = (1 + math.sqrt(5)) / 2
print(f"Golden ratio (φ): {PHI}")


# Generate Fibonacci numbers
def generate_fibonacci(n):
    fib = [0, 1]
    for i in range(2, n + 1):
        fib.append(fib[i-1] + fib[i-2])
    return fib


fib_numbers = generate_fibonacci(77)
print(f"Fibonacci numbers up to index 77: {fib_numbers}")


# Generate Lucas numbers
def generate_lucas(n):
    lucas = [2, 1]
    for i in range(2, n + 1):
        lucas.append(lucas[i-1] + lucas[i-2])
    return lucas


lucas_numbers = generate_lucas(77)
print(f"Lucas numbers up to index 77: {lucas_numbers}")


# Training data for classifier
training_data = [
    [2, 144, 16.0081093416841, 15.3149621611242, 1],
    [377, 987, 22.0713726262387, 21.3782254456787, 1],
