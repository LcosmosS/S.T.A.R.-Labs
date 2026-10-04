"""Joint cosmology likelihood with explicit non-finite rejection."""

from __future__ import annotations

import numpy as np


class JointLikelihood:
    """Combine Planck+SH0ES, DESI BAO, and cosmic-chronometer likelihoods."""

    def __init__(self, planck_like, bao_like, cc_like):
        self.planck_like = planck_like
        self.bao_like = bao_like
        self.cc_like = cc_like

    def __call__(self, model):
        components = (
            float(self.planck_like.log_likelihood(model)),
            float(self.bao_like.log_likelihood(model)),
            float(self.cc_like.log_likelihood(model)),
        )
        if not np.all(np.isfinite(components)):
            return -np.inf
        return float(sum(components))
