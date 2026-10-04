"""DESI BAO likelihood with strict dataset validation."""

from __future__ import annotations

import numpy as np
import pandas as pd


class DESIBAO:
    def __init__(self, bao_data, r_d=147.1):
        if isinstance(bao_data, dict):
            self.bao = {
                "z": np.asarray(bao_data["z"], dtype=float),
                "DM_over_rd": np.asarray(bao_data["DM_over_rd"], dtype=float),
                "sigma_DM": np.asarray(bao_data["sigma_DM"], dtype=float),
                "H_rd": np.asarray(bao_data["H_rd"], dtype=float),
                "sigma_H": np.asarray(bao_data["sigma_H"], dtype=float),
            }
        elif isinstance(bao_data, pd.DataFrame):
            self.bao = {
                key: bao_data[key].to_numpy(dtype=float)
                for key in ("z", "DM_over_rd", "sigma_DM", "H_rd", "sigma_H")
            }
        else:
            df = pd.read_csv(bao_data)
            self.bao = {
                key: df[key].to_numpy(dtype=float)
                for key in ("z", "DM_over_rd", "sigma_DM", "H_rd", "sigma_H")
            }

        lengths = {len(values) for values in self.bao.values()}
        if lengths == {0}:
            raise ValueError("DESI BAO dataset is empty")
        if len(lengths) != 1:
            raise ValueError("DESI BAO arrays must have equal lengths")
        if not all(np.all(np.isfinite(values)) for values in self.bao.values()):
            raise ValueError("DESI BAO dataset contains non-finite values")
        if np.any(self.bao["sigma_DM"] <= 0) or np.any(self.bao["sigma_H"] <= 0):
            raise ValueError("DESI BAO uncertainties must be positive")

        self.r_d = float(r_d)
        if not np.isfinite(self.r_d) or self.r_d <= 0:
            raise ValueError("r_d must be finite and positive")

    def log_likelihood(self, model):
        dm_model = np.asarray(model.DM(self.bao["z"]), dtype=float) / self.r_d
        h_model = np.asarray(model.H(self.bao["z"]), dtype=float) * self.r_d
        if dm_model.shape != self.bao["z"].shape or h_model.shape != self.bao["z"].shape:
            raise ValueError("model BAO predictions have incorrect shape")
        if not np.all(np.isfinite(dm_model)) or not np.all(np.isfinite(h_model)):
            return -np.inf

        chi2_dm = np.sum(
            ((self.bao["DM_over_rd"] - dm_model) / self.bao["sigma_DM"]) ** 2
        )
        chi2_h = np.sum(((self.bao["H_rd"] - h_model) / self.bao["sigma_H"]) ** 2)
        chi2 = float(chi2_dm + chi2_h)
        return -0.5 * chi2 if np.isfinite(chi2) else -np.inf

    def __call__(self, model):
        return self.log_likelihood(model)
