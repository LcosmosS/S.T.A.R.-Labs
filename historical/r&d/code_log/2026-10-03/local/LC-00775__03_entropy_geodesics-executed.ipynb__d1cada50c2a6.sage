if os.path.exists('results/projection_points.csv'):
    df = pd.read_csv('results/projection_points.csv')
    print("Loaded results/projection_points.csv")

elif RUNNING_IN_CI and os.path.exists(CI_LABELS):
    print("CI mode: synthesizing projection points from CI labels")
    labels = pd.read_csv(CI_LABELS)
    n = len(labels)
    df = pd.DataFrame({
        'x': np.random.rand(n),
        'y': np.random.rand(n),
        'z': np.random.rand(n)
    })

else:
    print("Projection points not found; generating synthetic points.")
    n = 150
    df = pd.DataFrame({
        'x': np.random.randint(0,4,size=n),
        'y': np.random.lognormal(5,1.0,size=n),
        'z': np.random.exponential(1.0,size=n)
    })

points = df[['x','y','z']].values
