"""Utility functions for I/O and reproducibility."""
import json
from pathlib import Path

def save_manifest(data, path):
    """Save reproducibility manifest."""
    Path(path).write_text(json.dumps(data, indent=2))

def set_seed(seed=42):
    """Set all random seeds for reproducibility."""
    import numpy as np
    np.random.seed(seed)
