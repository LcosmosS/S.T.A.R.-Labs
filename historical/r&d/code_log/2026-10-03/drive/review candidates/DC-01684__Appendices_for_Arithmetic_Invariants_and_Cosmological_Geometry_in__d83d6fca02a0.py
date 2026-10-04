from sage.all import *


def cosmic_denominator(n):
    """Predict denominator from coordinate index n (1=x, 2=y)"""
    return 3**(2*n + 2)


def cosmic_numerator_seed(r, rho, n):
    """
    Hypothesized recursive numerator generator
