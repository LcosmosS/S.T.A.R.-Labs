print("Notebook: 06_symbolic_regression_law_discovery")
print(
    "Data source:",
    (
        "projection_points.csv"
        if os.path.exists("results/projection_points.csv")
        else "CI labels" if RUNNING_IN_CI else "synthetic"
    ),
)
print("Outputs: results/sr_predictions.csv")