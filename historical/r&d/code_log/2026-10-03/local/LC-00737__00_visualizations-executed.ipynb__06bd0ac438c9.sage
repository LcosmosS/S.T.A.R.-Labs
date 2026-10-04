if os.path.exists('results/projection_points.csv'):
    df = pd.read_csv('results/projection_points.csv')
    X = df[['x','y','z']].values
else:
    X = np.random.rand(300,3)

print("Loaded", X.shape[0], "projection points")
