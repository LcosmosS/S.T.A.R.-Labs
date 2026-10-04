"""
Paper Figures Pipeline
======================

Automatically generates all figures needed for a cosmology paper:
- Hubble diagram
- H(z) comparison
- Distance modulus comparison
- Residuals
- Corner plot
- Parameter constraints table
"""

from __future__ import annotations
import os
import pandas as pd
import numpy as np
import corner

from src.physics.cosmology import Cosmology
from src.physics.symbolic_cosmology import SymbolicCosmology
from src.visualization.paper_figures import (
    plot_hubble_diagram, plot_Hz, plot_residuals
)


class PaperFiguresPipeline:
    """
    Unified, validated pipeline for generating paper-ready figures.
    """

    REQUIRED_KEYS = {"planck", "bao", "cc"}

    def __init__(self, chain, param_names, H_expr, data_paths):
        self.chain = chain
        self.param_names = param_names
        self.H_expr = H_expr
        self.data_paths = data_paths

        self._validate_inputs()

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------
    def _validate_inputs(self):
        # Validate required keys
        missing = self.REQUIRED_KEYS - set(self.data_paths.keys())
        if missing:
            raise ValueError(
                f"data_paths missing required keys: {missing}. "
                f"Expected keys: {self.REQUIRED_KEYS}"
            )

        # Validate each dataset
        for key, value in self.data_paths.items():
            if isinstance(value, str):
                raise TypeError(
                    f"data_paths['{key}'] is a string ('{value}'). "
                    f"Expected an embedded dataset dict, not a filename. "
                    f"Pass the actual dataset object, e.g. data_paths['planck'] = PLANCK_2015"
                )
            if not isinstance(value, dict):
                raise TypeError(
                    f"data_paths['{key}'] must be a dict, got {type(value)}"
                )

    # ---------------------------------------------------------
    # Model builders
    # ---------------------------------------------------------
    def best_fit_model(self):
        params = dict(zip(self.param_names, self.chain.mean(axis=0)))
        return SymbolicCosmology(self.H_expr, params)

    def lcdm_model(self):
        return Cosmology(
            "H0*sqrt(Ωm*(1+z)**3 + ΩΛ)",
            {"H0": 67.4, "Ωm": 0.315, "ΩΛ": 0.685}
        )

    # ---------------------------------------------------------
    # Main pipeline
    # ---------------------------------------------------------
    def run(self, output_dir="paper_figures"):
        os.makedirs(output_dir, exist_ok=True)

        # Convert embedded dict → DataFrame
        df_sn = pd.DataFrame(self.data_paths["sn"])

        # Build models
        star = self.best_fit_model()
        lcdm = self.lcdm_model()

        # Generate figures
        plot_hubble_diagram(df_sn, lcdm, star)
        plot_Hz([lcdm, star], ["ΛCDM", "S.T.A.R."])
        plot_residuals(df_sn, lcdm, star)

        # Corner plot
        fig = corner.corner(self.chain, labels=self.param_names, show_titles=True)
        fig.savefig(f"{output_dir}/corner_plot.png", dpi=200)

        # Return constraints
        return dict(zip(self.param_names, self.chain.mean(axis=0)))
