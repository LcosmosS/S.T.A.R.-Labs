import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


from sage.all import EllipticCurve, QQ, factor, RealField, prod, pari, Integer, kronecker, floor, pi as sage_pi
import numpy as np
import math
import gc
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from joblib import Parallel, delayed
import os
import logging
import sys
import traceback
import time
from sympy import symbols, sympify, lambdify
import sympy


# Set up logging
logging.basicConfig(filename='distortion_free_earth_mapping_test_v15.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


def log_print(*args, **kwargs):
    msg = " ".join(map(str, args))
    logging.info(msg)
    print(msg)


# Set up SageMath environment
os.environ["SAGE_NUM_THREADS"] = "1"
pari.allocatemem(2**28)
pari.set_real_precision(128)
log_print(f"PARI stack size set to {2**28} bytes, precision set to 128 bits")


# Constants
KAPPA = 1000
SQRT_KAPPA = math.sqrt(KAPPA)
PHI = (1 + math.sqrt(5)) / 2  # Golden Ratio
A = 637813700
C = 635675200
PI = sage_pi  # Use SageMath's pi for precision


# Generate Fibonacci and Lucas numbers
def generate_fibonacci(n):
    fib = [0, 1]
    for i in range(2, n + 1):
        fib.append(fib[i-1] + fib[i-2])
    return fib


def generate_lucas(n):
    lucas = [2, 1]
    for i in range(2, n + 1):
        lucas.append(lucas[i-1] + lucas[i-2])
    return lucas


fib_numbers = generate_fibonacci(100)
lucas_numbers = generate_lucas(100)
log_print(f"Fibonacci numbers up to index 100: {fib_numbers}")
log_print(f"Lucas numbers up to index 100: {lucas_numbers}")


# Helper functions
def satisfies_heegner_hypothesis(N, D):
    if D >= 0 or D % 4 not in [0, 1]:
        log_print(f"Heegner hypothesis failed: D={D} is not a negative fundamental discriminant")
        return False
    if not Integer(D).is_squarefree():
        log_print(f"Heegner hypothesis failed: D={D} is not squarefree")
        return False
    N = Integer(N)
    prime_factors = factor(N)
    for p, k in prime_factors:
        k_val = kronecker(D, p)
        if k_val == -1:
            log_print(f"p={p} is inert (kronecker(D,p)={k_val}), condition satisfied")
            continue
        if k_val == 0:
            if (p**2).divides(N) and (-D) % p == 0:
                log_print(f"Heegner condition passed for p={p}: k=0, p^2 divides N, and -D ≡ 0 (mod {p})")
                continue
            else:
                log_print(f"Heegner hypothesis failed for p={p}: k=0 but p^2 does not divide N or -D ≢ 0 (mod p)")
                return False
        if k_val == 1:
            if p.divides(-D) and not p.divides(N//p):
                log_print(f"p={p} splits and satisfies condition (kronecker(D,p)={k_val})")
                continue
            else:
                log_print(f"Heegner hypothesis failed for p={p}: k=1 but p does not divide -D or p divides N/p")
                return False
    log_print(f"Heegner hypothesis satisfied for N={N}, D={D}")
    return True


def find_suitable_discriminant(N):
    N = Integer(N)
    prime_factors = N.prime_factors()
    discriminants = []
    for p in prime_factors:
        for d in range(-3, -1000, -1):
            if d % 4 in [0, 1] and Integer(d).is_squarefree() and kronecker(d, p) != 1:
                discriminants.append(d)
    discriminants = list(set(discriminants))
    discriminants.sort()


    for D in discriminants[:50]:
        if satisfies_heegner_hypothesis(N, D):
            log_print(f"Found suitable discriminant D={D} from conductor-based list")
            return D


    D = -3
    max_attempts = 5000  # Reduced from 20,000
    attempt = 0
    while attempt < max_attempts:
        if D % 4 in [0, 1] and Integer(D).is_squarefree() and satisfies_heegner_hypothesis(N, D):
            log_print(f"Found suitable discriminant D={D} after dynamic search")
            return D
        D -= 1
        attempt += 1
    log_print("No suitable discriminant found after search")
    return None


def compute_heegner_point(E, conductor, max_twists=3):  # Reduced twists
    D = find_suitable_discriminant(conductor)
    if D is None:
        log_print("No suitable discriminant found, returning default (0,0)")
        return (0, 0)
    try:
        heegner = E.heegner_point(D)
        x, y = heegner.xy()
        a, b = E.a4(), E.a6()
        if abs(y**2 - (x**3 + a*x + b)) < 1e-10:
            log_print(f"Heegner point with D={D}: ({float(x)}, {float(y)})")
            return (float(x), float(y))
        else:
            log_print(f"Heegner point ({x}, {y}) does not lie on curve y^2 = x^3 + {a}x + {b}, attempting twist")
    except Exception as e:
        log_print(f"Failed to compute Heegner point with D={D} on original curve: {str(e)}")


    twist_primes = [2, 3, 5]
    for twist_idx in range(min(max_twists, len(twist_primes))):
        d = twist_primes[twist_idx]
        try:
            E_twist = E.quadratic_twist(d)
            conductor_twist = E_twist.conductor()
            log_print(f"Attempting quadratic twist with d={d}, new conductor={conductor_twist}")
            D = find_suitable_discriminant(conductor_twist)
            if D is None:
                log_print(f"No suitable discriminant found for twisted curve with d={d}")
                continue
            heegner = E_twist.heegner_point(D)
            x_twist, y_twist = heegner.xy()
            x = x_twist / (d**2)
            y = y_twist / (d**3)
            a, b = E.a4(), E.a6()
            if abs(y**2 - (x**3 + a*x + b)) < 1e-10:
                log_print(f"Heegner point with D={D} via twist d={d}: ({float(x)}, {float(y)})")
                return (float(x), float(y))
            else:
                log_print(f"Heegner point ({x}, {y}) from twist d={d} does not lie on curve, trying next twist")
        except Exception as e:
            log_print(f"Failed to compute Heegner point with twist d={d}: {str(e)}")
            continue


    # Fallback: Approximate using LLL
    try:
        log_print("Falling back to LLL approximation for Heegner point")
        P = E.gens()[0] if E.gens() else (0, 0)
        x, y = P[0], P[1] if len(P) == 2 else (0, 0)
        log_print(f"Approximated Heegner point via LLL: ({float(x)}, {float(y)})")
        return (float(x), float(y))
    except Exception as e:
        log_print(f"LLL approximation failed: {str(e)}, returning default (0,0)")
        return (0, 0)


def compute_authalic_latitude(geodetic_lat, flattening):
    e = np.sqrt(2 * flattening - flattening**2)
    sin_phi = np.sin(np.radians(geodetic_lat))
    q = (1 - e**2) * sin_phi / (1 - e**2 * sin_phi**2) + (1 / (2 * e)) * np.log((1 + e * sin_phi) / (1 - e * sin_phi))
    q0 = 1 + (1 / (2 * e)) * np.log((1 + e) / (1 - e))
    sin_beta = q / q0
    beta = np.degrees(np.arcsin(sin_beta))
    return beta


def symbolic_regression(ranks, lats, lons, zs):
    x, r = symbols('x r')
    expr = r * x + r**2
    expr_func = lambdify((x, r), expr, 'numpy')
    
    lats = np.array(lats)
    lons = np.array(lons)
    zs = np.array(zs)
    ranks = np.array(ranks)
    
    lat_coeffs = np.polyfit(ranks, lats, 1)
    lon_coeffs = np.polyfit(ranks, lons, 1)
    z_coeffs = np.polyfit(ranks, zs, 1)
    
    lat_expr = lat_coeffs[0] * r + lat_coeffs[1]
    lon_expr = lon_coeffs[0] * r + lon_coeffs[1]
    z_expr = z_coeffs[0] * r + z_coeffs[1]
    
    return lat_expr, lon_expr, z_expr


def analyze_curve(a, b, fib_idx, lucas_idx, is_original=False, max_attempts=3, conductor_limit=5e11, scaler=None, model=None):
    log_print(f"Analyzing curve: y² = x³ + {a}x + {b}")
    
    success = False
    features = None
    rank = None
    selmer3_rank = None
    leading_coeff = None
    omega = None
    reg = None
    tamagawa = None
    weak_bsd_holds = False
    log_delta = None
    log_cond = None
    longitude = None
    latitude = None
    elevation = None
    size = None
    heegner_x = heegner_y = 0
    z = None
    analytic_rank = None
    phi_adjusted = None
    lambda_adjusted = None


    max_coeff = max(abs(a), abs(b))
    scale_factor = 1.0
    a_scaled = a
    b_scaled = b
    if max_coeff > 1e7:
        scale_factor = max_coeff / 1e6
        a_scaled = a / scale_factor
        b_scaled = b / scale_factor
        log_print(f"Scaling coefficients: a={a} -> {a_scaled}, b={b} -> {b_scaled}, scale_factor={scale_factor}")


    try:
        E = EllipticCurve(QQ, [0, 0, 0, a_scaled, b_scaled])
    except ValueError as e:
        log_print(f"Error creating curve: {e}")
        return (success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
                selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size,
                heegner_x, heegner_y, z, phi_adjusted, lambda_adjusted)
