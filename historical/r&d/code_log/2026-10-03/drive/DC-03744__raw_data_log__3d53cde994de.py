import pandas as pd
import numpy as np
from pathlib import Path
from sage.schemes.elliptic_curves.ec_database import elliptic_curves
from sage.all import QQ, time
import random


# ────── CONFIG ──────
NUM_CURVES_PER_RANK = 200          # adjust as needed (safe on 48 GB)
MAX_CONDUCTOR = 100000             # keep low for speed
OUTPUT_DIR = Path("synthetic_cosmos")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_CSV = OUTPUT_DIR / "synthetic_cosmic_catalog.csv"


print("🚀 Starting cosmic simulation from Cremona elliptic curves...")


# Helper: inverse scaling laws (reverse of your thesis f/g functions)
def generate_synthetic_cosmology(E, rank):
