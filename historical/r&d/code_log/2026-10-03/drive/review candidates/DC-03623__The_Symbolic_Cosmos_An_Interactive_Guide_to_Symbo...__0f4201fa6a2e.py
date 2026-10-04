   fib = [0, 1]
   for i in range(2, n + 1):
       fib.append(fib[i-1] + fib[i-2])
   return fib

def generate_candidate_curves(max_fib_index=20):
   """Generates a list of (a, b) pairs from Fibonacci numbers."""
   fib_numbers = generate_fibonacci(max_fib_index)
   candidate_pairs = []
   # Start from index 4 to avoid trivial/small numbers
   for i in range(4, len(fib_numbers)):
       for j in range(4, len(fib_numbers)):
           candidate_pairs.append((fib_numbers[i], fib_numbers[j]))
   # Add the foundational Virgo Cluster curve
   candidate_pairs.append((-1706, 6320))
   return candidate_pairs

# --- Block 3: Scaling Constants (defined early for use later) ---
VIRGO_DISTANCE = 54e6  # 54 million light-years
VIRGO_COMOVING_VOLUME = 1e9  # Mly^3
KAPPA = 1000
SQRT_KAPPA = math.sqrt(KAPPA)

# Foundational curve's real period (pre-calculated for calibration)
VIRGO_OMEGA = 0.42236269
# Master scaling constant derived from the Virgo Cluster benchmark
COSMO_SCALE = VIRGO_DISTANCE / (VIRGO_OMEGA * SQRT_KAPPA)

print("--- Starting Computational Pipeline ---")
print(f"Using COSMO_SCALE factor: {COSMO_SCALE}")

# --- Main Loop: Generation, Calculation, Validation, and Scaling ---
validated_curves_data = []
candidate_pairs = generate_candidate_curves()

for a, b in candidate_pairs:
   print(f"\n--- Analyzing Curve: y^2 = x^3 + {a}x + {b} ---")
   
   try:
       # --- Block 2: Calculation and Validation ---
       E = EllipticCurve(QQ, [a, b])
       
       if E.discriminant() == 0:
           print("Result: Singular curve. Skipping.")
           continue
       
       # Compute invariants
       rank = E.rank()
       tors_order = E.torsion_order()
       conductor = E.conductor()
       
       # Set a conductor limit to avoid extremely long computations
       if conductor > 1e12:
           print("Result: Conductor too large. Skipping.")
           continue
           
       omega = E.period_lattice().real_period()
       reg = E.regulator()
       tamagawa = prod(E.tamagawa_numbers())
       
       # Verify Weak BSD
       L = E.lseries()
       analytic_rank = L.analytic_rank()
       
       if rank != analytic_rank:
           print("Result: Weak BSD FAILED. Skipping.")
           continue
       else:
           print("Weak BSD Holds: Algebraic Rank = Analytic Rank =", rank)
           
       # Verify Strong BSD
       leading_coeff = L.derivative(1, rank) / factorial(rank)
       sha_order = 1  # Assume |Sha(E)| = 1 for simplicity
       rhs = (omega * reg * sha_order * tamagawa) / (tors_order**2)
       
       if abs(leading_coeff - rhs) > 1e-5:
           # If it fails, calculate the implied |Sha(E)|
           implied_sha = (leading_coeff * (tors_order**2)) / (omega * reg * tamagawa)
           print(f"Strong BSD FAILED: Left={leading_coeff:.4f}, Right={rhs:.4f}")
           print(f"Implied |Sha(E)|: {implied_sha:.4f}")
           continue
       else:
           print("Strong BSD Holds: Leading coefficient matches.")

       # --- Block 3: Scaling ---
       
       # Calculate Physical Distance
       scaled_period = omega * COSMO_SCALE
       print(f"Scaled Period: {scaled_period / 1e6:.2f} million light-years")
       
       # Calculate Density Height (with rank-dependent scaling)
       if rank == 0: reg_scale_factor = 1
       elif rank == 1: reg_scale_factor = 15
       elif rank == 2: reg_scale_factor = 12
       else: reg_scale_factor = 20
       scaled_regulator = reg * SQRT_KAPPA * reg_scale_factor
       print(f"Scaled Regulator (Density Height): {scaled_regulator:.2f}")
       
       # Estimate Comoving Volume (with rank-dependent denominator)
       if rank == 0: volume_denom = 1e13
       elif rank == 1: volume_denom = 5e12
       elif rank == 2: volume_denom = 3e12
       else: volume_denom = 3e11
       comoving_volume = (omega * reg * COSMO_SCALE**3) / volume_denom
       print(f"Estimated Comoving Volume: {comoving_volume:.2f} Mly^3")
       
       # Store validated data
       validated_curves_data.append({
           "a": a, "b": b, "rank": rank, "regulator": reg,
           "scaled_distance": scaled_period, "density_height": scaled_regulator,
           "comoving_volume": comoving_volume
       })
       print("Result: Curve VALIDATED and added to dataset.")
       
   except Exception as e:
       print(f"An error occurred: {e}. Skipping curve.")

print("\n--- Computational Pipeline Finished ---")
print(f"Total validated curves: {len(validated_curves_data)}")

# Optionally, print the final dataset
# for data in validated_curves_data:
#     print(data)
