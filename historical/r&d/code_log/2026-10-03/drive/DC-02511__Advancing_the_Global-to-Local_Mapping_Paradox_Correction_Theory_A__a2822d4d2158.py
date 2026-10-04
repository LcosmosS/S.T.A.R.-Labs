if twist_d:
E_curve = E_twist
else:
E_curve = E
points = E_curve.gens()
if points:
regulator = E_curve.regulator(points)
print(f"Regulator: {regulator}")
else:
print("No points found for regulator computation")
except Exception as e:
print(f"Regulator computation failed: {e}")
try:
L = E.lseries()
dok = L.dokchitser(prec=50)
L1 = dok(1)
leading_coeff = L1
if abs(L1) < 1e-5:
for n in range(1, 5):
L_deriv = dok.derivative(1, n)
if abs(L_deriv) < 1e-5:
continue
analytic_rank = n
leading_coeff = L_deriv / math.factorial(n)
break
print(f"Leading coefficient: {leading_coeff}")
except Exception as e:
print(f"L-series computation failed: {e}")
leading_coeff = None
try:
omega = E.period_lattice().real_period(prec=50)
tamagawa = prod(E.tamagawa_numbers())
sha_order = 1
rhs = leading_coeff * (tors_order**2) if leading_coeff is not None else 0
reg = rhs / (omega * tamagawa * sha_order) if analytic_rank and analytic_rank > 0 and leading_coeff else 1.0
except Exception as e:
print(f"BSD invariants computation failed: {e}")
omega, tamagawa, reg = None, None, None
log_delta = math.log(abs(delta)) if delta != 0 else 0
log_cond = math.log(float(conductor)) if conductor > 0 else 0
longitude = (log_delta / 10.0) * 180 if log_delta != 0 else 0
longitude = max(min(longitude, 180), -180)
latitude = (log_cond / 10.0) * 90 if log_cond != 0 else 0
latitude = max(min(latitude, 90), -90)
elevation = analytic_rank * 200.0 if analytic_rank is not None else 0
elevation = min(elevation, 1000)
cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA) if omega else 0
raw_volume = omega * reg * cosmo_scale**3 if omega and reg else 0
size = math.log1p(raw_volume) / 1e13 if raw_volume > 0 else 0
size = max(min(size * 100, 10), 0.1)
scaled_period = omega * cosmo_scale if omega else 0
denominator = {0: 1e13, 1: 1e15, 2: 5e13, 3: 3e11}.get(analytic_rank, 1e13) if analytic_rank is not None else 1e13
comoving_volume = math.log1p(raw_volume) / denominator if raw_volume > 0 else raw_volume / denominator
reg_factor = 20 - 5 * analytic_rank if analytic_rank is not None and analytic_rank <= 3 else 10
scaled_reg = reg * SQRT_KAPPA * reg_factor if reg else 0
print(f"Real period (Omega): {omega}")
print(f"Dynamic COSMO_SCALE: {cosmo_scale}")
print(f"Scaled period: {float(scaled_period)} light-years")
print(f"Regulator: {reg}")
print(f"Scaled regulator: {float(scaled_reg)}")
print(f"Product of Tamagawa numbers: {tamagawa}")
print(f"Estimated comoving volume: {comoving_volume} Mly^3")
print(f"Earth mapping: Longitude={longitude}°, Latitude={latitude}°, Elevation={elevation}m, Size={size}")
weak_bsd_holds = (analytic_rank == algebraic_rank) if analytic_rank is not None and algebraic_rank is not None else False
print(f"Weak BSD holds: {weak_bsd_holds}")
try:
plt.figure()
plot = E.plot(xmin=-5, xmax=5, ymin=-10, ymax=10)
plt.title(f"Elliptic Curve y^2 = x^3 + {a}x + {b}")
plt.grid(True)
plt.savefig(f"curve_a{a}_b{b}.png")
plt.close()
print(f"Plot saved as curve_a{a}_b{b}.png")
except Exception as e:
print(f"Plotting failed: {e}")
features = [a, b, log_delta, log_cond, tors_order]
return True, features, analytic_rank, leading_coeff / 10 if leading_coeff else 0, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size
except Exception as e:
print(f"Error analyzing curve: {e}")
return False, None, None, None, None, None, None, False, None, None, None, None, None, None
