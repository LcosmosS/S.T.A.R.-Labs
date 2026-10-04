print("Notebook: 02_entropy_field_demo")
print(
    "Data used:",
    (
        "projection_points.csv"
        if os.path.exists("results/projection_points.csv")
        else "CI labels" if RUNNING_IN_CI else "synthetic"
    ),
)
print(
    "Outputs: results/entropy_summary.csv, results/entropy_hist.png, results/entropy_quiver.png"
)