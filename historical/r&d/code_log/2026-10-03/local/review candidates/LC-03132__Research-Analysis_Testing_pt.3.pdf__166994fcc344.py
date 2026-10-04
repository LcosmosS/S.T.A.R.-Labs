        reg = E.regulator() if rank > 0 else 1.0
        tamagawa = prod(E.tamagawa_numbers())
        sha_order = 1  # Initial hypothesis
        rhs = (omega * reg * sha_order * tamagawa) / (tors_order**2)
        print(f"Real period (Omega): {omega}")
        print(f"Regulator: {reg}")
        print(f"Product of Tamagawa numbers: {tamagawa}")
        print(f"Right-hand side of strong BSD (with |Sha(E)| = 1): {rhs}")

        # Verify strong BSD
        if abs(leading_coeff - rhs) < 1e-10:
            print("Strong BSD holds: Leading coefficient matches with |Sha(E)| = 1")
        else:
            print("Strong BSD fails: Leading coefficient does not match with |Sha(E)| = 1")
            sha_order = (leading_coeff * tors_order**2) / (omega * reg * tamagawa)
            print(f"Adjusted |Sha(E)| to match: {sha_order}")
    except:
        print("Failed to compute BSD invariants")

    print("-" * 20)

# Example calls
fib_pairs = [(5, 13), (8, 21), (13, 34)]
for a, b in fib_pairs:
    analyze_curve(a, b)

analyze_curve(-1706, 6320, is_original=True)
