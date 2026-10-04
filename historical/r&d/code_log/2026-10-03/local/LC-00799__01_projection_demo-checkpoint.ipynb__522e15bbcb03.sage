import sys, os, platform
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
import re#

sys.path.append("src")
sys.path.append("../src")

np.random.seed(42)

print("Python:", platform.python_version())
print("NumPy:", np.__version__, "Pandas:", pd.__version__)

os.makedirs("results", exist_ok=True)