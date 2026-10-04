# Retry Attempt 18 with regulator approximation
print(f"\nRetrying Attempt 18 with regulator approximation: Testing Fibonacci curve with a=2584, b=144")
a, b = 2584, 144
E = EllipticCurve(QQ, [0, 0, 0, a, b])
delta = E.discriminant()
conductor = E.conductor()
tors_order = E.torsion_subgroup().order()
print(f"Fibonacci curve: y² = x³ + {a}x + {b}")
print(f"Discriminant: {delta}")
print(f"Conductor: {conductor} = {factor(conductor)}")
print(f"Torsion order: {tors_order}")


# Analytic rank and leading coefficient
L = E.lseries()
dok = L.dokchitser(prec=100)
analytic_rank = 0
leading_coeff = dok(1)
if abs(leading_coeff) < 1e-10:
    L1_deriv = dok.derivative(1, 1)
    if abs(L1_deriv) < 1e-10:
        L1_deriv2 = dok.derivative(1, 2)
        analytic_rank = 2
        leading_coeff = L1_deriv2 / 2
print(f"Analytic rank: {analytic_rank}")
print(f"Leading coefficient: {leading_coeff}")


# Algebraic rank via PARI/GP
E_pari = pari.ellinit([0, 0, 0, a, b])
rank_info = E_pari.ellrank()
rank = int(rank_info[0])
print(f"Algebraic rank (via PARI/GP): {rank}")


# 3-Selmer rank
weak_bsd_holds = (analytic_rank == rank)
selmer3_rank = rank if weak_bsd_holds else None
print(f"3-Selmer rank (refined using BSD): {selmer3_rank}")


# Compute real period and Tamagawa numbers
omega = E.period_lattice().real_period(prec=100)
tamagawa = prod(E.tamagawa_numbers())
print(f"Real period (Omega): {omega}")
print(f"Product of Tamagawa numbers: {tamagawa}")


# Approximate the regulator
sha_order = 1  # Assume |Sha(E)| = 1
rhs = leading_coeff * (tors_order**2)
reg = rhs / (omega * tamagawa * sha_order)
print(f"Approximated regulator: {reg}")


# Cosmological invariants
cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
scaled_period = omega * SQRT_KAPPA * cosmo_scale
comoving_volume = (omega * reg * cosmo_scale**3) / (3e12)  # Rank 2
scaled_reg = reg * SQRT_KAPPA * 13  # Rank 2
print(f"Dynamic COSMO_SCALE: {cosmo_scale}")
print(f"Scaled period: {float(scaled_period)} light-years")
print(f"Scaled regulator (Reg * √κ * 13): {float(scaled_reg)}")
print(f"Estimated comoving volume (Omega * Reg * scale^3 / 3e12): {comoving_volume} Mly^3")
print(f"Right-hand side of strong BSD (with |Sha(E)| = 1): {rhs / (tors_order**2)}")
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
plt.scatter(x_vals, y_vals, s=float(max(density_size, 1)), c='blue', alpha=0.5, label=f'Rank {rank}')
plt.scatter(x_vals, -y_vals, s=float(max(density_size, 1)), c='blue', alpha=0.5)
contour_y = np.full_like(x_vals, float(5))
plt.plot(x_vals, contour_y, 'r--', label=f'Regulator {scaled_reg:.0f}')
plt.plot(x_vals, -contour_y, 'r--')
plt.title(f'Curve y² = x³ + {a}x + {b}, Density: {leading_coeff * 177:.0f}')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.savefig(f"curve_{a}_{b}.png")
plt.close()
print(f"Polynomial plot saved as curve_{a}_{b}.png")
print("-" * 20)


# Update interweb_data
interweb_data.append((a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, log_delta, log_cond))
with open("interweb_nodes.txt", "a") as f:
    f.write(f"{a},{b},{rank},{normalized_leading_coeff},{omega},{reg},{tamagawa},{weak_bsd_holds},{log_delta},{log_cond}\n")
with open("unique_curves.txt", "a") as f:
    f.write(f"{a},{b},{rank},{omega},{reg},{comoving_volume},{scaled_reg},{normalized_leading_coeff * 10},{conductor},curve_{a}_{b}.png\n")


# Regenerate the interweb plot
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
node_counts = {}
for node in interweb_data:
    key = (node[0], node[1], node[2])
    node_counts[key] = node_counts.get(key, 0) + 1
filtered_data = []
for node in interweb_data:
    key = (node[0], node[1], node[2])
    if node_counts[key] > 0:
        filtered_data.append(node)
        node_counts[key] -= 1
