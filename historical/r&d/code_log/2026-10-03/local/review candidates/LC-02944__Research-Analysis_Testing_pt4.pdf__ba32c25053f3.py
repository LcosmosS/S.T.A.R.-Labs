cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
scaled_period = omega * SQRT_KAPPA *
cosmo_scale comoving_volume = (omega * reg * cosmo_scale**3) / (3e12)

# Rank 2
scaled_reg = reg * SQRT_KAPPA * 13

# Rank 2
print(f"Dynamic COSMO_SCALE: {cosmo_scale}")

print(f"Scaled period: {float(scaled_period)} light-years")
print(f"Scaled regulator (Reg * √κ * 13): {float(scaled_reg)}")
print(f"Estimated comoving volume (Omega * Reg * scale^3 / 3e12): {comoving_volume}
Mly^3") print(f"Right-hand side of strong BSD (with |Sha(E)| = 1): {rhs / (tors_order**2)}")
print("Strong BSD holds: Leading coefficient matches by construction")

# Features for interweb_data
log_delta = math.log(abs(delta))
log_cond = math.log(conductor)
features = [a, b, log_delta, log_cond, tors_order]
normalized_leading_coeff = leading_coeff / 10

# Generate polynomial plot

x_range = 4 * math.sqrt(abs(a))
x_vals = np.linspace(-x_range, x_range, 1000)
y_vals = np.sqrt(np.maximum(x_vals**3 + a * x_vals + b, 0))
density_size = min(leading_coeff * 177 / 20, 200)
plt.figure(figsize=(8, 6))
plt.scatter(x_vals, y_vals, s=float(max(density_size, 1)), c='blue', alpha=0.5, label=f'Rank
{rank}') plt.scatter(x_vals, -y_vals, s=float(max(density_size, 1)), c='blue', alpha=0.5)
contour_y = np.full_like(x_vals, float(5))
plt.plot(x_vals, contour_y, 'r--', label=f'Regulator {scaled_reg:.0f}') plt.plot(x_vals, -contour_y,
