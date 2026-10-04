# === Pre-registered parameters (edit before running experiments) ===
Amax = 1e12
Nmax = 1e6
V0 = 1.0
TOP_SCALE = 25.0  # Mpc, Topological Locked Scale (for later)
N_QUANTILES = 200

# File paths (edit to match your repo/data layout)
ARITH_CREMONA = "acsc_validation_cremona.csv"
ARITH_LMFDB = "acsc_validation_lmfdb.csv"
COSMIC_FILE = "cosmic_volume_sample.csv"  # path to your cosmic point cloud (comoving coords)
OUT_DIR = "derived"
os.makedirs(OUT_DIR, exist_ok=True)
