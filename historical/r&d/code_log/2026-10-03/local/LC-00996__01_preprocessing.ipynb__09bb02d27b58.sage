# Map common column names to the keys expected by acsc.projection
# Adjust these mappings to match your CSV column names.
col_map = {
    "delta": ["delta", "minimal_discriminant", "disc", "D"],
    "conductor": ["conductor", "N"],
    "rank": ["sage_rank", "rank", "algebraic_rank"],
    "regulator": ["regulator", "R"],
    "real_period": ["real_period", "omega_real", "Q"],
    "torsion_order": ["torsion_order", "torsion", "T"],
}

def find_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

# Build a normalized DataFrame with required keys
records = []
missing = set()
for idx, row in df.iterrows():
    rec = {}
    for key, candidates in col_map.items():
        col = find_col(df, candidates)
        if col is None:
            missing.add(key)
            rec[key] = None
        else:
            rec[key] = row[col]
    rec["source"] = row.get("source", None)
    records.append(rec)

if missing:
    print("Warning: missing columns for keys:", missing)

# Convert to DataFrame for numeric cleaning
rec_df = pd.DataFrame(records)

# Clean numeric columns robustly
for c in ["delta", "conductor", "rank", "regulator", "real_period", "torsion_order"]:
    if c in rec_df.columns:
        rec_df[c] = pd.to_numeric(rec_df[c], errors="coerce")

# Drop rows missing essential invariants (choose policy: drop or impute)
essential = ["delta", "conductor", "rank"]
before = len(rec_df)
rec_df = rec_df.dropna(subset=essential)
after = len(rec_df)
print(f"Dropped {before-after} rows missing essential invariants; remaining {after}")
