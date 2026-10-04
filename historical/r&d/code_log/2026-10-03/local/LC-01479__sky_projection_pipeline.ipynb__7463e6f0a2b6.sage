# 1. Imports & Project Root Setup
import sys
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_project_root():
    cwd = Path.cwd().resolve()
    for parent in [cwd] + list(cwd.parents):
        if (parent / "src").exists():
            return parent
    return cwd

ROOT = get_project_root()
sys.path.insert(0, str(ROOT))
print(" Project root:", ROOT)