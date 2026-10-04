         return np.nan
    try:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
        return E.discriminant()
    except (TypeError, ValueError):
        return np.nan

# --- 5. Main Processing Pipeline ---

def main():
    """The main function to run the data processing pipeline."""
    try:
        chunk_iter = pd.read_csv(
            INPUT_FILE,
            chunksize=CHUNKSIZE,
            on_bad_lines='skip',
            low_memory=True
        )
    except FileNotFoundError:
        print(f"Error: Input file not found at '{INPUT_FILE}'.", file=sys.stderr)