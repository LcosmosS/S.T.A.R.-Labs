# Import necessary libraries from the environment
import requests
import numpy as np
import math
from astropy.coordinates import SkyCoord
import astropy.units as u
from astroquery.sdss import SDSS  # Assuming astroquery is available; if not, install via conda-forge
from gudhi import AlphaComplex  # Assuming gudhi is available; if not, install via conda-forge
from gudhi.wasserstein import wasserstein_distance
import pandas as pd
from sage.all import EllipticCurve, fibonacci, QQ, floor  # Import from SageMath
from sage.combinat.combinat import lucas_number1, lucas_number2


# Step 1: Generate elliptic curves using recursive sequences (Fibonacci, Lucas) with SageMath
def generate_elliptic_curves(max_n=50, scalars=[1, -1]):
    phi = (1 + QQ(5).sqrt()) / 2
    curves = []
    for n in range(1, max_n + 1):
        seqs = [
            fibonacci(n),  # Fibonacci
            lucas_number2(n, 1, -1),  # Lucas (standard sequence with P=1, Q=-1)
            floor(phi * n)  # Golden ratio approximation
        ]
        for a_base in seqs:
            for b_base in seqs:
                for scalar_a in scalars:
                    for scalar_b in scalars:
                        a = scalar_a * a_base
                        b = scalar_b * b_base
                        try:
                            E = EllipticCurve(QQ, [0, 0, 0, a, b])
                            disc = E.discriminant()
                            if disc != 0:
                                N = E.conductor()
                                abs_disc = abs(disc)
                                r = E.rank(only_bounds=True)[0]  # Use bounds for faster computation; full rank may be slow
                                curves.append({'label': f'E_{a}_{b}', 'N': N, 'Delta': abs_disc, 'r': r})
                        except Exception as e:
                            pass  # Skip singular or invalid curves
    # Deduplicate by discriminant or conductor if needed
    unique_curves = {c['Delta']: c for c in curves}.values()
    return list(unique_curves)


# Step 2: Project curves to 3D coordinates (phi, theta, z)
def project_curves(curves, alpha=200):
    deltas = [c['Delta'] for c in curves if c['Delta'] > 0]
    ns = [c['N'] for c in curves]
