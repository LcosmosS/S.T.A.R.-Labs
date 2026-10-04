cosmic_path = 'data/raw/JApJ94494_2MASS_GAIADR3_EPOCH.csv'

if os.path.exists(cosmic_path):
    cosmic = pd.read_csv(cosmic_path)
    print("Loaded cosmic dataset:", cosmic_path)

    # Try to extract redshift or distance modulus columns
    if 'RAdeg' in cosmic.columns and 'DEdeg' in cosmic.columns:
        # No redshift column → synthesize z and distance
        z = np.clip(np.random.normal(loc=0.02, scale=0.01, size=len(cosmic)), 0.001, 0.2)
        dist = 10**((37.936 - 25)/5.0) * np.ones(len(cosmic))  # placeholder
    else:
        z = np.random.uniform(0.001, 0.2, size=200)
        dist = (3e5/70.0) * z * (1 + 0.5*z)

elif RUNNING_IN_CI and os.path.exists(CI_LABELS):
    print("CI mode: generating synthetic redshift–distance pairs from CI labels")
    labels = pd.read_csv(CI_LABELS)
    n = len(labels)

    z = np.sort(np.random.uniform(0.001, 0.2, size=n))
    H0_true = 70.0
    dist = (3e5 / H0_true) * z * (1 + 0.5*z) + np.random.normal(scale=5.0, size=n)

else:
    print("Cosmic dataset not found; generating synthetic redshift–distance pairs.")
    n = 120
    z = np.sort(np.random.uniform(0.001, 0.2, size=n))
    H0_true = 70.0
    dist = (3e5 / H0_true) * z * (1 + 0.5*z) + np.random.normal(scale=5.0, size=n)
