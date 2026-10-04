    print("Weak BSD fails: Algebraic rank != Analytic rank")

# Compute BSD invariants for strong BSD
omega = E.period_lattice().real_period(prec=100)
# Compute the regulator, handling rank 0 case
if rank == 0:
    reg = 1.0  # Regulator is 1 for rank 0
else:
    reg = E.regulator()  # Remove prec parameter
tamagawa = prod(E.tamagawa_numbers())
sha_order = 1  # Initial hypothesis based on 2-Selmer rank

# Compute the right-hand side of the strong BSD formula
rhs = (omega * reg * sha_order * tamagawa) / (tors_order^2)
print(f"Real period (Omega): {omega}")
print(f"Regulator: {reg}")
print(f"Product of Tamagawa numbers: {tamagawa}")
print(f"Right-hand side of strong BSD (with |Sha(E)| = 1): {rhs}")

# Verify strong BSD
if abs(leading_coeff - rhs) < 1e-10:
    print("Strong BSD holds: Leading coefficient matches with |Sha(E)| = 1")
else:
    print("Strong BSD fails: Leading coefficient does not match with |Sha(E)| = 1")
    # Adjust Sha(E) to match
    sha_order = (leading_coeff * tors_order^2) / (omega * reg * tamagawa)
    print(f"Adjusted |Sha(E)| to match: {sha_order}")
