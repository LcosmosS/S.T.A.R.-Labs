"""End-to-end cosmology inference orchestration.

The pipeline validates inputs and fails on incomplete placeholder datasets instead
of manufacturing finite likelihoods.
"""

from __future__ import annotations

import yaml

from src.likelihoods.cosmic_chronometers import CosmicChronometers
from src.likelihoods.data.cosmic_chronometers import COSMIC_CHRONOMETERS
from src.likelihoods.data.desi_bao_dr1 import DESI_BAO_DR1
from src.likelihoods.data.pantheon_plus_full import PANTHEON_PLUS_FULL
from src.likelihoods.data.planck_2015 import PLANCK_2015
from src.likelihoods.data.planck_2018_recon import PLANCK_2018_RECON
from src.likelihoods.desi_bao import DESIBAO
from src.likelihoods.joint_likelihood import JointLikelihood
from src.likelihoods.pantheon_plus import PantheonPlusLikelihood
from src.likelihoods.planck_shoes_joint import PlanckSH0ESJointLikelihood
from src.physics.mcmc_joint_pipeline import JointMCMCPipeline
from src.pipeline.paper_figures_pipeline import PaperFiguresPipeline


DATASET_REGISTRY = {
    "PLANCK_2015": PLANCK_2015,
    "PLANCK_2018_RECON": PLANCK_2018_RECON,
    "DESI_BAO_DR1": DESI_BAO_DR1,
    "COSMIC_CHRONOMETERS": COSMIC_CHRONOMETERS,
    "PANTHEON_PLUS_FULL": PANTHEON_PLUS_FULL,
}


def load_dataset(name):
    if name not in DATASET_REGISTRY:
        raise KeyError(
            f"Unknown dataset '{name}'. Available: {list(DATASET_REGISTRY.keys())}"
        )
    return DATASET_REGISTRY[name]


def _validate_config(config):
    if not isinstance(config, dict):
        raise ValueError("inference config must be a mapping")
    for key in (
        "model",
        "datasets",
        "likelihoods",
        "priors",
        "proposal_widths",
        "mcmc",
        "output_dir",
    ):
        if key not in config:
            raise KeyError(f"inference config missing required section: {key}")
    for key in ("planck", "bao", "cc", "sn"):
        if key not in config["datasets"]:
            raise KeyError(f"inference config missing datasets.{key}")
    for key in ("shoes_H0", "shoes_sigma", "bao_r_d"):
        if key not in config["likelihoods"]:
            raise KeyError(f"inference config missing likelihoods.{key}")
    if float(config["likelihoods"]["shoes_sigma"]) <= 0:
        raise ValueError("likelihoods.shoes_sigma must be positive")
    if float(config["likelihoods"]["bao_r_d"]) <= 0:
        raise ValueError("likelihoods.bao_r_d must be positive")
    if "seed" not in config["mcmc"]:
        raise KeyError("inference config must declare mcmc.seed")


def build_joint_likelihood(config):
    _validate_config(config)

    planck = load_dataset(config["datasets"]["planck"])
    bao = load_dataset(config["datasets"]["bao"])
    cc = load_dataset(config["datasets"]["cc"])
    sn = load_dataset(config["datasets"]["sn"])

    nuisance = config["likelihoods"]
    planck_like = PlanckSH0ESJointLikelihood(
        planck,
        H0_shoes=float(nuisance["shoes_H0"]),
        sigma_shoes=float(nuisance["shoes_sigma"]),
    )
    bao_like = DESIBAO(bao, r_d=float(nuisance["bao_r_d"]))
    cc_like = CosmicChronometers(cc)
    sn_like = PantheonPlusLikelihood(sn)
    return JointLikelihood(planck_like, bao_like, cc_like, sn_like)


def run_full_inference(config_path):
    with open(config_path, "r", encoding="utf-8") as stream:
        config = yaml.safe_load(stream)
    _validate_config(config)

    planck = load_dataset(config["datasets"]["planck"])
    bao = load_dataset(config["datasets"]["bao"])
    cc = load_dataset(config["datasets"]["cc"])
    sn = load_dataset(config["datasets"]["sn"])

    joint = build_joint_likelihood(config)

    mcmc = JointMCMCPipeline(
        config["model"]["H_expr"],
        config["model"]["param_names"],
        config["priors"],
        config["proposal_widths"],
        joint,
        seed=config["mcmc"]["seed"],
        fixed_params=config["model"].get("fixed_params", {}),
    )
    chain = mcmc.run(
        theta0=config["mcmc"]["theta0"],
        nsteps=config["mcmc"]["nsteps"],
    )

    figures = PaperFiguresPipeline(
        chain,
        config["model"]["param_names"],
        config["model"]["H_expr"],
        data_paths={"planck": planck, "bao": bao, "cc": cc, "sn": sn},
    )
    return figures.run(config["output_dir"])
