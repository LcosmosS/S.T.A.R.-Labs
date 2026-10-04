import pandas as pd
from fractions import Fraction
from pathlib import Path
import json, math

CLEAN = Path("rank_verification_master_consensus.cleaned.csv")
OUT_FINAL = Path("rank_verification_master_consensus.final.csv")
TRIAGE = Path("rank_verification_triage_final.csv")

if not CLEAN.exists():
    raise FileNotFoundError(f"Cleaned CSV not found: {CLEAN}")

df = pd.read_csv(CLEAN, dtype=str).fillna("")

# Helper to treat empty strings as missing
def empty_to_none(x):
    return None if x == "" else x

# Normalize columns: keep raw string columns and create numeric parsed columns
def parse_maybe_fraction(s):
    if s is None or s == "":
        return None
    s = str(s).strip()
    if "/" in s:
        try:
            return Fraction(s)
        except Exception:
            return s
    try:
        if "." in s or "e" in s.lower():
            return float(s)
        return int(s)
    except Exception:
        return s

# Columns that may contain rationals or mixed types: coerce to object and keep raw string
mixed_cols = ["discriminant_parsed","j_invariant_parsed","regulator_parsed","tamagawa_parsed","real_period_parsed"]
for c in mixed_cols:
    if c in df.columns:
        # ensure object dtype
        df[c] = df[c].astype(object)
        # create a numeric-parsed column if useful
        df[c + "_num"] = df[c].apply(lambda v: parse_maybe_fraction(empty_to_none(v)))

# Parse rank columns into integers where possible
rank_cols = ["pari_sel2_dim_parsed","pari_analytic_rank_parsed","sage_rank_primary_parsed","sage_rank_fallback_parsed","consensus_rank"]
for c in rank_cols:
    if c in df.columns:
        def to_int_or_none(v):
            v = empty_to_none(v)
            if v is None:
                return None
            try:
                return int(float(str(v)))
            except Exception:
                return None
        df[c + "_num"] = df[c].apply(to_int_or_none)

# Consensus decision function (same rules as before, but using numeric parsed columns)
def consensus_decision_row(row):
    pari_sel2 = row.get("pari_sel2_dim_parsed_num")
    pari_analytic = row.get("pari_analytic_rank_parsed_num")
    sage_primary = row.get("sage_rank_primary_parsed_num")
    sage_fallback = row.get("sage_rank_fallback_parsed_num")
    # prefer certified Sage primary, else fallback
    sage_rank = sage_primary if sage_primary is not None else sage_fallback
    if sage_rank is not None and pari_analytic is not None and pari_analytic == sage_rank:
        return sage_rank, "sage_vs_pari_analytic_agree"
    if sage_rank is not None and isinstance(pari_sel2, (int,)) and pari_sel2 == sage_rank:
        return sage_rank, "sage_vs_sel2_agree"
    if pari_analytic is not None and isinstance(pari_sel2, (int,)) and pari_analytic == pari_sel2:
        return pari_analytic, "pari_analytic_vs_sel2_agree"
    if pari_analytic is not None and sage_rank is not None and pari_analytic == sage_rank:
        return pari_analytic, "pari_analytic_and_sage_agree"
    if sage_rank is not None and pari_analytic is None and pari_sel2 is None:
        return sage_rank, "sage_only"
    if pari_analytic is not None and sage_rank is None:
        return pari_analytic, "pari_analytic_only"
    if isinstance(pari_sel2, int):
        return None, f"sel2_lower_bound={pari_sel2}"
    return None, "no_consensus"

# Apply consensus to each row
consensus_vals = df.apply(consensus_decision_row, axis=1, result_type="expand")
consensus_vals.columns = ["consensus_rank_computed","consensus_reason_computed"]
df["consensus_rank_computed"] = consensus_vals["consensus_rank_computed"]
df["consensus_reason_computed"] = consensus_vals["consensus_reason_computed"]

# If consensus_rank column exists and is empty, fill from computed consensus
if "consensus_rank" in df.columns:
    df["consensus_rank_filled"] = df.apply(lambda r: r["consensus_rank_computed"] if (r["consensus_rank"]=="" or r["consensus_rank"] is None) else r["consensus_rank"], axis=1)
else:
    df["consensus_rank_filled"] = df["consensus_rank_computed"]

# Prepare final output columns (keep raw and numeric parsed)
final_cols = [
    "label","a_list",
    "pari_sel2_raw","pari_sel2_dim_parsed","pari_sel2_dim_parsed_num",
    "pari_analytic_rank_parsed","pari_analytic_rank_parsed_num",
    "sage_rank_primary_parsed","sage_rank_primary_parsed_num",
    "sage_rank_fallback_parsed","sage_rank_fallback_parsed_num",
    "discriminant_parsed","discriminant_parsed_num",
    "j_invariant_parsed","j_invariant_parsed_num",
    "regulator_parsed","regulator_parsed_num",
    "tamagawa_parsed","tamagawa_parsed_num",
    "real_period_parsed","real_period_parsed_num",
    "consensus_rank","consensus_rank_filled","consensus_reason_computed","consensus_reason"
]
# Keep only columns that exist
final_cols = [c for c in final_cols if c in df.columns]

df_final = df[final_cols].copy()

# Write final CSV
df_final.to_csv(OUT_FINAL, index=False)
print("Wrote final consensus CSV to", OUT_FINAL)

# Create triage CSV: rows with no consensus and missing both PARI analytic and Sage primary
triage_mask = (
    (df_final.get("consensus_rank_filled").isna() | (df_final.get("consensus_rank_filled") == "")) &
    (df_final.get("pari_analytic_rank_parsed_num").isna()) &
    (df_final.get("sage_rank_primary_parsed_num").isna())
)
triage = df_final[triage_mask]
triage.to_csv(TRIAGE, index=False)
print("Wrote triage CSV to", TRIAGE, "rows:", len(triage))

# Print short summary
print("Summary")
print(" total rows:", len(df_final))
print(" consensus assigned:", df_final['consensus_rank_filled'].notna().sum())
print(" triage rows needing manual inspection:", len(triage))