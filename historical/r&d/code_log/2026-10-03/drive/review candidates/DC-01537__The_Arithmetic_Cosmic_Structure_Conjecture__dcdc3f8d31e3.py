def parse_and_filter(csv_path, ra_bounds, dec_bounds):
    df = pd.read_csv(csv_path)
    df = df[(df['ra'] >= ra_bounds[0]) & (df['ra'] <= ra_bounds[1])]
    df = df[(df['dec'] >= dec_bounds[0]) & (df['dec'] <= dec_bounds[1])]
    return df
