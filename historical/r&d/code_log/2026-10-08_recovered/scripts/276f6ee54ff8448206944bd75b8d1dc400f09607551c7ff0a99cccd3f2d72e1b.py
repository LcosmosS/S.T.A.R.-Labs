"""
Top‑level package initializer for the S.T.A.R. model.
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
