# 1. Imports
import sys
import os
from pathlib import Path

def get_project_root():
    if "__file__" not in globals():
        cwd = Path(os.getcwd()).resolve()
        for parent in [cwd] + list(cwd.parents):
            if (parent / "src").exists():
                return parent
        return cwd
    return Path(__file__).resolve().parents[1]

ROOT = get_project_root()
sys.path.insert(0, str(ROOT))
print("Project root added to sys.path:", ROOT)

import numpy as np
import pandas as pd

# Embedded datasets
from src.likelihoods.data.planck_2015 import PLANCK_2015
from src.likelihoods.data.planck_2018_recon import PLANCK_2018_RECON
from src.likelihoods.data.desi_bao_dr1 import DESI_BAO_DR1
from src.likelihoods.data.cosmic_chronometers import COSMIC_CHRONOMETERS
from src.likelihoods.data.pantheon_plus_full import PANTHEON_PLUS_FULL
print("SN count:", len(PANTHEON_PLUS_FULL["z"]))

# Likelihoods
from src.likelihoods.planck_shoes_joint import PlanckSH0ESJointLikelihood
from src.likelihoods.desi_bao import DESIBAO
from src.likelihoods.cosmic_chronometers import CosmicChronometers
from src.likelihoods.joint_likelihood import JointLikelihood
from src.likelihoods.data.pantheon_plus import PANTHEON_PLUS_FULL

# MCMC
from src.physics.mcmc_joint_pipeline import JointMCMCPipeline

# Modernized figure pipeline
from src.pipeline.paper_figures_pipeline import PaperFiguresPipeline
from src.analysis.latex_constraints import constraints_to_latex
