# Suppress deprecation warnings for pkg_resources
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from sage.all import EllipticCurve, QQ, factor, RealField, prod, pari
import random
import numpy as np
from sklearn.linear_model import LogisticRegression
import math