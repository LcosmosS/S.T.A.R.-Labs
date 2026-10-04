from sage.all import EllipticCurve, QQ, factor, RealField, prod
from sage.schemes.elliptic_curves.sha_tate import Sha
import random
import numpy as np
from sklearn.linear_model import LogisticRegression
import math


def generate_fibonacci(n):
    """Generate Fibonacci numbers up to index n."""
    fib = [0, 1]
    if n < 2:
        return fib[:n+1]
    for i in range(2, n+1):
        fib.append(fib[i-1] + fib[i-2])
    return fib


def random_fibonacci_pair(n, classifier=None, fib_list=None, X_data=None):
    """Select a random Fibonacci pair, biased by classifier or heuristic."""
    if fib_list is None:
        fib_list = generate_fibonacci(n)
