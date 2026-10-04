import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


from sage.all import EllipticCurve, QQ, factor, RealField, prod, fundamental_discriminant
from sage.arith.misc import kronecker_symbol
import numpy as np
import math
import gc
import csv
from datetime import datetime
import matplotlib.pyplot as plt


# Cosmological constants
KAPPA = 1000
SQRT_KAPPA = math.sqrt(KAPPA)
VIRGO_DISTANCE = 54e6  # light-years


# Golden ratio
PHI = (1 + math.sqrt(5)) / 2


# Fibonacci and Lucas numbers (abbreviated for brevity)
fib_numbers = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368]
lucas_numbers = [2, 1, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199, 322, 521, 843, 1364, 2207, 3571, 5778, 9349, 15127, 24476, 39603, 64079, 103682]


# Training data
training_data = [
    [2, 144, 16.0081093416841, 15.3149621611242, 1],
    [377, 987, 22.0713726262387, 21.3782254456787, 1],
