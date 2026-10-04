"""
Sky Survey Dataset Builder
==========================

Merges the two sky-survey datasets into a unified table with:
- RA/Dec
- redshift
- magnitudes
- cosmology-ready fields
"""

from __future__ import annotations
import pandas as pd
from pathlib import Path
from src.data.load_sky_surveys import load_sky_surveys
from src.utils.astro_utils import clean_dataframe


class SkySurveyDatasetBuilder:
    def __init__(self, downsample=None):
        self.downsample = downsample

    def build(self):
        df1, df2 = load_sky_surveys(downsample=self.downsample)
        df = pd.concat([df1, df2], ignore_index=True)
        df = clean_dataframe(df)
        return df

    def save(self, path="data/processed/sky_surveys.parquet"):
        df = self.build()
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(path)
        return path
