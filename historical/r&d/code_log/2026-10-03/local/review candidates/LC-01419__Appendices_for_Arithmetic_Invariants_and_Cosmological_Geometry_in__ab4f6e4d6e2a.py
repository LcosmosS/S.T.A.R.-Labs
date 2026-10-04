from sage.all import EllipticCurve, QQ, RealField
import random
import numpy as np
import math
import matplotlib.pyplot as plt
from tqdm import tqdm

# --- Cosmological Constants ---
KAPPA = 1000.0
SQRT_KAPPA = math.sqrt(KAPPA)
VIRGO_DISTANCE = 5.4e7  # 54 million light-years
