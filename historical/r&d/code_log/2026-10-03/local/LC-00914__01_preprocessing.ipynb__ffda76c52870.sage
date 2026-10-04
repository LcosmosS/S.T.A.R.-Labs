# Reproducibility and environment
import sys, os
REPO_ROOT = os.getcwd()   # assumes notebook is in repo root; adjust if not
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
print("Inserted REPO_ROOT to sys.path:", REPO_ROOT)
print("sys.path[0]:", sys.path[0])

import json
import platform
import numpy as np
import pandas as pd


REPO_ROOT = os.path.abspath("..")  # adjust if notebook lives elsewhere

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
print("sys.path[0] set to:", sys.path[0])

SEED = 42
np.random.seed(SEED)

# Record versions for reproducibility
env = {
    "python": platform.python_version(),
    "numpy": np.__version__,
    "pandas": pd.__version__,
}
print("Environment:", json.dumps(env, indent=2))
