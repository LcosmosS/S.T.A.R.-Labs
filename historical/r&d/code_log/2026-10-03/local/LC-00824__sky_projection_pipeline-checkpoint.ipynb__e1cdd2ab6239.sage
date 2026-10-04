# 4. Generate Arithmetic Cloud & Project
np.random.seed(42)
n_samples = 8000

arithmetic_data = {
    "delta": np.random.lognormal(0, 1.8, n_samples),
    "conductor": np.random.lognormal(4, 2.2, n_samples),
    "rank": np.random.randint(0, 5, n_samples),
    "regulator": np.random.lognormal(0, 1.4, n_samples),
}

projector = ArithmeticProjector(Amax=1.0, Nmax=1.0, V0=1.0)

print("Projecting arithmetic invariants to cosmic manifold...")
arithmetic_cloud = projector.project(arithmetic_data)
embedded = projector.embed_to_cosmic(arithmetic_cloud)

print(f"Projection completed. Embedded shape: {embedded.shape}")