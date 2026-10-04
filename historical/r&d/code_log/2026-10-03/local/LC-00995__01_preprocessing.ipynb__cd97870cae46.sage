# Robust loader: reads CSV in chunks if file is large, returns DataFrame
def load_csv_maybe_chunks(path, max_rows=None, chunksize=200_000):
    if max_rows is not None:
        return pd.read_csv(path, nrows=max_rows)
    # try reading normally; fallback to chunks if memory error
    try:
        return pd.read_csv(path)
    except Exception as e:
        print(f"Standard read failed ({e}), trying chunked read...")
        chunks = []
        for chunk in pd.read_csv(path, chunksize=chunksize):
            chunks.append(chunk)
        return pd.concat(chunks, ignore_index=True)

# Load arithmetic catalogs
cremona = load_csv_maybe_chunks(ARITH_CREMONA)
lmfdb = load_csv_maybe_chunks(ARITH_LMFDB)
print(f"Cremona: {len(cremona):,} rows; LMFDB: {len(lmfdb):,} rows")

# Combine and keep provenance
cremona["source"] = "cremona"
lmfdb["source"] = "lmfdb"
df = pd.concat([cremona, lmfdb], ignore_index=True)
print("Combined rows:", len(df))
