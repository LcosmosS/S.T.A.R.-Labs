#!/bin/bash

"""
ACSC: Arithmetic–Cosmic Structure Conjecture computational framework.

A reproducible pipeline for testing the correspondence between topological features
of elliptic-curve arithmetic clouds and cosmic structure.
"""

__version__ = "0.1.0"
__author__ = "Patrick J. McNamara"

# Core exports for convenient access
from .projection import project
from .quantile import QuantileAligner
from .tda_pipeline import compute_persistence
from .statistics import w2_between_diagrams, empirical_p_value

__all__ = [
    "project",
    "QuantileAligner",
    "compute_persistence",
    "w2_between_diagrams",
    "empirical_p_value",
]

