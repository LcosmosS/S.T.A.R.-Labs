# We exclude the raw proxies (like flux_gr) and focus on the physical variables
sym_features = [
    'normalized_density',
    'local_betti_1',
    'local_betti_2',
    'T_cosmo',
    'Anthropic'
]

X_sym = complex_web[sym_features]
y_sym = complex_web['persistence_entropy']

# 3. Configure the PySR Regressor
# We give it basic operators to see if an Euler-like characteristic emerges naturally
pysr_model = PySRRegressor(
    niterations=40,
    binary_operators=["+", "*", "-", "/"],
    unary_operators=["exp", "inv(x) = 1/x"],
    extra_sympy_mappings={"inv": lambda x: 1/x},
    loss="loss(prediction, target) = (prediction - target)^2",
    model_selection="best",
    random_state=42
)

# 4. Fit the model
pysr_model.fit(X_sym, y_sym)

print("\n--- Top Candidate Equations ---")
print(pysr_model.sympy())

# --- REFINED HISTOGRAM ---
print("\n Histogram of log(discovered constants)...")
# Constants from your Complexity 11 Equation (β=16.26, offset=1.35, etc.)
constants = [16.263, np.sqrt(1.5), 1.2209, 16.183, 1.352]
plt.figure(figsize=(8, 5))
plt.hist(np.log(np.abs(constants) + 1e-8), bins=10, color='darkgreen', alpha=0.7)
plt.title("Log-Spectral Distribution of Discovered Constants")
plt.xlabel("log(|constant|)")
plt.ylabel("Frequency")
plt.grid(axis='y', alpha=0.3)
plt.show()

print("\n S.T.A.R. Pipeline Complete. Visualization and Foliation test saved.")