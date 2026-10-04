# PARI rerun patched cell — includes to_json_safe and normalization helpers
import csv, json, math, os, time, traceback, ast, re
from pathlib import Path
import pandas as pd

# ---------- CONFIG ----------
FINAL_CSV = Path("rank_verification_master_consensus.final.csv")   # input (existing final)
CLEANED_CSV = Path("rank_verification_master_consensus.cleaned.csv")  # optional backup
MASTER_OUT = Path("rank_verification_master_consensus.pari_updates.csv")  # incremental append file
WORKDIR = Path("pari_rerun_work")
WORKDIR.mkdir(exist_ok=True)
LOGFILE = WORKDIR / "pari_rerun.log"

BATCH_SIZE = int(15)   # adjust (start small)
START_INDEX = 0   # resume index in the list of missing rows
# ------------------------------------------------

def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOGFILE, "a") as f:
        f.write(line + "\n")

# ---------- Helpers ----------
def to_json_safe(obj):
    """Return a JSON-safe string for writing into CSVs (compact, no NaNs)."""
    try:
        return json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
    except Exception:
        try:
            return json.dumps(str(obj))
        except Exception:
            return '""'

def normalize_numeric_field(s):
    """Normalize numeric-like strings: empty -> None, numeric -> int if integral else float, else original string."""
    if s is None:
        return None
    st = str(s).strip()
    if st == "":
        return None
    # try integer
    try:
        if "." in st or "e" in st.lower():
            f = float(st)
            if abs(f - round(f)) < 1e-12:
                return int(round(f))
            return f
        return int(st)
    except Exception:
        # try to parse rational like '123/7'
        if "/" in st:
            try:
                num, den = st.split("/", 1)
                numf = float(num)
                denf = float(den)
                if denf != 0:
                    val = numf / denf
                    if abs(val - round(val)) < 1e-12:
                        return int(round(val))
                    return val
            except Exception:
                pass
        return st

def parse_a_list_field(s):
    """Parse a_list field into a 5-int list or None. Accepts JSON-like, Python list, or plain text."""
    if s is None:
        return None
    if isinstance(s, (list, tuple)):
        try:
            return [int(x) for x in list(s)[:5]]
        except Exception:
            return None
    st = str(s).strip()
    if st == "":
        return None
    # try JSON / Python literal
    try:
        if st.startswith("[") and st.endswith("]"):
            arr = ast.literal_eval(st)
            if isinstance(arr, (list, tuple)) and len(arr) >= 5:
                return [int(arr[i]) for i in range(5)]
    except Exception:
        pass
    # fallback: extract first 5 integers
    nums = re.findall(r"-?\d+", st)
    if len(nums) >= 5:
        try:
            return [int(nums[i]) for i in range(5)]
        except Exception:
            return None
    return None

# ---------- Main ----------
if not FINAL_CSV.exists():
    raise FileNotFoundError(f"Final CSV not found: {FINAL_CSV}")

# load final CSV as strings to avoid mixed dtypes; fillna with empty string
df = pd.read_csv(FINAL_CSV, dtype=str).fillna("")

# identify rows needing PARI (missing analytic rank or sel2 dim)
def is_blank(s):
    return s is None or str(s).strip() == ""

need_mask = df['pari_analytic_rank_parsed_num'].astype(str).apply(lambda s: s.strip() == "") | \
            df['pari_sel2_dim_parsed_num'].astype(str).apply(lambda s: s.strip() == "")
missing_df = df[need_mask].copy()
n_missing = len(missing_df)
log(f"Loaded {len(df)} rows; {n_missing} rows missing PARI results")

if n_missing == 0:
    log("No missing PARI rows found; nothing to do.")
else:
    # prepare master output header if not exists
    if not MASTER_OUT.exists():
        with open(MASTER_OUT, "w", newline="") as mf:
            writer = csv.writer(mf)
            header = [
                "label","a_list",
                "pari_sel2_raw","pari_sel2_dim_parsed","pari_sel2_dim_parsed_num",
                "pari_analytic_rank_parsed","pari_analytic_rank_parsed_num",
                "pari_error","time_s"
            ]
            writer.writerow(header)

    labels = missing_df['label'].tolist()
    start = START_INDEX
    for batch_start in range(start, n_missing, BATCH_SIZE):
        batch_labels = labels[batch_start: batch_start + BATCH_SIZE]
        batch_rows = []
        log(f"Processing PARI batch {batch_start}..{batch_start+len(batch_labels)-1} ({len(batch_labels)} curves)")
        for label in batch_labels:
            # pick the first matching row (should be unique)
            rows_matching = df.index[df['label'] == label].tolist()
            if not rows_matching:
                log(f"  {label}: not found in dataframe; skipping")
                continue
            row = df.loc[rows_matching[0]]  # safe integer index via .loc with index value
            a_list = parse_a_list_field(row.get('a_list', ""))
            if a_list is None:
                log(f"  {label}: missing a_list; skipping")
                batch_rows.append([label, to_json_safe(row.get('a_list', "")), "", "", "", "", "", "no_a", 0.0])
                continue

            t0 = time.time()
            pari_error = ""
            sel2_raw = ""
            sel2_dim = ""
            sel2_dim_num = ""
            analytic_rank = ""
            analytic_rank_num = ""

            try:
                # ellinit
                a_str = ",".join(str(int(x)) for x in a_list)
                Epari = pari(f"ellinit([{a_str}])")
            except Exception as e:
                pari_error = f"ellinit_error:{e}"
                log(f"  {label}: ellinit failed: {e}")
                batch_rows.append([label, to_json_safe(a_list), sel2_raw, sel2_dim, sel2_dim_num, analytic_rank, analytic_rank_num, pari_error, round(time.time()-t0,3)])
                continue

            # ellselmer(...,2) primary attempt then fallback
            try:
                # prefer calling ellselmer(E,2) if the PARI binding supports it; try both safe ways
                try:
                    sel2 = pari("ellselmer")(Epari, 2)
                except Exception:
                    # try direct call style
                    sel2 = pari("ellselmer")(Epari)
                sel2_raw = str(sel2)
                # try to interpret sel2 result: if it's a vector or list, try length
                try:
                    length = int(pari("length")(sel2))
                    if length > 0 and (length & (length - 1)) == 0:
                        sel2_dim = int(round(math.log2(length)))
                        sel2_dim_num = sel2_dim
                    else:
                        sel2_dim = str(length)
                        sel2_dim_num = int(length) if isinstance(length, int) else ""
                except Exception:
                    # if length fails, leave raw string and empty numeric
                    sel2_dim = str(sel2)
                    sel2_dim_num = ""
            except Exception as e:
                # record both primary and fallback messages if present
                msg = str(e)
                # try a fallback call that some PARI versions accept
                try:
                    sel2 = pari("ellselmer")(Epari)
                    sel2_raw = str(sel2)
                    try:
                        length = int(pari("length")(sel2))
                        if length > 0 and (length & (length - 1)) == 0:
                            sel2_dim = int(round(math.log2(length)))
                            sel2_dim_num = sel2_dim
                        else:
                            sel2_dim = str(length)
                            sel2_dim_num = int(length) if isinstance(length, int) else ""
                    except Exception:
                        sel2_dim = str(sel2)
                        sel2_dim_num = ""
                    log(f"  {label}: ellselmer fallback succeeded")
                except Exception as e2:
                    pari_error = (pari_error + ";" + f"ellselmer_error:{msg}; ellselmer_fallback_error:{e2}").lstrip(";")
                    log(f"  {label}: ellselmer error: {msg}; fallback error: {e2}")

            # analytic rank (try ellanalyticrank then ellrank)
            try:
                ar = pari("ellanalyticrank")(Epari)
                analytic_rank = str(ar)
                analytic_rank_num = normalize_numeric_field(str(ar))
            except Exception as e:
                try:
                    ar2 = pari("ellrank")(Epari)
                    analytic_rank = str(ar2)
                    analytic_rank_num = normalize_numeric_field(str(ar2))
                except Exception as e2:
                    pari_error = (pari_error + ";" + f"analytic_rank_error:{e}; analytic_rank_fallback_error:{e2}").lstrip(";")
                    log(f"  {label}: analytic rank error: {e}; fallback: {e2}")

            t_elapsed = time.time() - t0
            batch_rows.append([
                label,
                to_json_safe(a_list),
                sel2_raw,
                str(sel2_dim) if sel2_dim != "" else "",
                str(sel2_dim_num) if sel2_dim_num != "" else "",
                analytic_rank,
                str(analytic_rank_num) if analytic_rank_num is not None else "",
                pari_error,
                round(t_elapsed, 3)
            ])
            log(f"  {label}: done (sel2_dim={sel2_dim}, analytic_rank={analytic_rank_num}) time={t_elapsed:.2f}s")

        # write batch file and append to master
        batch_file = WORKDIR / f"pari_batch_{batch_start}_{batch_start+len(batch_rows)-1}.csv"
        with open(batch_file, "w", newline="") as bf:
            writer = csv.writer(bf)
            writer.writerow(["label","a_list","pari_sel2_raw","pari_sel2_dim_parsed","pari_sel2_dim_parsed_num","pari_analytic_rank_parsed","pari_analytic_rank_parsed_num","pari_error","time_s"])
            writer.writerows(batch_rows)
        log(f"  Wrote batch file {batch_file}")

        # append to MASTER_OUT
        with open(MASTER_OUT, "a", newline="") as mf:
            writer = csv.writer(mf)
            for r in batch_rows:
                writer.writerow(r)
        log(f"  Appended batch to master {MASTER_OUT}")

        # update in-memory df with new PARI results so subsequent batches see updated values
        for r in batch_rows:
            label = r[0]
            sel2_raw, sel2_dim, sel2_dim_num, analytic_rank, analytic_rank_num, pari_error = r[2], r[3], r[4], r[5], r[6], r[7]
            idxs = df.index[df['label'] == label].tolist()
            if not idxs:
                continue
            idx = idxs[0]
            if sel2_raw:
                df.at[idx, 'pari_sel2_raw'] = sel2_raw
            if sel2_dim:
                df.at[idx, 'pari_sel2_dim_parsed'] = sel2_dim
            if sel2_dim_num:
                df.at[idx, 'pari_sel2_dim_parsed_num'] = sel2_dim_num
            if analytic_rank:
                df.at[idx, 'pari_analytic_rank_parsed'] = analytic_rank
            if analytic_rank_num != "" and analytic_rank_num is not None:
                df.at[idx, 'pari_analytic_rank_parsed_num'] = str(analytic_rank_num)
            if pari_error:
                prev = df.at[idx, 'pari_error'] if 'pari_error' in df.columns else ""
                prev = "" if prev is None else str(prev)
                df.at[idx, 'pari_error'] = (prev + ";" + pari_error).lstrip(";")

        # persist updated cleaned CSV (so you can resume)
        backup = FINAL_CSV.with_suffix(".pari_update_backup.csv")
        df.to_csv(backup, index=False)
        log(f"  Wrote intermediate backup {backup}")

    # final write: merge updates into FINAL_CSV (overwrite)
    df.to_csv(FINAL_CSV, index=False)
    log(f"Finished PARI rerun. Updated final CSV: {FINAL_CSV}")

log("PARI re-run complete.")
