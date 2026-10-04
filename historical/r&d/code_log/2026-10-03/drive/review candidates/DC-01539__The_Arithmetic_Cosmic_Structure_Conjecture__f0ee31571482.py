def phi_star(row):
    return np.array([
        np.log10(row['delta']),
        np.log10(row['conductor']),
        np.log10(row['regulator']),
        row['rank'],
        row['torsion_order']
