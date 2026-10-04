# Full cleaned cell: robust CSV cleanup + helpers (to_json_safe, coercion) + log-based filling
# Paste and run in your Jupyter notebook. Requires pandas.
# Backs up original, removes repeated headers, deduplicates, normalizes numeric fields,
# fills missing fields from sage_logs/sage_<label>.log, writes cleaned CSV and summary.

import ast, csv, json, math, os, re, shutil, sys, traceback, time
from fractions import Fraction
from pathlib import Path
import pandas as pd

# ---------- CONFIG ----------
SRC = Path("rank_verification_master_consensus.csv")
BACKUP = SRC.with_suffix(".backup.csv")
OUT = Path("rank_verification_master_consensus.cleaned.csv")
WORKDIR = Path("batch_work_verbose")
LOGDIR = Path("sage_logs")
WORKDIR.mkdir(exist_ok=True)
LOGDIR.mkdir(exist_ok=True)
# expected header (used for filtering repeated headers)
EXPECTED_COLS = [
    "label","a_list",
    "pari_sel2_raw","pari_sel2_dim","pari_analytic_rank","pari_error",
    "sage_two_descent_logfile","sage_two_descent","sage_rank_primary","sage_rank_fallback",
    "discriminant","j_invariant","regulator","tamagawa","torsion","real_period",
    "consensus_rank","consensus_reason","notes","time_s"
]
# ------------------------------------------------

if not SRC.exists():
    raise FileNotFoundError(f"Source file not found: {SRC}")

# Backup original
shutil.copy2(SRC, BACKUP)
print(f"Backed up original to {BACKUP}")

# Read raw lines and remove repeated header occurrences
with open(SRC, "r", encoding="utf-8", errors="replace") as f:
    raw_lines = f.readlines()

# Find first non-empty header line
header_line = None
for ln in raw_lines:
    if ln.strip():
        header_line = ln.strip()
        break
if header_line is None:
    raise RuntimeError("No header found in CSV")

filtered_lines = []
first_header_seen = False
for ln in raw_lines:
    if ln.strip() == header_line:
        if not first_header_seen:
            filtered_lines.append(ln)
            first_header_seen = True
        else:
            # skip repeated header
            continue
    else:
        filtered_lines.append(ln)

tmp = SRC.with_suffix(".tmp.csv")
with open(tmp, "w", encoding="utf-8", newline="") as f:
    f.writelines(filtered_lines)

# Read with pandas, tolerant to bad lines
try:
    df = pd.read_csv(tmp, dtype=str, keep_default_na=False, na_values=["", "NA", "None"])
except Exception:
    df = pd.read_csv(tmp, dtype=str, engine="python", on_bad_lines="skip", keep_default_na=False, na_values=["", "NA", "None"])

print(f"Loaded {len(df)} rows after removing repeated headers")

# If header differs, ensure expected columns exist (add missing as empty)
for c in EXPECTED_COLS:
    if c not in df.columns:
        df[c] = pd.NA

# Remove accidental embedded header rows (e.g., rows where label == 'label')
df = df[df['label'].astype(str).str.lower() != 'label']

# Trim whitespace and drop empty labels
df['label'] = df['label'].astype(str).str.strip()
df = df[df['label'] != ""]

# ---------- Helpers ----------
def to_json_safe(obj):
    """Recursively convert objects to JSON-serializable Python types."""
    if obj is None:
        return None
    if isinstance(obj, (str, bool, int, float)):
        return obj
    try:
        if hasattr(obj, "__int__") and not isinstance(obj, int):
            return int(obj)
        if hasattr(obj, "__float__") and not isinstance(obj, float):
            return float(obj)
    except Exception:
        pass
    if isinstance(obj, (list, tuple)):
        return [to_json_safe(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): to_json_safe(v) for k, v in obj.items()}
    return str(obj)

def parse_a_list(s):
    """Parse a_list-like strings into a list of 5 ints if possible."""
    if s is None or (isinstance(s, float) and math.isnan(s)):
        return None
    try:
        if isinstance(s, (list, tuple)):
            return [int(x) for x in s[:5]]
        s2 = str(s).strip()
        if s2.startswith("[") and s2.endswith("]"):
            arr = ast.literal_eval(s2)
            if isinstance(arr, (list, tuple)) and len(arr) >= 5:
                return [int(arr[i]) for i in range(5)]
        nums = re.findall(r"-?\d+", s2)
        if len(nums) >= 5:
            return [int(nums[i]) for i in range(5)]
    except Exception:
        pass
    return None

def parse_numeric_field(val):
    """Parse integers, floats, and rationals like '-2705452128/49' into Python types (Fraction or int/float)."""
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return None
    s = str(val).strip()
    if s == "":
        return None
    # rational
    if "/" in s and re.match(r"^-?\d+/\d+$", s):
        try:
            return Fraction(s)
        except Exception:
            pass
    # integer
    if re.match(r"^-?\d+$", s):
        try:
            return int(s)
        except Exception:
            pass
    # float
    try:
        return float(s)
    except Exception:
        pass
    return s  # fallback to string

def coerce_scalar(x):
    """Coerce Sage/PARI numeric-like objects to native Python scalars where possible."""
    if x is None:
        return None
    try:
        if hasattr(x, "__int__") and not isinstance(x, int):
            return int(x)
        if hasattr(x, "__float__") and not isinstance(x, float):
            return float(x)
    except Exception:
        pass
    if isinstance(x, (int, float, str)):
        return x
    return str(x)

# ---------- Parse a_list and create parsed numeric columns ----------
df['a_list_parsed'] = df['a_list'].apply(parse_a_list)
# Ensure native ints in a_list_parsed
df['a_list_parsed'] = df['a_list_parsed'].apply(lambda arr: [int(x) for x in arr] if arr is not None else None)

# Create parsed numeric columns (suffix _parsed)
numeric_cols = [
    ("pari_sel2_dim", "pari_sel2_dim_parsed"),
    ("pari_analytic_rank", "pari_analytic_rank_parsed"),
    ("sage_rank_primary", "sage_rank_primary_parsed"),
    ("sage_rank_fallback", "sage_rank_fallback_parsed"),
    ("discriminant", "discriminant_parsed"),
    ("j_invariant", "j_invariant_parsed"),
    ("regulator", "regulator_parsed"),
    ("real_period", "real_period_parsed"),
    ("consensus_rank", "consensus_rank_parsed"),
    ("time_s", "time_s_parsed")
]
for src_col, parsed_col in numeric_cols:
    if src_col in df.columns:
        df[parsed_col] = df[src_col].apply(parse_numeric_field)
    else:
        df[parsed_col] = None

# Some rows may have embedded Sage outputs in other columns; attempt a light salvage from 'sage_two_descent'
def salvage_embedded_fields(s):
    if not isinstance(s, str):
        return {}
    out = {}
    # look for patterns like True,1,1,... or sequences of small integers
    if "True" in s or "False" in s:
        parts = [p.strip() for p in s.split(",")]
        ints = [p for p in parts if re.match(r"^-?\d+$", p)]
        if len(ints) >= 2:
            try:
                out['sage_rank_primary_parsed'] = int(ints[0])
                out['sage_rank_fallback_parsed'] = int(ints[1])
            except Exception:
                pass
    return out

salvaged = 0
for idx, row in df.iterrows():
    s = row.get('sage_two_descent') or ""
    if isinstance(s, str) and s.strip():
        got = salvage_embedded_fields(s)
        if got.get('sage_rank_primary_parsed') is not None and pd.isna(row.get('sage_rank_primary_parsed')):
            df.at[idx, 'sage_rank_primary_parsed'] = got['sage_rank_primary_parsed']; salvaged += 1
        if got.get('sage_rank_fallback_parsed') is not None and pd.isna(row.get('sage_rank_fallback_parsed')):
            df.at[idx, 'sage_rank_fallback_parsed'] = got['sage_rank_fallback_parsed']; salvaged += 1

if salvaged:
    print(f"Salvaged {salvaged} rank fields from embedded sage_two_descent text")

# ---------- Deduplicate by label using a native integer score ----------
parsed_cols = [c for c in df.columns if c.endswith("_parsed")]
if not parsed_cols:
    parsed_cols = [c for c in ["pari_sel2_dim_parsed","pari_analytic_rank_parsed","sage_rank_primary_parsed","sage_rank_fallback_parsed","discriminant_parsed","j_invariant_parsed","regulator_parsed","real_period_parsed"] if c in df.columns]

if parsed_cols:
    df["_score"] = df[parsed_cols].notna().sum(axis=1).astype(int)
else:
    df["_score"] = df.notna().sum(axis=1).astype(int)

# small bonus if sage_two_descent text exists
df["_score"] = df["_score"] + df["sage_two_descent"].notna().astype(int)

df = df.sort_values(["label", "_score"], ascending=[True, True])
df = df.drop_duplicates(subset="label", keep="last").reset_index(drop=True)
df = df.drop(columns=["_score"], errors="ignore")

print(f"After deduplication: {len(df)} unique labels")

# ---------- Extract missing info from per-curve logs ----------
def extract_from_log(label):
    logfile = LOGDIR / f"sage_{label}.log"
    if not logfile.exists():
        return {}
    text = logfile.read_text(errors="ignore")
    out = {}
    # common patterns written by worker_verbose
    m = re.search(r"discriminant\s*=\s*([^\s,]+)", text)
    if m:
        out['discriminant_from_log'] = m.group(1)
    m = re.search(r"j_invariant\s*=\s*([^\s,]+)", text)
    if m:
        out['j_invariant_from_log'] = m.group(1)
    m = re.search(r"rank_primary\s*=\s*([0-9]+)", text)
    if m:
        out['rank_primary_from_log'] = int(m.group(1))
    m = re.search(r"rank_fallback\s*=\s*([0-9]+)", text)
    if m:
        out['rank_fallback_from_log'] = int(m.group(1))
    m = re.search(r"regulator\s*=\s*([0-9.eE+-/]+)", text)
    if m:
        out['regulator_from_log'] = m.group(1)
    m = re.search(r"tamagawa\s*=\s*([^\s,]+)", text)
    if m:
        out['tamagawa_from_log'] = m.group(1)
    m = re.search(r"torsion\s*=\s*(Torsion Subgroup isomorphic to .+)", text)
    if m:
        out['torsion_from_log'] = m.group(1).strip()
    m = re.search(r"real_period\s*=\s*([0-9.eE+-]+)", text)
    if m:
        out['real_period_from_log'] = m.group(1)
    return out

filled = 0
for idx, row in df.iterrows():
    label = row['label']
    logvals = extract_from_log(label)
    if not logvals:
        continue
    if pd.isna(row.get('discriminant_parsed')) and logvals.get('discriminant_from_log'):
        df.at[idx, 'discriminant_parsed'] = parse_numeric_field(logvals['discriminant_from_log']); filled += 1
    if pd.isna(row.get('j_invariant_parsed')) and logvals.get('j_invariant_from_log'):
        df.at[idx, 'j_invariant_parsed'] = parse_numeric_field(logvals['j_invariant_from_log']); filled += 1
    if pd.isna(row.get('sage_rank_primary_parsed')) and logvals.get('rank_primary_from_log') is not None:
        df.at[idx, 'sage_rank_primary_parsed'] = logvals['rank_primary_from_log']; filled += 1
    if pd.isna(row.get('sage_rank_fallback_parsed')) and logvals.get('rank_fallback_from_log') is not None:
        df.at[idx, 'sage_rank_fallback_parsed'] = logvals['rank_fallback_from_log']; filled += 1
    if pd.isna(row.get('regulator_parsed')) and logvals.get('regulator_from_log'):
        df.at[idx, 'regulator_parsed'] = parse_numeric_field(logvals['regulator_from_log']); filled += 1
    if pd.isna(row.get('tamagawa_parsed')) and logvals.get('tamagawa_from_log'):
        df.at[idx, 'tamagawa_parsed'] = logvals['tamagawa_from_log']; filled += 1
    if pd.isna(row.get('torsion_parsed')) and logvals.get('torsion_from_log'):
        df.at[idx, 'torsion_parsed'] = logvals['torsion_from_log']; filled += 1
    if pd.isna(row.get('real_period_parsed')) and logvals.get('real_period_from_log'):
        df.at[idx, 'real_period_parsed'] = parse_numeric_field(logvals['real_period_from_log']); filled += 1

print(f"Filled {filled} missing fields from sage_logs where available")

# ---------- Build cleaned DataFrame for output ----------
out_cols = [
    "label",
    "a_list_parsed",
    "pari_sel2_raw",
    "pari_sel2_dim_parsed",
    "pari_analytic_rank_parsed",
    "pari_error",
    "sage_two_descent_logfile",
    "sage_two_descent",
    "sage_rank_primary_parsed",
    "sage_rank_fallback_parsed",
    "discriminant_parsed",
    "j_invariant_parsed",
    "regulator_parsed",
    "tamagawa_parsed",
    "torsion_parsed",
    "real_period_parsed",
    "consensus_rank",
    "consensus_reason",
    "notes",
    "time_s"
]

for c in out_cols:
    if c not in df.columns:
        df[c] = None

clean_df = df[out_cols].copy()
# Normalize a_list to JSON string for CSV readability
clean_df = clean_df.rename(columns={"a_list_parsed": "a_list"})
clean_df['a_list'] = clean_df['a_list'].apply(lambda x: json.dumps(x) if x is not None else "")

# Normalize parsed numeric columns for CSV (Fractions -> string, floats/ints -> string)
def normalize_for_csv(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return ""
    if isinstance(v, Fraction):
        return str(v)
    return str(v)

for c in ["pari_sel2_dim_parsed","pari_analytic_rank_parsed","sage_rank_primary_parsed","sage_rank_fallback_parsed","discriminant_parsed","j_invariant_parsed","regulator_parsed","real_period_parsed","tamagawa_parsed","torsion_parsed"]:
    if c in clean_df.columns:
        clean_df[c] = clean_df[c].apply(normalize_for_csv)

# Write cleaned CSV
clean_df.to_csv(OUT, index=False)
print(f"Wrote cleaned CSV to {OUT}")

# ---------- Summary and triage list ----------
missing_summary = {
    "missing_pari_sel2_dim": (clean_df['pari_sel2_dim_parsed'] == "").sum(),
    "missing_pari_analytic_rank": (clean_df['pari_analytic_rank_parsed'] == "").sum(),
    "missing_sage_rank_primary": (clean_df['sage_rank_primary_parsed'] == "").sum(),
    "missing_discriminant": (clean_df['discriminant_parsed'] == "").sum(),
    "rows_total": len(clean_df)
}
print("Missing fields summary:", missing_summary)

# Labels needing manual inspection: no consensus and missing both PARI analytic and Sage rank
manual = clean_df[
    (clean_df['consensus_rank'].isna() | (clean_df['consensus_rank'] == "")) &
    (clean_df['pari_analytic_rank_parsed'] == "") &
    (clean_df['sage_rank_primary_parsed'] == "")
]['label'].tolist()

print(f"{len(manual)} labels need manual inspection. Example first 40:", manual[:40])

# Save triage CSV for manual review
TRIAGE = Path("rank_verification_triage.csv")
triage_df = clean_df[clean_df['label'].isin(manual)].copy()
if not triage_df.empty:
    triage_df.to_csv(TRIAGE, index=False)
    print(f"Wrote triage CSV with {len(triage_df)} rows to {TRIAGE}")

print("Cleaning complete.")