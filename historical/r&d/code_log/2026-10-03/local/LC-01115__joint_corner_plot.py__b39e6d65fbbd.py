"""
Joint Posterior Corner Plot
===========================

Generates a corner plot for the full joint likelihood:
Planck + SH0ES + DESI BAO + Cosmic Chronometers
"""

from __future__ import annotations
import corner
import matplotlib.pyplot as plt


def plot_joint_corner(chain, param_names, save_path=None):
    fig = corner.corner(
        chain,
        labels=param_names,
        show_titles=True,
        title_fmt=".3f",
        quantiles=[0.16, 0.5, 0.84],
        title_kwargs={"fontsize": 12},
        label_kwargs={"fontsize": 12},
        smooth=1.0,
        color="navy"
    )

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    return fig
