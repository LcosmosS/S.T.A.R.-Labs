print("Notebook: 07_tda_stability_analysis")
print(
    "Data source:",
    (
        "projection_points.csv"
        if os.path.exists("results/projection_points.csv")
        else "CI labels" if RUNNING_IN_CI else "synthetic"
    ),
)
print(
    "Outputs: results/tda_landscape.npy, results/persistence_landscape.png (if computed)"
)