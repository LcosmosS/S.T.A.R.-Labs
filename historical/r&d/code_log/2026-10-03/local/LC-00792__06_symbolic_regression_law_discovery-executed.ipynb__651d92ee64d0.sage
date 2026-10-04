if os.path.exists('results/projection_points.csv'):
    df = pd.read_csv('results/projection_points.csv')
    X = df[['x','y','z']].values
    y = df['x']*0.5 + df['z']*0.1 + np.random.normal(scale=0.1, size=len(df))
    print("Loaded projection_points.csv")

elif RUNNING_IN_CI and os.path.exists(CI_LABELS):
    print("CI mode: synthesizing regression dataset from CI labels")
    labels = pd.read_csv(CI_LABELS)
    n = len(labels)
    X = np.random.rand(n,3)
    y = X[:,0]*0.5 + X[:,2]*0.1 + np.random.normal(scale=0.1, size=n)

else:
    print("Projection points not found; generating synthetic dataset.")
    n = 120
    X = np.random.rand(n,3)
    y = X[:,0]*0.5 + X[:,2]*0.1 + np.random.normal(scale=0.1, size=n)
