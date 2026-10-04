import numpy as np
import pandas as pd
from scipy.stats import wasserstein_distance
from sklearn.neighbors import NearestNeighbors


class ArithmeticSeed:
    """Equivalent to a 'Spacecraft' in GMAT. Defines the source arithmetic DNA."""
    def __init__(self, label, rank, regulator, conductor):
        self.label = label
        self.rank = rank
        self.regulator = regulator
        self.conductor = conductor
        self.invariants = np.array([rank, regulator, np.log10(conductor)])


class ProjectionEngine:
    """Equivalent to 'ForceModel'. Defines the constants of the projection Φ."""
    def __init__(self):
        # Physics constants derived from PySR and ACSC
        self.ALPHA = np.sqrt(1.5)  # The Curvature Anchor
        self.BETA = 16.263         # The Hubble-Time Scaling
        self.GAMMA = 1.0           # Entropy gradient coefficient


    def apply(self, seed, t_cosmo):
        """The core ACSC mapping function Φ(E) -> (x, y, z)"""
        # Symbolic dynamics: Tully-Fisher proxy driven by rank and regulator
        tf_proxy = (seed.rank * self.ALPHA) + np.log(seed.regulator + 1.1)
        
        # The Unfolding Equation (derived from PySR)
        # y ≈ ((T_cosmo * Tully_Fisher) + 1.2209) - (T_cosmo * 16.263)
        z_projected = ((t_cosmo * tf_proxy) + self.ALPHA) - (t_cosmo * self.BETA)
        
        # Angular unfolding using conductor as a phase proxy
        theta = np.mod(np.log10(seed.conductor) * 2 * np.pi, 2 * np.pi)
        phi = np.mod(seed.regulator * np.pi, np.pi)
        
        r = np.abs(z_projected) * 1000 # Scaling to Mpc
        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = r * np.cos(phi)
        
        return np.array([x, y, z])


class MissionControl:
    """The SMAT Orchestrator. Runs 'Missions' to align seeds with real observations."""
    def __init__(self):
        self.engine = ProjectionEngine()
        self.seeds = []
        self.target_manifold = None


    def load_target_catalog(self, filepath):
        """Loads the Real-World (Manifold) data for alignment."""
        self.target_manifold = pd.read_csv(filepath)
        print(f"📡 Target Manifold Loaded: {len(self.target_manifold)} cosmic signatures.")


    def add_seeds(self, seed_df):
        """Adds ArithmeticSeeds to the mission queue."""
        for _, row in seed_df.iterrows():
            s = ArithmeticSeed(row['cremona_label'], row['exact_rank'], row['regulator'], row['conductor'])
            self.seeds.append(s)


    def run_projection_mission(self, redshift_slice=0.1):
