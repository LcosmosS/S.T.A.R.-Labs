            print(f"Right-hand side of strong BSD (with |Sha(E)| = 1): {rhs}")

            if abs(leading_coeff - rhs) < 1e-10:
                print("Strong BSD holds: Leading coefficient matches with |Sha(E)| = 1")
            else:
                print("Strong BSD fails: Leading coefficient does not match with |Sha(E)| = 1")
                sha_order = (leading_coeff * tors_order**2) / (omega * reg * tamagawa)
                print(f"Adjusted |Sha(E)| to match: {sha_order}")
        except Exception as e:
            print(f"Failed to compute BSD invariants: {e}")
            return False, None, None, None, None, None, None, False, E

    log_delta = math.log(abs(delta)) if delta != 0 else 0
    log_cond = math.log(conductor) if conductor > 0 else 0
    features = [a, b, log_delta, log_cond, tors_order]
    normalized_leading_coeff = leading_coeff / 10 if leading_coeff else 0

    # Enhanced polynomial plot
    if success and rank is not None:
        try:
            x_range = 2 * math.sqrt(abs(a)) if abs(a) > 1 else 10
            x_vals = np.linspace(-x_range, x_range, 1000)
            y_vals = np.sqrt(np.maximum(x_vals**3 + a * x_vals + b, 0))
            density_size = (leading_coeff * 177 / 100) if leading_coeff else 10  # Map to ~6320
