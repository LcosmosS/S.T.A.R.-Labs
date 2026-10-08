
# scripts/tda_worker.py
import sys, json, pickle, numpy as np
from pathlib import Path
from acsc.tda_pipeline import compute_persistence

def main(coords_npz, out_dir, start, end, maxdim="1", thresh="None"):
    coords_npz = Path(coords_npz)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    data = np.load(coords_npz)
    coords = data["coords"][int(start):int(end)]
    try:
        thr = None if thresh in ("None","none","") else float(thresh)
        res = compute_persistence(coords, maxdim=int(maxdim), thresh=thr)
        out_path = out_dir / f"dgms_{start}_{end}.pkl"
        with open(out_path, "wb") as fh:
            pickle.dump(res, fh)
        print("OK", start, end, out_path)
    except Exception as e:
        err_path = out_dir / f"error_{start}_{end}.json"
        err = {"start": int(start), "end": int(end), "error": str(e)}
        err_path.write_text(json.dumps(err))
        print("ERR", start, end, err_path)

if __name__ == "__main__":
    # usage: python scripts/tda_worker.py coords.npz out_dir start end [maxdim] [thresh]
    main(*sys.argv[1:])
