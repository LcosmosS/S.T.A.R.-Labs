import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)



from sage.all import EllipticCurve, QQ, factor, RealField, prod, pari, heegner_points, Integer, RealNumber

import numpy as np

import math

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.linear_model import LogisticRegression

from sklearn.preprocessing import StandardScaler



# Cosmological constants

KAPPA = 1000

SQRT_KAPPA = math.sqrt(KAPPA)

VIRGO_DISTANCE = 54e6

VIRGO_COMOVING_VOLUME = 1e9

DENSITY_HEIGHT_TARGET = 6320



# Golden ratio

PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.618033988749895

print(f"Golden ratio (φ): {PHI}")



# Initial interweb_data (from previous runs)

interweb_data = [

    (13, 377, 0, 1.5248784246208363956283412258 / 10, 1.5248784246208363956283412258, 1.0, 1,
True, math.log(61540336), math.log(61540336)),

    (2, 144, 3, 35.620854002542971603630883958 / 10, 1.8236602565125279190648710531,
9.76630758808727, 2, True, math.log(8958464), math.log(4479232)),

    (144, 233, 1, 14.397681380538820045587978770 / 10, 1.1093071817654113436605273746,
2.16316418289501, 6, True, math.log(214555824), math.log(17879652)),

    (34, 144, 2, 12.623558290853645758994107725 / 10, 1.5874476029557543327015819683,
3.97605510485800, 2, True, math.log(11473408), math.log(5736704)),