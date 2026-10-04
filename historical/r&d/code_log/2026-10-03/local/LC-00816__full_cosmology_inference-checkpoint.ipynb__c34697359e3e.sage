# 2. Build likelihoods from embedded data

def build_joint_likelihood(planck_dict):
    planck_like = PlanckSH0ESJointLikelihood(planck_dict)
    bao_like = DESIBAO(DESI_BAO_DR1)
    cc_like = CosmicChronometers(COSMIC_CHRONOMETERS)
    return JointLikelihood(planck_like, bao_like, cc_like)

joint_2015 = build_joint_likelihood(PLANCK_2015)
joint_2018 = build_joint_likelihood(PLANCK_2018_RECON)
