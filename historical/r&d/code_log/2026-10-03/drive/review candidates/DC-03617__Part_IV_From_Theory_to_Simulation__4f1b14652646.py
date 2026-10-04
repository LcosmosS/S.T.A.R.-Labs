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
