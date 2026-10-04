# List and quick verify
from pathlib import Path
import glob, pickle, json

out_dir = Path("derived/tda_ptd_batches")
pkl_files = sorted(glob.glob(str(out_dir / "dgms_*.pkl")))
err_files = sorted(glob.glob(str(out_dir / "error_*.json")))

print("Result files:", len(pkl_files))
print("Error files:", len(err_files))
# show first and last few
print("Sample files:", pkl_files[:3], "...", pkl_files[-3:])
