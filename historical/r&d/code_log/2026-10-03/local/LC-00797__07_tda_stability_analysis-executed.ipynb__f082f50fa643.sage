if os.path.exists('results/projection_points.csv'):
    df = pd.read_csv('results/projection_points.csv')
    X = df[['x','y','z']].values
    print("Loaded results/projection_points.csv")

elif RUNNING_IN_CI and os.path.exists(CI_LABELS):
    print("CI mode: synthesizing projection points from CI labels")
    labels = pd.read_csv(CI_LABELS)
    n = len(labels)
    X = np.random.rand(n,3)

else:
    print("Projection points not found; generating synthetic points.")
    X = np.random.rand(150,3)

print("Points shape:", X.shape)
