"""
S.T.A.R. Model Parameter Constraints Table
==========================================

Generates a publication-ready table of posterior constraints from an MCMC chain.
"""

from __future__ import annotations
import numpy as np
import pandas as pd


def summarize_chain(chain, param_names):
    """
    Returns a DataFrame with:
    - mean
    - median
    - 1σ lower/upper
    - 2σ lower/upper
    """
    summary = []

    for i, name in enumerate(param_names):
        samples = chain[:, i]
        mean = np.mean(samples)
        median = np.median(samples)
        lo_1, hi_1 = np.percentile(samples, [16, 84])
        lo_2, hi_2 = np.percentile(samples, [2.5, 97.5])

        summary.append({
            "parameter": name,
            "mean": mean,
            "median": median,
            "1σ_low": lo_1,
            "1σ_high": hi_1,
            "2σ_low": lo_2,
            "2σ_high": hi_2,
        })

    return pd.DataFrame(summary)


def to_markdown_table(df):
    """Return a Markdown table."""
    return df.to_markdown(index=False)


def to_latex_table(df):
    """Return a LaTeX table."""
    return df.to_latex(index=False, float_format="%.4f")
