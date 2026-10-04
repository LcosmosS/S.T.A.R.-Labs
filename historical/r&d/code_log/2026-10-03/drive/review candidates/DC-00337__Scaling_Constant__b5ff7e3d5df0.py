import numpy as np
import pandas as pd
from sage.all import EllipticCurve, QQ


# ==============================================================================
# SECTION 1: FOUNDATIONAL UCF & PHYSICAL DATA
# ==============================================================================


DATA_DRIVEN_KAPPA = 31.5926


def get_galaxy_virial_data():
    """
    Provides curated data for galaxies with known virial properties from accredited
