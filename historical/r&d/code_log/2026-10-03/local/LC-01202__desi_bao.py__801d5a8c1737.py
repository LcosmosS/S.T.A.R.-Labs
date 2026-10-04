"""
DESI BAO Likelihood
===================

Implements Gaussian likelihood for DESI BAO measurements:
- D_M(z) / r_d
- H(z) * r_d
"""

from __future__ import annotations
import numpy as np
import pandas as pd


class DESIBAO:
    def __init__(self, bao_data, r_d=147.1):
        """
        bao_data can be:
        - a dict (embedded data module)
        - a CSV file path (legacy mode)
        """
        if isinstance(bao_data, dict):
            self.bao = bao_data
        else:
            df = pd.read_csv(bao_data)
            self.bao = {
                "z": df["z"].tolist(),
                "DM_over_rd": df["DM_over_rd"].tolist(),
                "sigma_DM": df["sigma_DM"].tolist(),
                "H_rd": df["H_rd"].tolist(),
                "sigma_H": df["sigma_H"].tolist(),
            }

        self.r_d = r_d

    def log_likelihood(self, model):
        chi2 = 0.0

        # Embedded dict mode
        if isinstance(self.bao, dict):
            z_list = self.bao["z"]
            DM_over_rd_list = self.bao["DM_over_rd"]
            sigma_DM_list = self.bao["sigma_DM"]
            H_rd_list = self.bao["H_rd"]
            sigma_H_list = self.bao["sigma_H"]

            for z, DM_obs, sDM, H_obs, sH in zip(
                z_list, DM_over_rd_list, sigma_DM_list, H_rd_list, sigma_H_list
            ):
                DM_model = model.DM(z) / self.r_d
                H_model = model.H(z) * self.r_d

                chi2 += ((DM_obs - DM_model) / sDM) ** 2
                chi2 += ((H_obs - H_model) / sH) ** 2

            return -0.5 * chi2

        # Legacy CSV mode (DataFrame)
        for _, row in self.bao.iterrows():
            z = row["z"]
            DM_obs = row["DM_over_rd"]
            sDM = row["sigma_DM"]
            H_obs = row["H_rd"]
            sH = row["sigma_H"]

            DM_model = model.DM(z) / self.r_d
            H_model = model.H(z) * self.r_d

            chi2 += ((DM_obs - DM_model) / sDM) ** 2
            chi2 += ((H_obs - H_model) / sH) ** 2

        return -0.5 * chi2
