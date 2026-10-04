import numpy as np

class PantheonPlusLikelihood:
    def __init__(self, data):
        self.z = np.array(data["z"])
        self.mu = np.array(data["mu"])
        self.sigma = np.array(data["sigma_mu"])

    def chi2(self, model):
        mu_model = model.mu(self.z)
        return np.sum(((self.mu - mu_model) / self.sigma)**2)
