"""
MCMC Cosmology Fitter
=====================

Runs Metropolis–Hastings MCMC to infer posterior distributions for
S.T.A.R. Model parameters.
"""

from __future__ import annotations
import numpy as np
from src.physics.symbolic_cosmology import SymbolicCosmology


class MCMCCosmologyFitter:
    def __init__(self, H_expr, param_names, priors, proposal_widths):
        """
        priors : dict[param] = (mean, sigma)
        proposal_widths : dict[param] = step size
        """
        self.H_expr = H_expr
        self.param_names = param_names
        self.priors = priors
        self.proposal_widths = proposal_widths

    def _log_prior(self, theta):
        lp = 0
        for val, name in zip(theta, self.param_names):
            mu, sigma = self.priors[name]
            lp += -0.5 * ((val - mu) / sigma)**2
        return lp

    def _log_likelihood(self, theta, z, mu_obs, sigma_mu):
        params = dict(zip(self.param_names, theta))
        model = SymbolicCosmology(self.H_expr, params)
        mu_model = np.array([model.distance_modulus(zi) for zi in z])
        chi2 = np.sum(((mu_obs - mu_model) / sigma_mu)**2)
        return -0.5 * chi2

    def _log_posterior(self, theta, z, mu_obs, sigma_mu):
        return self._log_prior(theta) + self._log_likelihood(theta, z, mu_obs, sigma_mu)

    def run(self, z, mu_obs, sigma_mu, theta0, nsteps=5000):
        chain = np.zeros((nsteps, len(theta0)))
        chain[0] = theta0
        logp = self._log_posterior(theta0, z, mu_obs, sigma_mu)

        for i in range(1, nsteps):
            proposal = chain[i-1] + np.array([
                np.random.normal(0, self.proposal_widths[name])
                for name in self.param_names
            ])

            logp_new = self._log_posterior(proposal, z, mu_obs, sigma_mu)
            accept = np.random.rand() < np.exp(logp_new - logp)

            if accept:
                chain[i] = proposal
                logp = logp_new
            else:
                chain[i] = chain[i-1]

        return chain
