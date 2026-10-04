# 3. Define S.T.A.R. Model

H_expr = "H0*sqrt(max(Ωm*(1+z)**3 + ΩΛ + a*z + b*z**2, 1e-12))"
param_names = ["H0", "Ωm", "ΩΛ", "a", "b"]

priors = {
    "H0": (72, 5),      
    "Ωm": (0.3, 0.08),
    "ΩΛ": (0.7, 0.08),
    "a": (-0.05, 0.05), 
    "b": (0, 0.05),
}

proposal_widths = {
    "H0": 0.1,
    "Ωm": 0.01,
    "ΩΛ": 0.01,
    "a": 0.002,
    "b": 0.002,
}
# === DEBUG: Check Data & Initial Posterior ===
print("Type of PANTHEON_PLUS_FULL:", type(PANTHEON_PLUS_FULL))
df_sn = pd.DataFrame(PANTHEON_PLUS_FULL)
print("DataFrame shape:", df_sn.shape)
print("Columns:", df_sn.columns.tolist())
print("First 5 z values:", df_sn["z"].head().tolist())

# Check likelihood at starting point
theta0 = np.array([70.0, 0.300, 0.700, 1e-4, 1e-4])

print("\n=== Initial Log-Posterior Check ===")
print("theta0 =", theta0)

try:
    logp = joint_2015(theta0)
    print(f"joint_2015(theta0) = {logp}")
except Exception as e:
    print(f"joint_2015 ERROR: {e}")

try:
    logp = joint_2018(theta0)
    print(f"joint_2018(theta0) = {logp}")
except Exception as e:
    print(f"joint_2018 ERROR: {e}")

print("joint_2015(theta0) =", joint_2015(theta0))
print("joint_2018(theta0) =", joint_2018(theta0))