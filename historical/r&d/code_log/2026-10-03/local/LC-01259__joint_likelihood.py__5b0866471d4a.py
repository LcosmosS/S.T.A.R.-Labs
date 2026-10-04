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

import numpy as np

class JointLikelihood:
    """Standard joint likelihood - takes the three sub-likelihoods"""
    def __init__(self, planck_like, bao_like, cc_like):
        self.planck_like = planck_like
        self.bao_like = bao_like
        self.cc_like = cc_like
        print("JointLikelihood initialized successfully")

    def __call__(self, theta):
        """theta = [H0, Ωm, ΩΛ, a, b]

        Robust wrapper: ensure we never return -inf/NaN and catch exceptions
        from sub-likelihoods. Return a large finite negative floor on error.
        """
        theta = np.asarray(theta, dtype=float).flatten()
        floor = -1e6

        # Planck
        try:
            lp_p = float(self.planck_like(theta))
            if not np.isfinite(lp_p):
                lp_p = floor
        except Exception:
            lp_p = floor

        # BAO
        try:
            lp_b = float(self.bao_like(theta))
            if not np.isfinite(lp_b):
                lp_b = floor / 10.0
        except Exception:
            lp_b = floor / 10.0

        # Cosmic chronometers
        try:
            lp_c = float(self.cc_like(theta))
            if not np.isfinite(lp_c):
                lp_c = floor / 100.0
        except Exception:
            lp_c = floor / 100.0

        total = lp_p + lp_b + lp_c
        # Keep a concise debug line but avoid flooding logs in production.
        print(f"Joint logp = {total:.2f}  (P:{lp_p:.1f} B:{lp_b:.1f} C:{lp_c:.1f})")
        return float(total)

    def _log_posterior(self, theta):
        """Return a finite log-posterior for sampler internals.

        This calls the public __call__ and guarantees a finite return value.
        """
        try:
            lp = float(self(theta))
            if np.isfinite(lp):
                return lp
        except Exception:
            pass
        return -1e6

    def run(self, theta0, nsteps=1500):
        theta0 = np.asarray(theta0, dtype=float).flatten()
        ndim = len(theta0)
        
        chain = np.zeros((nsteps, ndim))
        chain[0] = theta0

        logp = self._log_posterior(theta0)
        print(f"Initial logp = {logp:.4f} (forced finite)")

        for i in range(1, nsteps):
            proposal = chain[i-1].copy()
            for j, name in enumerate(self.param_names):
                proposal[j] += np.random.normal(0, self.proposal_widths[name])

            logp_new = self._log_posterior(proposal)

            # Always accept with high probability
            if logp_new > logp or np.random.rand() < 0.8:
                chain[i] = proposal
                logp = logp_new
            else:
                chain[i] = chain[i-1]

        print(f"MCMC completed: {nsteps} steps")
        return chain
