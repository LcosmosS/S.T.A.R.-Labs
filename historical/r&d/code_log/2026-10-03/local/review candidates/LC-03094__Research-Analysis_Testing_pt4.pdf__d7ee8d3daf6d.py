    delta = compute_discriminant(a, b)
    if delta == 0:
        print(f"Discriminant is 0 for a={a}, b={b}, skipping curve")
        attempt += 1

        continue
