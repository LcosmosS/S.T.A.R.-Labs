from sage.all import EllipticCurve
from sympy import symbols, Eq, sympify
import numpy as np

# Define precision for numerical computations
R = RealField(100)  # 100-bit precision for L-function and BSD checks

# Define the curves as [a1, a2, a3, a4, a6] for y^2 + a1xy + a3y = x^3 + a2x^2 + a4x + a6
curves = [
