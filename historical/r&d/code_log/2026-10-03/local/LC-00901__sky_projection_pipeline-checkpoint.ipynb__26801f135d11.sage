# 3. Load Real Galaxy Data for Overlay
galaxy_paths = [
    ROOT / "data" / "cosmic" / "DESIDR8_SDSSDR16_SIMBAD.csv",
    ROOT / "data" / "cosmic" / "JApJ94494_2MASS_GAIADR3_EPOCH.csv",
    # Add more paths if you have other catalogs
]

galaxies = None
for path in galaxy_paths:
    if path.exists():
        galaxies = pd.read_csv(path)
        print(f" Loaded {len(galaxies)} real galaxies from {path.name}")
        break

if galaxies is None:
    print(" No galaxy catalog found. Generating synthetic galaxies.")
    np.random.seed(42)
    galaxies = pd.DataFrame({
        'ra': np.random.uniform(0, 360, 5000),
        'dec': np.random.uniform(-90, 90, 5000),
        'z': np.random.lognormal(0, 0.6, 5000).clip(0.01, 2.5),
        'logM': np.random.normal(10.5, 0.8, 5000)
    })