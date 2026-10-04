    logmass = df['logmass']
    z = df['z']
    features = pd.DataFrame({
        'logmass': logmass,
        'z': z,
        'logmass2': logmass**2,
        'z2': z**2,
        'logmass_z': logmass * z,
        'quenching': np.maximum(logmass - high_mass_threshold, 0),
        'low_mass': (logmass < low_mass_threshold) * logmass
    })
    # Include additional features if available
    for feat in ['metallicity', 'environment']:
        if feat in df.columns:
            features[feat] = df[feat]
    return features


def main():
    # Load dataset
    csv_file = 'Stellar_Mass2_Table_cleaned.csv'
    try:
        df = pd.read_csv(csv_file)
        print(f"Loaded '{csv_file}' successfully.")
    except FileNotFoundError:
        print(f"Error: '{csv_file}' not found.")
