print("Notebook: 03_entropy_geodesics")
print(
    "Data source:",
    (
        "projection_points.csv"
        if os.path.exists("results/projection_points.csv")
        else "CI labels" if RUNNING_IN_CI else "synthetic"
    ),
)
print("Outputs: results/geodesics.npy, results/geodesics_overlay.png")