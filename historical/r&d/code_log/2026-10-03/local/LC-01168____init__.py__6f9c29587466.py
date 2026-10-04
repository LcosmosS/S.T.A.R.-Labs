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
from src.data.load_sky_surveys import load_sky_surveys

def test_sky_surveys_load():
    df1, df2 = load_sky_surveys(downsample=100, validate_schema=True)
    assert len(df1) > 0
    assert len(df2) > 0

__all__ = [
    "project",
    "QuantileAligner",
    "compute_persistence",
    "w2_between_diagrams",
    "empirical_p_value",
]

