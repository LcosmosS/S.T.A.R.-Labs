def generate_synthetic_universe(num_galaxies, entropy_profile):
positions = np.random.rand(num_galaxies, 3)
masses = np.random.choice(entropy_profile, num_galaxies)
return positions, masses
positions, masses = generate_synthetic_universe(10000, [symbolic_entropy])
