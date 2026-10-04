print("Notebook: 05_hubble_tension_fit")
print(
    "Data used:",
    (
        cosmic_path
        if os.path.exists(cosmic_path)
        else "CI labels" if RUNNING_IN_CI else "synthetic"
    ),
)
print("Outputs: results/hubble_fit.png, results/hubble_fit_summary.json")