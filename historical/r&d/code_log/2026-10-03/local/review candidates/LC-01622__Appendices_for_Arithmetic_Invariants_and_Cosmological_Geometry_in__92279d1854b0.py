def process_data():
    processed_chunks = []
    total_rows_processed = 0
    try:
        chunk_iter = pd.read_csv(INPUT_FILE, usecols=REQUIRED_COLUMNS,
chunksize=CHUNKSIZE, on_bad_lines='skip', low_memory=True)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error reading input file: {e}", file=sys.stderr); return None

    for i, chunk in enumerate(chunk_iter):
        print(f"  - Processing chunk {i+1}...")
        chunk.replace(-9999, np.nan, inplace=True)
        chunk.dropna(subset=REQUIRED_COLUMNS, inplace=True)
        chunk = chunk[chunk['z'] > 0].copy()
        if chunk.empty: continue

        chunk['distance_mpc'] = chunk['z'].apply(calculate_distance_mpc)
        chunk['mass_sm'] = chunk['logmass'].apply(convert_logmass_to_sm)