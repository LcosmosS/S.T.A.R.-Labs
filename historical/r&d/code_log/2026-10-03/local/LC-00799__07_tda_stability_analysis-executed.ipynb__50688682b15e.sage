try:
    from src.tda.persistence_landscape import PersistenceLandscape
    from src.tda.bootstrap_stability import BootstrapStability

    PL = PersistenceLandscape(resolution=200)
    BS = BootstrapStability(num_bootstrap=20, resolution=200)

    barcodes = diagrams if diagrams is not None else []
    landscape = PL.landscape(barcodes[1] if len(barcodes) > 1 else [])

    np.save('results/tda_landscape.npy', landscape)
    print("Saved results/tda_landscape.npy")

except Exception as e:
    print("Persistence landscape/bootstrap modules not available; skipping.", e)
