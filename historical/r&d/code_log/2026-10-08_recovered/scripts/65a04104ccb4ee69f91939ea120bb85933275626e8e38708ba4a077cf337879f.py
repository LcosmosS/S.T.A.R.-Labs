"""
Joint Cosmology Likelihood Engine
=================================

Combines:
- Planck distance priors
- SH0ES H0 measurement
- DESI BAO
- Cosmic chronometers

Returns total log-likelihood for any cosmology model.
"""

from __future__ import annotations

class JointLikelihood:
    def __init__(self, planck_shoes, desi_bao, cc):
        """
        Parameters
        ----------
        planck_shoes : PlanckSH0ESJointLikelihood
        desi_bao : DESIBAO
        cc : CosmicChronometers
        """
        self.planck_shoes = planck_shoes
        self.desi_bao = desi_bao
        self.cc = cc

    def log_likelihood(self, model):
        lp = self.planck_shoes.log_likelihood(model)
        lb = self.desi_bao.log_likelihood(model)
        lc = self.cc.log_likelihood(model)
        return lp + lb + lc
