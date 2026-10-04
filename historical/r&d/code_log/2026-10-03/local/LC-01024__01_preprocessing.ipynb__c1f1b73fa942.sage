import ast, csv, json, math, os, re, subprocess, sys, threading, time
from pathlib import Path
from queue import Queue, Empty
import pandas as pd

# CONFIG
INPUT_CSV = "arithmetic_verified.csv"
MASTER_OUT = "rank_verification_master_consensus.csv"
WORKDIR = Path("batch_work_verbose")
WORKDIR.mkdir(exist_ok=True)
BATCH_SIZE = int(15)
TWO_LIMIT = 10000
SAGE_CMD = "sage"   # or full path
WORKER_SCRIPT = "sage_worker_verbose.py"
LOGDIR = Path("sage_logs")
LOGDIR.mkdir(exist_ok=True)

# helper: parse a-invariants
def parse_a_field(field):
    if pd.isna(field) or field is None:
        return None
    if isinstance(field, (list, tuple)):
        return [int(x) for x in field[:5]]
    s = str(field).strip()
    if s.startswith("[") and s.endswith("]"):
        try:
            obj = ast.literal_eval(s)
            if isinstance(obj, (list, tuple)) and len(obj) >= 5:
                return [int(obj[i]) for i in range(5)]
        except Exception:
            pass
    ints = re.findall(r"-?\d+", s)
    if len(ints) >= 5:
        return [int(ints[i]) for i in range(5)]
    return None

# PARI helpers (best-effort)
def pari_ellinit(a_list):
    a_str = ",".join(str(int(x)) for x in a_list)
    return pari(f"ellinit([{a_str}])")

def pari_2selmer_and_analytic(E_pari):
    out = {"sel2_raw": None, "sel2_dim": None, "analytic_rank": None, "pari_error": None}
    try:
        sel2 = pari("ellselmer")(E_pari, 2)
        out["sel2_raw"] = str(sel2)
        try:
            length = int(pari("length")(sel2))
            if length > 0 and (length & (length - 1)) == 0:
                out["sel2_dim"] = int(round(math.log2(length)))
            else:
                out["sel2_dim"] = length
        except Exception:
            out["sel2_dim"] = None
    except Exception as e:
        out["pari_error"] = f"ellselmer_error:{e}"
        # continue to try analytic rank
    try:
        ar = pari("ellanalyticrank")(E_pari)
        out["analytic_rank"] = int(ar)
    except Exception:
        try:
            ar2 = pari("ellrank")(E_pari)
            out["analytic_rank"] = int(ar2)
        except Exception:
            out["analytic_rank"] = None
    return out

def to_json_safe(obj):
    """Recursively convert objects to JSON-serializable Python types."""
    if obj is None:
        return None
    # native primitives
    if isinstance(obj, (str, bool, int, float)):
        return obj
    # convert Sage/PARI numeric-like objects
    try:
        if hasattr(obj, "__int__") and not isinstance(obj, int):
            return int(obj)
        if hasattr(obj, "__float__") and not isinstance(obj, float):
            return float(obj)
    except Exception:
        pass
    # lists/tuples
    if isinstance(obj, (list, tuple)):
        return [to_json_safe(x) for x in obj]
    # dicts
    if isinstance(obj, dict):
        return {str(k): to_json_safe(v) for k, v in obj.items()}
    # fallback: string representation
    return str(obj)


# start persistent worker
proc = subprocess.Popen([SAGE_CMD, "-python", WORKER_SCRIPT],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        text=True, bufsize=int(1))

# thread to read stdout lines into a queue
stdout_q = Queue()
stderr_q = Queue()
def enqueue(pipe, q):
    for line in iter(pipe.readline, ''):
        if not line:
            break
        q.put(line)
    pipe.close()

t_out = threading.Thread(target=enqueue, args=(proc.stdout, stdout_q), daemon=True)
t_err = threading.Thread(target=enqueue, args=(proc.stderr, stderr_q), daemon=True)
t_out.start(); t_err.start()

# load input and master
if not Path(INPUT_CSV).exists():
    raise FileNotFoundError(INPUT_CSV)
df = pd.read_csv(INPUT_CSV, dtype=str)
n = len(df)
print(f"Loaded {n} rows from {INPUT_CSV}")

if not Path(MASTER_OUT).exists():
    with open(MASTER_OUT, "w", newline="") as mf:
        writer = csv.writer(mf)
        header = [
            "label","a_list",
            "pari_sel2_raw","pari_sel2_dim","pari_analytic_rank","pari_error",
            "sage_two_descent_logfile","sage_two_descent","sage_rank_primary","sage_rank_fallback",
            "discriminant","j_invariant","regulator","tamagawa","torsion","real_period",
            "consensus_rank","consensus_reason","notes","time_s"
        ]
        writer.writerow(header)

# build processed set
processed = set()
try:
    mdf = pd.read_csv(MASTER_OUT, dtype=str)
    processed.update(mdf['label'].astype(str).tolist())
except Exception:
    pass

# consensus decision function
def consensus_decision(pari_sel2_dim, pari_analytic, sage_primary, sage_fallback):
    # prefer certified Sage primary, else fallback
    sage_rank = sage_primary if sage_primary is not None else sage_fallback
    # if Sage gives a rank and PARI analytic agrees -> consensus
    if sage_rank is not None and pari_analytic is not None and int(pari_analytic) == int(sage_rank):
        return int(sage_rank), "sage_vs_pari_analytic_agree"
    # if Sage rank equals inferred sel2_dim (when sel2_dim is numeric and equals rank) -> consensus
    if sage_rank is not None and isinstance(pari_sel2_dim, int) and pari_sel2_dim == sage_rank:
        return int(sage_rank), "sage_vs_sel2_agree"
    # if PARI analytic and sel2_dim agree -> consensus
    if pari_analytic is not None and isinstance(pari_sel2_dim, int) and pari_analytic == pari_sel2_dim:
        return int(pari_analytic), "pari_analytic_vs_sel2_agree"
    # if two independent sources (PARI analytic and Sage) both exist and equal -> consensus
    if pari_analytic is not None and sage_rank is not None and int(pari_analytic) == int(sage_rank):
        return int(pari_analytic), "pari_analytic_and_sage_agree"
    # if only one source exists, return it but mark as single_source
    if sage_rank is not None and pari_analytic is None and pari_sel2_dim is None:
        return int(sage_rank), "sage_only"
    if pari_analytic is not None and sage_rank is None:
        return int(pari_analytic), "pari_analytic_only"
    # if sel2_dim exists and is a lower bound, return None but note lower bound
    if isinstance(pari_sel2_dim, int):
        return None, f"sel2_lower_bound={pari_sel2_dim}"
    return None, "no_consensus"

# main loop: prefilter with PARI, send ambiguous to worker
for idx in range(0, n, BATCH_SIZE):
    batch = df.iloc[idx: idx + BATCH_SIZE]
    batch_results = []
    for i, row in batch.iterrows():
        label = str(row.get("label", f"row_{i}"))
        if label in processed:
            print(f"skip {label}")
            continue
        a_field = row.get("used_a_invariants") or row.get("a_list") or None
        a_list = parse_a_field(a_field)
        if a_list is None:
            try:
                a_list = [int(row.get(k)) for k in ("a1","a2","a3","a4","a6")]
            except Exception:
                a_list = None
        if a_list is None:
            batch_results.append([label, None] + [None]*16 + ["no_a", ""])
            processed.add(label)
            continue

        t0 = time.perf_counter()
        # PARI prefilter
        try:
            Epari = pari_ellinit(a_list)
            pari_res = pari_2selmer_and_analytic(Epari)
        except Exception as e:
            pari_res = {"sel2_raw": None, "sel2_dim": None, "analytic_rank": None, "pari_error": str(e)}

        # If PARI analytic and sel2_dim agree, we can avoid Sage
        if pari_res.get("sel2_dim") is not None and pari_res.get("analytic_rank") is not None and pari_res.get("sel2_dim") == pari_res.get("analytic_rank"):
            sage_td = None
            sage_primary = None
            sage_fallback = None
            logfile = None
            consensus_rank, reason = consensus_decision(pari_res.get("sel2_dim"), pari_res.get("analytic_rank"), sage_primary, sage_fallback)
        else:
            # send to worker (no timeout)
           # prepare and send task (safe)
            task = {"label": label, "a_list": to_json_safe(a_list), "two_limit": to_json_safe(TWO_LIMIT)}
            proc.stdin.write(json.dumps(task) + "\n")
            proc.stdin.flush()

            # wait for worker response
            resp_line = None
            while True:
                try:
                    resp_line = stdout_q.get(timeout=int(0.1))
                except Empty:
                    if proc.poll() is not None:
                        err = []
                        try:
                            while True:
                                err.append(stderr_q.get_nowait())
                        except Empty:
                            pass
                        raise RuntimeError("Sage worker terminated unexpectedly: " + "".join(err))
                    continue
                if resp_line:
                    break

            # parse and normalize
            try:
                resp = json.loads(resp_line)
            except Exception:
                resp = {"error": "json_parse_error_from_worker", "raw": resp_line}

            sage_primary = int(resp["rank_primary"]) if resp.get("rank_primary") is not None else None
            sage_fallback = int(resp["rank_fallback"]) if resp.get("rank_fallback") is not None else None
            sage_td = resp.get("two_descent")
            # pick up other numeric fields defensively
            disc = resp.get("discriminant")
            try:
                disc = int(disc) if disc is not None else None
            except Exception:
                pass

            # extract worker outputs
            sage_primary = resp.get("rank_primary")
            sage_fallback = resp.get("rank_fallback")
            sage_td = resp.get("two_descent") if resp.get("two_descent") is not None else None
            logfile = LOGDIR / f"sage_{label}.log"
            # attempt to pick up discriminant/j/regulator etc from worker
            disc = resp.get("discriminant")
            jinv = resp.get("j_invariant")
            regulator = resp.get("regulator")
            tamagawa = resp.get("tamagawa")
            torsion = resp.get("torsion")
            real_period = resp.get("real_period")
            consensus_rank, reason = consensus_decision(pari_res.get("sel2_dim"), pari_res.get("analytic_rank"), sage_primary, sage_fallback)

        t_elapsed = time.perf_counter() - t0

        row_out = [
            label,
            json.dumps(a_list),
            pari_res.get("sel2_raw"),
            pari_res.get("sel2_dim"),
            pari_res.get("analytic_rank"),
            str(logfile) if 'logfile' in locals() and logfile is not None else None,
            sage_td if 'sage_td' in locals() else None,
            sage_primary if 'sage_primary' in locals() else None,
            sage_fallback if 'sage_fallback' in locals() else None,
            disc if 'disc' in locals() else None,
            jinv if 'jinv' in locals() else None,
            regulator if 'regulator' in locals() else None,
            tamagawa if 'tamagawa' in locals() else None,
            torsion if 'torsion' in locals() else None,
            real_period if 'real_period' in locals() else None,
            consensus_rank,
            reason,
            ""
        ]
        batch_results.append(row_out)
        processed.add(label)
        print(f"{label}: consensus={consensus_rank} reason={reason} time={t_elapsed:.1f}s")

    # write batch file and append to master
    batch_file = WORKDIR / f"batch_{idx}_{idx+len(batch)-1}.csv"
    with open(batch_file, "w", newline="") as bf:
        writer = csv.writer(bf)
        writer.writerow([
            "label","a_list","pari_sel2_raw","pari_sel2_dim","pari_analytic_rank",
            "sage_two_descent_logfile","sage_two_descent","sage_rank_primary","sage_rank_fallback",
            "discriminant","j_invariant","regulator","tamagawa","torsion","real_period",
            "consensus_rank","consensus_reason","notes"
        ])
        writer.writerows(batch_results)
    with open(MASTER_OUT, "a", newline="") as mf:
        writer = csv.writer(mf)
        writer.writerows(batch_results)
    print(f"Wrote {batch_file} and appended to {MASTER_OUT}")

# close worker
proc.stdin.close()
time.sleep(int(0.5))
proc.terminate()
proc.wait()
print("Done. Master:", MASTER_OUT)