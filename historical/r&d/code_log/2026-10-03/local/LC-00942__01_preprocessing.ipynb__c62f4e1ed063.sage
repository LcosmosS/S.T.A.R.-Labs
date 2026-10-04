# sanitize_and_write_summary.py
import json, numpy as np
from pathlib import Path

def _to_py(obj):
    # Convert numpy scalars, SymPy-like wrappers, and nested containers to plain Python types
    if obj is None or isinstance(obj, (str, bool, int, float)):
        return obj
    if isinstance(obj, (np.integer, np.floating, np.bool_)):
        return obj.item()
    if isinstance(obj, dict):
        return {str(k): _to_py(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_py(v) for v in obj]
    # Try numeric coercions for wrappers exposing __int__/__float__
    try:
        if hasattr(obj, "__int__") and not isinstance(obj, bool):
            return int(obj)
    except Exception:
        pass
    try:
        if hasattr(obj, "__float__"):
            return float(obj)
    except Exception:
        pass
    # Fallback to string
    return str(obj)

# Load summaries from memory if present, otherwise reconstruct from all_results
try:
    summaries  # use existing variable if in notebook namespace
except NameError:
    # attempt to reconstruct minimal summaries from pickles
    import glob, pickle
    files = sorted(glob.glob("derived/tda_ptd_batches/dgms_*.pkl"))
    summaries = []
    for f in files:
        with open(f, "rb") as fh:
            res = pickle.load(fh)
        dgms = res.get("dgms", [])
        h0 = np.asarray(dgms[0]) if len(dgms) > 0 else np.empty((0,2))
        h1 = np.asarray(dgms[1]) if len(dgms) > 1 else np.empty((0,2))
        summaries.append({
            "file": f,
            "n_h0": int(len(h0)),
            "n_h1": int(len(h1)),
            "h0_mean_life": float(np.mean(h0[:,1]-h0[:,0])) if h0.size else 0.0,
            "h1_mean_life": float(np.mean(h1[:,1]-h1[:,0])) if h1.size else 0.0
        })

out_path = Path("derived/tda_ptd_batches/summary_per_chunk.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(_to_py(summaries), indent=2))
print("Wrote sanitized summary to", out_path)
