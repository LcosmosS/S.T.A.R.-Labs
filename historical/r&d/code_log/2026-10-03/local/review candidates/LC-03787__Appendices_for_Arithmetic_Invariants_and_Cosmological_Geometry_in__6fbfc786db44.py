    chunk.replace(-9999, np.nan, inplace=True)

    key_cols = ['z', 'Fg', 'Fr', 'Fz', 'EBV', 'plx', 'pmRA', 'pmDE']

    chunk.dropna(subset=key_cols, inplace=True)

    chunk = chunk[(chunk['Fg'] > 0) & (chunk['Fr'] > 0) & (chunk['Fz'] > 0)]



    chunk['flux_gr'] = chunk['Fg'] / chunk['Fr']

    chunk['flux_rz'] = chunk['Fr'] / chunk['Fz']

    chunk['log_EBV'] = np.log(chunk['EBV'] + 1e-6)

    chunk['pm_mag'] = np.sqrt(chunk['pmRA']**2 + chunk['pmDE']**2)



    return chunk



# Load full CSV in chunks

df_list = []

for chunk in pd.read_csv("1760769987443A.csv", chunksize=chunksize):

    processed = process_chunk(chunk)

    if not processed.empty:

        df_list.append(processed)

df = pd.concat(df_list, ignore_index=True)

print("Processed Data Info:", df.info())
