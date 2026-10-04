if os.path.exists("results/projection_points.csv"):
    df = pd.read_csv("results/projection_points.csv")
    points = df[["x", "y", "z"]].values
    print("Loaded results/projection_points.csv")

elif RUNNING_IN_CI and os.path.exists(CI_LABELS):
    print("CI mode: synthesizing projection points from CI labels")
    labels = pd.read_csv(CI_LABELS)
    n = len(labels)
    df = pd.DataFrame(
        {"x": np.random.rand(n), "y": np.random.rand(n), "z": np.random.rand(n)}
    )
    points = df[["x", "y", "z"]].values

else:
    print("Projection points not found; generating synthetic points.")
    points = np.random.rand(200, 3)