    chunk['generator_coords'] = chunk['log_delta'].apply(lambda x: (x, x*2) if not pd.isna(x) else np.nan)
    chunk['generator_structure'] = chunk['generator_coords'].apply(analyze_generator_structure)
    summary = {'Rows Processed': len(chunk)}
    print_step(20, f"process_chunk (Chunk {chunk_idx+1}/{total_chunks})", summary)
    return chunk


# --- 21. Cohomology Processing Function --- 
def process_cohomology(chunk, chunk_idx, total_chunks):
    print_step(21, f"process_cohomology (Chunk {chunk_idx+1}/{total_chunks})")
    chunk, betti_1, summary = compute_cohomology(chunk)
    print_step(21, f"process_cohomology (Chunk {chunk_idx+1}/{total_chunks})", summary)
    return chunk, betti_1


# --- 22. Main Processing --- 
def main(): 
    print_step(1, "Configuration")
    print_step(2, "Imports")
    print_step(22, "Main Processing")
    df = pd.read_csv(INPUT_FILE)
    df = df[REQUIRED_COLUMNS].iloc[:ROW_LIMIT]
    df[['logmass', 'metallicity']] = df[['logmass', 'metallicity']].replace(-9999, np.nan)
    summary = {'Initial Rows': len(df), 'NaN Counts': df[['logmass', 'metallicity']].isna().sum().to_dict()}
    print_step(22, "Data Loading", summary)


    print_step(20, "Chunk Processing")
    chunks = [df[i:i+CHUNKSIZE] for i in range(0, len(df), CHUNKSIZE)]
    total_chunks = len(chunks)
    with mp.Pool(processes=3) as pool:
        df_list = pool.starmap(process_chunk, [(chunk, idx, total_chunks) for idx, chunk in enumerate(chunks)])
    df = pd.concat(df_list, ignore_index=True)
    gc.collect()
    summary = {'Total Rows Processed': len(df), 'Chunks Processed': total_chunks}
    print_step(20, "Chunk Processing", summary)


    print_step(21, "Cohomology Processing")
    chunks = [df[i:i+CHUNKSIZE] for i in range(0, len(df), CHUNKSIZE)]
    with mp.Pool(processes=3) as pool:
        results = pool.starmap(process_cohomology, [(chunk, idx, total_chunks) for idx, chunk in enumerate(chunks)])
    df_list = [res[0] for res in results]
    betti_1_vals = [res[1] for res in results]
