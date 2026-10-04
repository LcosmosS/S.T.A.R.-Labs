# Batch TDA pipeline (fixed, one cell)
import os, sys, json, time, pickle, subprocess
from pathlib import Path
import numpy as np
import pandas as pd
from src.data.load_sky_surveys import load_sky_surveys

def test_sky_surveys_load():
    df1, df2 = load_sky_surveys(downsample=100, validate_schema=True)
    assert len(df1) > 0
    assert len(df2) > 0

# ---------- User-editable parameters ----------
aligned_csv = "derived/acsc_projected_cremona_ptd_aligned.csv"   # input aligned coords
coords_npz = "derived/coords_ptd_al.npz"                         # saved coords file
worker_script = "scripts/tda_worker.py"
out_dir = "derived/tda_ptd_batches"
chunk = 300                     # points per chunk (200-500 recommended)
maxdim = 1                      # compute H0/H1 only
sample_size_for_thresh = 2000   # sample size to estimate distance distribution
thresh_factor = 0.3             # thresh = median(sampled_pairwise_distances) * thresh_factor
max_workers = max(1, (os.cpu_count() or 2) - 1)  # concurrency bound
timeout_seconds = 600           # per-job timeout in seconds (10 minutes)
# ------------------------------------------------

Path("scripts").mkdir(parents=True, exist_ok=True)
Path("derived").mkdir(parents=True, exist_ok=True)
Path(out_dir).mkdir(parents=True, exist_ok=True)

# 1) Write worker script
worker_code = r'''
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
'''
Path(worker_script).write_text(worker_code)
print("Wrote worker script:", worker_script)

# 2) Load aligned CSV and save coords npz
if not Path(aligned_csv).exists():
    raise FileNotFoundError(f"Aligned CSV not found: {aligned_csv}")

df = pd.read_csv(aligned_csv)
if not {"x_ptd_al","y_ptd_al","z_ptd_al"}.issubset(df.columns):
    raise ValueError("Aligned CSV must contain x_ptd_al,y_ptd_al,z_ptd_al columns")

coords = df[["x_ptd_al","y_ptd_al","z_ptd_al"]].to_numpy()
np.savez_compressed(coords_npz, coords=coords)
print("Saved coords:", coords_npz, "shape:", coords.shape)

# 3) Estimate a conservative threshold from sampled pairwise distances
from scipy.spatial.distance import pdist
n = coords.shape[0]
sample_n = min(sample_size_for_thresh, n)
rng = np.random.RandomState(42)
sample_idx = rng.choice(n, size=sample_n, replace=False)
sample_coords = coords[sample_idx]
d = pdist(sample_coords)
median_d = float(np.median(d))
thresh = float(median_d * thresh_factor)
print(f"Sampled {sample_n} points; median pairwise distance {median_d:.6g}; chosen thresh {thresh:.6g}")

# 4) Build job list
jobs = []
for start in range(0, n, chunk):
    end = min(n, start + chunk)
    jobs.append({"start": int(start), "end": int(end)})

jobs_meta = {
    "coords_file": coords_npz,
    "out_dir": out_dir,
    "n_points": int(n),
    "chunk": int(chunk),
    "maxdim": int(maxdim),
    "thresh": float(thresh),
    "jobs_total": len(jobs),
    "created_at": time.time()
}
Path(out_dir, "jobs.json").write_text(json.dumps(jobs_meta, indent=2))
print("Prepared", len(jobs), "jobs; chunk size:", chunk, "max_workers:", max_workers)

# 5) Launch jobs with bounded concurrency and per-job timeout
active = []
completed = []
failed = []
job_index = 0

def launch_job(job):
    start, end = job["start"], job["end"]
    cmd = [sys.executable, worker_script, coords_npz, out_dir, str(start), str(end), str(maxdim), str(thresh)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return {"proc": p, "start": start, "end": end, "launched_at": time.time()}

print("Launching jobs...")
try:
    while job_index < len(jobs) or active:
        # launch while we have capacity
        while job_index < len(jobs) and len(active) < max_workers:
            job = jobs[job_index]
            handle = launch_job(job)
            active.append(handle)
            job_index += 1
            print(f"Launched job {handle['start']}:{handle['end']} (active {len(active)})")
            time.sleep(0.05)   # use float sleep

        # poll active processes
        for handle in active[:]:
            p = handle["proc"]
            ret = p.poll()
            elapsed = time.time() - handle["launched_at"]
            if ret is not None:
                # process finished
                try:
                    stdout, stderr = p.communicate(timeout=1)
                except Exception:
                    stdout, stderr = "", ""
                if ret == 0:
                    completed.append((int(handle['start']), int(handle['end'])))
                    print(f"Completed {handle['start']}:{handle['end']}")
                else:
                    failed.append((int(handle['start']), int(handle['end']), (stderr or "").strip()[:200]))
                    print(f"Failed {handle['start']}:{handle['end']} ret={ret} err={(stderr or '').strip()[:200]}")
                active.remove(handle)
            elif elapsed > timeout_seconds:
                # timeout: kill process
                try:
                    p.kill()
                except Exception:
                    pass
                failed.append((int(handle['start']), int(handle['end']), "timeout"))
                print(f"Timeout killed job {handle['start']}:{handle['end']}")
                active.remove(handle)
        # brief sleep to avoid busy loop
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Interrupted by user; terminating active workers...")
    for handle in active:
        try:
            handle["proc"].kill()
        except Exception:
            pass
    raise

# helper: sanitize objects for JSON
import numpy as _np
def _to_py(obj):
    if obj is None or isinstance(obj, (str, bool, int, float)):
        return obj
    if isinstance(obj, (_np.integer, _np.floating, _np.bool_)):
        return obj.item()
    if isinstance(obj, dict):
        return {str(k): _to_py(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_py(v) for v in obj]
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
    return str(obj)

def write_json_safe(path, obj, indent=2):
    Path(path).write_text(json.dumps(_to_py(obj), indent=indent))

# 6) Summary and write status (sanitized)
status = {
    "completed_count": int(len(completed)),
    "failed_count": int(len(failed)),
    "completed": completed[:20],
    "failed": failed[:20]
}
write_json_safe(Path(out_dir, "jobs_status.json"), status, indent=2)
print("All jobs processed. Completed:", len(completed), "Failed:", len(failed))

# 7) Aggregate results (load pickles)
import glob
pkl_files = sorted(glob.glob(os.path.join(out_dir, "dgms_*.pkl")))
print("Found pkl result files:", len(pkl_files))
all_results = []
for f in pkl_files:
    try:
        with open(f, "rb") as fh:
            res = pickle.load(fh)
        all_results.append(res)
    except Exception as e:
        print("Error loading", f, e)

# Example summary: print first 5 chunk diagram sizes
for i, res in enumerate(all_results[:5]):
    dgms = res.get("dgms", [])
    print(f"chunk {i} dgms lengths:", [len(d) for d in dgms])

# Save a small index manifest for downstream analysis (sanitized)
manifest = {
    "coords_file": coords_npz,
    "result_files": pkl_files,
    "n_chunks": len(pkl_files),
    "completed": len(completed),
    "failed": len(failed),
    "params": {"chunk": chunk, "max_workers": max_workers, "thresh": thresh, "maxdim": maxdim}
}
write_json_safe(Path(out_dir, "aggregate_manifest.json"), manifest, indent=2)
print("Wrote aggregate manifest:", Path(out_dir, "aggregate_manifest.json"))
print("Pipeline finished.")
