"""Utility functions for I/O and reproducibility."""
import json
from pathlib import Path
from src.data.load_sky_surveys import load_sky_surveys

def test_sky_surveys_load():
    df1, df2 = load_sky_surveys(downsample=100, validate_schema=True)
    assert len(df1) > 0
    assert len(df2) > 0

def save_manifest(data, path):
    """Save reproducibility manifest."""
    Path(path).write_text(json.dumps(data, indent=2))

def set_seed(seed=42):
    """Set all random seeds for reproducibility."""
    import numpy as np
    np.random.seed(seed)
