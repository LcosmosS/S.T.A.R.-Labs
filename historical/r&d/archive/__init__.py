"""
Top‑level package initializer for the S.T.A.R. model.

This file exists so that imports like:
    from src.entropy.entropy_field import EntropyField
    from src.physics.hubble_tension_fit import HubbleTensionFit
    from src.tda.bootstrap_stability import BootstrapStability
    from src.symbolic_regression.sr_pipeline import SRPipeline
    from src.acsc.tda_pipeline import persistence_wasserstein

work correctly inside CI, notebooks, and the container.
"""

# Re-export subpackages for convenience (optional)
from . import entropy
from . import physics
from . import tda
from . import symbolic_regression
from . import acsc

__all__ = [
    "entropy",
    "physics",
    "tda",
    "symbolic_regression",
    "acsc",
]

