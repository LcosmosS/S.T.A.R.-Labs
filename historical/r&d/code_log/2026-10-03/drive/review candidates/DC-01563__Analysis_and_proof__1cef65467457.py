import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from scipy.optimize import minimize, curve_fit
from astropy.cosmology import Planck18 as cosmo
from astropy import units as u
import sympy as sp
from scipy.stats import wasserstein_distance
from scipy.linalg import norm
from networkx import Graph, number_connected_components, cycle_basis
import logging
import time
from datetime import datetime
import multiprocessing as mp


# Setup logging to file
logging.basicConfig(filename='ucf_test.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('UCF_Tester_v4')


# Constants
PHI = (1 + np.sqrt(5)) / 2
DELTA_MAX = 1e12
N_MAX = 1e6
ALPHA = PHI
LAMBDA = 1.0
CHUNK_SIZE = 100
SAMPLE_CURVES = 1000  # Adjusted for stability
INPUT_FILE = 'GalSpecExtra.csv'
PLOT_PREFIX = 'ucf_test_v4'


# Load and impute large CSV in chunks (parallel)
def process_chunk(chunk):
    chunk.replace(-9999, np.nan, inplace=True)
    imputer = KNNImputer(n_neighbors=5)
    imputable_cols = ['logmass', 'petrorad_r', 'ellipticity', 'sfr', 'metallicity']
    chunk[imputable_cols] = imputer.fit_transform(chunk[imputable_cols])
    chunk['comoving_distance_mpc'] = chunk['z'].apply(lambda z: cosmo.comoving_distance(z).to(u.Mpc).value if z > 0 else 0.0)
    return chunk


def load_and_impute_large_csv(file_path):
    chunks = pd.read_csv(file_path, chunksize=CHUNK_SIZE)
    with mp.Pool(mp.cpu_count()) as pool:
        processed_chunks = pool.map(process_chunk, chunks)
    return pd.concat(processed_chunks, ignore_index=True)


# Generate elliptic curves with limited i to avoid large numbers
def fibonacci_lucas(n, use_lucas=False):
    if n < 0:
        return 0
    a, b = (0, 2) if use_lucas else (0, 1)
    for _ in range(n):
        a, b = b, a + b
    return a


def generate_curve(i):
    # Limit i to smaller values
    i = i % 20 + 1  # Cycle to small i
    a = fibonacci_lucas(i) * (-1)**i
    b = fibonacci_lucas(i, use_lucas=True)
    try:
        x, y = sp.symbols('x y')
        eq = y**2 - (x**3 + a * x + b)
        disc = float(-16 * (4 * a**3 + 27 * b**2))
        cond = float(sp.Abs(disc) ** (1/3))
        # Decipher rank (heuristic: bit length / 3 + torsion proxy)
        rank = float(int(abs(disc)).bit_length() // 3 + 1) if disc != 0 else 0.0
        reg = float(np.log(np.abs(disc) + 1))
        tors = 1.0
        omega = 1.0
        gen_type = 'recursive' if i > 1 else 'simple'
        rational_gen = 'rational' if sp.sympify(a).is_rational and sp.sympify(b).is_rational else 'irrational'
        return {
            'i': i, 'a': a, 'b': b, 'discriminant': disc, 'conductor': cond,
            'rank': rank, 'regulator': reg, 'torsion_order': tors, 'real_period': omega,
            'gen_type': gen_type, 'rational_gen': rational_gen
        }
    except Exception as e:
        logger.warning(f"Curve gen failed for i={i}: {e}")
        # Default dict on failure
        return {
            'i': i, 'a': 0, 'b': 0, 'discriminant': 0.0, 'conductor': 1.0,
            'rank': 0.0, 'regulator': 1.0, 'torsion_order': 1.0, 'real_period': 1.0,
            'gen_type': 'simple', 'rational_gen': 'rational'
        }


def generate_elliptic_curves(num_curves):
    curves = [generate_curve(i) for i in range(1, num_curves + 1)]
    return pd.DataFrame(curves)


# Bin by generator type
def bin_by_generator(df_curves):
    if 'gen_type' not in df_curves.columns or 'rational_gen' not in df_curves.columns:
        logger.warning("Missing gen_type or rational_gen columns; defaulting bin.")
        return {'default': len(df_curves)}
    bins = df_curves.groupby(['gen_type', 'rational_gen'])
    bin_summary = {name: len(group) for name, group in bins}
    logger.info(f"Bin summary: {bin_summary}")
    with open('ucf_analysis.txt', 'w') as f:
        f.write(f"Bin summary: {bin_summary}\n")
    return bin_summary


# Projection Φ
def compute_projection(df_curves):
    df = df_curves.copy()
    df['phi'] = np.log(np.abs(df['discriminant']) + 1e-10) / np.log(DELTA_MAX) * 360
    df['theta'] = np.log(np.abs(df['conductor']) + 1e-10) / np.log(N_MAX) * 180
    df['z'] = PHI * df['rank']
    return df


# Align projections with cosmic data
def align_projections(df_cosmo, df_proj):
    df_cosmo_sample = df_cosmo.sample(n=len(df_proj), replace=True).reset_index(drop=True)
    df_proj = df_proj.reset_index(drop=True)
    aligned = []
    for cosmo_row, proj_row in zip(df_cosmo_sample.itertuples(index=False), df_proj.itertuples(index=False)):
        row = dict(proj_row._asdict())
        row['ra'] = cosmo_row.ra
        row['dec'] = cosmo_row.dec
        row['comoving'] = cosmo_row.comoving_distance_mpc
        aligned.append(row)
    return pd.DataFrame(aligned)


# HD 3D Manifold Visualization with +/- axes and MP4 animation
def visualize_hd_manifold(df_proj, duration=45):
    scaler = StandardScaler()
    df_proj[['ra_norm', 'dec_norm', 'comoving_norm']] = scaler.fit_transform(df_proj[['ra', 'dec', 'comoving']])


    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(df_proj['ra_norm'], df_proj['dec_norm'], df_proj['comoving_norm'], c=df_proj['rank'], cmap='viridis')
    ax.set_xlabel('RA (norm, +/-)')
    ax.set_ylabel('DEC (norm, +/-)')
    ax.set_zlabel('Comoving (norm, +/-)')
    ax.set_title('HD 3D Manifold (Binned by Generator Type)')
    cbar = plt.colorbar(scatter)
    cbar.set_label('Rank')
    plt.savefig(f'{PLOT_PREFIX}_manifold.png')
    logger.info("Static manifold PNG saved.")


    frames = int(duration * 2)  # ~2 fps
    def animate(frame):
        ax.view_init(elev=30, azim=frame * (360 / frames))
        return scatter,


    ani = FuncAnimation(fig, animate, frames=frames, interval=500)
    ani.save(f'{PLOT_PREFIX}_animation.mp4', writer='ffmpeg', dpi=100)
    logger.info(f"MP4 animation saved ({duration}s).")


# Main Test
if __name__ == '__main__':
    start_time = time.time()
    logger.info("Starting UCF Test v4")


    # Load and impute large CSV
    df_cosmo = load_and_impute_large_csv(INPUT_FILE)
    logger.info(f"Loaded and imputed {len(df_cosmo)} rows.")


    # Generate curves
    df_curves = generate_elliptic_curves(SAMPLE_CURVES)
    logger.info(f"Generated {len(df_curves)} curves with deciphered ranks.")


    # Bin by generator
    bin_by_generator(df_curves)


    # Compute projection
    df_proj = compute_projection(df_curves)


    # Align with cosmic data
    df_aligned = align_projections(df_cosmo, df_proj)


    # Visualize HD 3D manifold MP4
    visualize_hd_manifold(df_aligned, duration=45)


    logger.info(f"Test complete. Time: {time.time() - start_time:.2f}s")
    with open('ucf_analysis.txt', 'a') as f:
        f.write(f"Test complete. Time: {time.time() - start_time:.2f}s\n")
