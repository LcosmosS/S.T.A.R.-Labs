pd.set_option('mode.chained_assignment', None)

os.makedirs("visualizations", exist_ok=True)

chunksize = 10000



# Process chunk

def process_chunk(chunk):

    chunk = chunk.copy()

    chunk.replace(-9999, np.nan, inplace=True)

    key_cols = ['z', 'Fg', 'Fr', 'Fz', 'EBV', 'plx', 'pmRA', 'pmDE', 'Chi2', 'delChi2', 'TSNR2_ELG',
'TSNR2_LRG', 'Morph', 'OType']

    chunk = chunk.dropna(subset=key_cols)

    chunk = chunk[(chunk['Fg'] > 0) & (chunk['Fr'] > 0) & (chunk['Fz'] > 0)]



    coeff_cols = [col for col in chunk.columns if col.startswith('COEFF')]

    if coeff_cols:

        chunk['coeff_sum'] = chunk[coeff_cols].sum(axis=1)

        chunk['coeff_mean'] = chunk[coeff_cols].mean(axis=1)



    chunk['flux_gr'] = chunk['Fg'] / chunk['Fr']

    chunk['flux_rz'] = chunk['Fr'] / chunk['Fz']

    chunk['log_EBV'] = np.log(chunk['EBV'] + 1e-6)