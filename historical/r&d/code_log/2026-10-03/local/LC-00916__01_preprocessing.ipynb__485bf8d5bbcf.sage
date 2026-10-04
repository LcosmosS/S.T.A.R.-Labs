# If running in a fresh environment, you may need to pip install the requirements.
# Uncomment the next cell to install from requirements.txt in a notebook environment.
# !pip install -r requirements.txt

# Import our package modules (assumes acsc/ is on PYTHONPATH or repo root)
from acsc.projection import project as project_records
from acsc.quantile import QuantileAligner

# Optional: tda/statistics modules for quick checks
from acsc.tda_pipeline import compute_persistence
from acsc.statistics import w2_between_diagrams, empirical_p_value
