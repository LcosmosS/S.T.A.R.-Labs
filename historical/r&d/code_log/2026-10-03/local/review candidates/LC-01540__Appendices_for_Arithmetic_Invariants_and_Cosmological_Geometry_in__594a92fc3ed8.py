import requests
import pandas as pd
import time
import re
from sage.all import EllipticCurve, QQ

# ==============================================================================
# SECTION 1: CORE UCF PARAMETERS AND EXPANDED CLUSTER DATA
# ==============================================================================

# This KAPPA constant is the unified, data-driven value from your paper
# "Deciphering the Cosmic Grammar". It is the key to generating new curves.
DATA_DRIVEN_KAPPA = 31.5926

def get_expanded_cluster_data():
    """
    Provides physical parameters for a curated list of major cosmological structures,
