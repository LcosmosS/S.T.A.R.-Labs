import csv, json, math, os, time, traceback
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

if not FINAL_CSV.exists():
    raise FileNotFoundError(f"Final CSV not found: {FINAL_CSV}")

# load final CSV (strings)
df = pd.read_csv(FINAL_CSV, dtype=str).fillna("")

# helper to interpret parsed numeric columns (they may be empty strings)
def to_int_or_none(s):
    if s is None or s == "" or str(s).strip() == "":
        return None
    try:
        return int(float(str(s)))
    except Exception:
        return None

# identify rows needing PARI (missing analytic rank or sel2 dim)
need_mask = df['pari_analytic_rank_parsed_num'].astype(str).apply(lambda s: s.strip() == "") | df['pari_sel2_dim_parsed_num'].astype(str).apply(lambda s: s.strip() == "")
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

    # helper to parse a_list string into list of ints
    import ast, re
    def parse_a_list_field(s):
        if s is None or s == "" or str(s).strip() == "":
            return None
        try:
            if isinstance(s, list):
                return [int(x) for x in s[:5]]
            st = str(s).strip()
            if st.startswith("[") and st.endswith("]"):
                arr = ast.literal_eval(st)
                return [int(arr[i]) for i in range(5)]
            nums = re.findall(r"-?\d+", st)
            if len(nums) >= 5:
                return [int(nums[i]) for i in range(5)]
        except Exception:
            pass
        return None

    # iterate in batches
    labels = missing_df['label'].tolist()
    start = START_INDEX
    for batch_start in range(start, n_missing, BATCH_SIZE):
        batch_labels = labels[batch_start: batch_start + BATCH_SIZE]
        batch_rows = []
        log(f"Processing PARI batch {batch_start}..{batch_start+len(batch_labels)-1} ({len(batch_labels)} curves)")
        for label in batch_labels:
            row = df[df['label'] == label].iloc[int(0)]
            a_list = parse_a_list_field(row.get('a_list', ""))
            if a_list is None:
                log(f"  {label}: missing a_list; skipping")
                batch_rows.append([label, row.get('a_list', ""), None, None, None, None, None, "no_a", 0.0])
                continue

            t0 = time.time()
            pari_error = None
            sel2_raw = None
            sel2_dim = None
            sel2_dim_num = None
            analytic_rank = None
            analytic_rank_num = None

            try:
                # ellinit
                a_str = ",".join(str(int(x)) for x in a_list)
                Epari = pari(f"ellinit([{a_str}])")
            except Exception as e:
                pari_error = f"ellinit_error:{e}"
                log(f"  {label}: ellinit failed: {e}")
                batch_rows.append([label, json.dumps(a_list), sel2_raw, sel2_dim, sel2_dim_num, analytic_rank, analytic_rank_num, pari_error, round(time.time()-t0,3)])
                continue

            # ellselmer(...,2)
            try:
                sel2 = pari("ellselmer")(Epari, 2)
                sel2_raw = str(sel2)
                try:
                    length = int(pari("length")(sel2))
                    if length > 0 and (length & (length - 1)) == 0:
                        sel2_dim = int(round(math.log2(length)))
                        sel2_dim_num = sel2_dim
                    else:
                        sel2_dim = length
                        # if length is not power of two, keep numeric length as-is
                        try:
                            sel2_dim_num = int(length)
                        except Exception:
                            sel2_dim_num = None
                except Exception:
                    sel2_dim = None
                    sel2_dim_num = None
            except Exception as e:
                pari_error = (pari_error or "") + f"; ellselmer_error:{e}"
                log(f"  {label}: ellselmer error: {e}")

            # analytic rank
            try:
                ar = pari("ellanalyticrank")(Epari)
                analytic_rank = str(ar)
                try:
                    analytic_rank_num = int(ar)
                except Exception:
                    analytic_rank_num = None
            except Exception:
                try:
                    ar2 = pari("ellrank")(Epari)
                    analytic_rank = str(ar2)
                    try:
                        analytic_rank_num = int(ar2)
                    except Exception:
                        analytic_rank_num = None
                except Exception as e:
                    pari_error = (pari_error or "") + f"; analytic_rank_error:{e}"
                    log(f"  {label}: analytic rank error: {e}")

            t_elapsed = time.time() - t0
            batch_rows.append([
                label,
                json.dumps(a_list),
                sel2_raw,
                sel2_dim,
                sel2_dim_num,
                analytic_rank,
                analytic_rank_num,
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
            if sel2_raw is not None:
                df.at[idx, 'pari_sel2_raw'] = sel2_raw
            if sel2_dim is not None:
                df.at[idx, 'pari_sel2_dim_parsed'] = str(sel2_dim)
            if sel2_dim_num is not None:
                df.at[idx, 'pari_sel2_dim_parsed_num'] = str(sel2_dim_num)
            if analytic_rank is not None:
                df.at[idx, 'pari_analytic_rank_parsed'] = str(analytic_rank)
            if analytic_rank_num is not None:
                df.at[idx, 'pari_analytic_rank_parsed_num'] = str(analytic_rank_num)
            if pari_error is not None:
                prev = df.at[idx, 'pari_error'] if 'pari_error' in df.columns else ""
                df.at[idx, 'pari_error'] = (prev + ";" + pari_error).lstrip(";")

        # persist updated cleaned CSV (so you can resume)
        backup = FINAL_CSV.with_suffix(".pari_update_backup.csv")
        df.to_csv(backup, index=False)
        log(f"  Wrote intermediate backup {backup}")

    # final write: merge updates into FINAL_CSV (overwrite)
    df.to_csv(FINAL_CSV, index=False)
    log(f"Finished PARI rerun. Updated final CSV: {FINAL_CSV}")

log("PARI re-run complete.")