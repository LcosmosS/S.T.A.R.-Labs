import yaml

from src.likelihoods.data.planck_2015 import PLANCK_2015
from src.likelihoods.data.planck_2018_recon import PLANCK_2018_RECON
from src.likelihoods.data.desi_bao_dr1 import DESI_BAO_DR1
from src.likelihoods.data.cosmic_chronometers import COSMIC_CHRONOMETERS

from src.likelihoods.planck_shoes_joint import PlanckSH0ESJointLikelihood
from src.likelihoods.desi_bao import DESIBAO
from src.likelihoods.cosmic_chronometers import CosmicChronometers
from src.likelihoods.joint_likelihood import JointLikelihood

from src.physics.mcmc_joint_pipeline import JointMCMCPipeline
from src.pipeline.paper_figures_pipeline import PaperFiguresPipeline
from src.likelihoods.data.pantheon_plus_full import PANTHEON_PLUS_FULL
from src.likelihoods.pantheon_plus import PantheonPlusLikelihood

DATASET_REGISTRY = {
    "PLANCK_2015": PLANCK_2015,
    "PLANCK_2018_RECON": PLANCK_2018_RECON,
    "DESI_BAO_DR1": DESI_BAO_DR1,
    "COSMIC_CHRONOMETERS": COSMIC_CHRONOMETERS,
    "PANTHEON_PLUS_FULL": PANTHEON_PLUS_FULL
}

def load_dataset(name):
    if name not in DATASET_REGISTRY:
        raise KeyError(f"Unknown dataset '{name}'. Available: {list(DATASET_REGISTRY.keys())}")
    return DATASET_REGISTRY[name]

def build_joint_likelihood(config):
    planck = load_dataset(config["datasets"]["planck"])
    bao = load_dataset(config["datasets"]["bao"])
    cc = load_dataset(config["datasets"]["cc"])
    sn = load_dataset(config["datasets"]["sn"])

    planck_like = PlanckSH0ESJointLikelihood(planck)
    bao_like = DESIBAO(bao)
    cc_like = CosmicChronometers(cc)
    sn_like = PantheonPlusLikelihood(sn)

    return JointLikelihood(planck_like, bao_like, cc_like, sn_like)

def run_full_inference(config_path):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Load datasets
    planck = load_dataset(config["datasets"]["planck"])
    bao = load_dataset(config["datasets"]["bao"])
    cc = load_dataset(config["datasets"]["cc"])

    # Build likelihood
    joint = build_joint_likelihood(planck)

    # Run MCMC
    mcmc = JointMCMCPipeline(
        config["model"]["H_expr"],
        config["model"]["param_names"],
        config["priors"],
        config["proposal_widths"],
        joint
    )

    chain = mcmc.run(
        theta0=config["mcmc"]["theta0"],
        nsteps=config["mcmc"]["nsteps"]
    )

    # Generate figures
    fig = PaperFiguresPipeline(
        chain,
        config["model"]["param_names"],
        config["model"]["H_expr"],
        data_paths={"planck": planck, "bao": bao, "cc": cc}
    )

    constraints = fig.run(config["output_dir"])
    return constraints
