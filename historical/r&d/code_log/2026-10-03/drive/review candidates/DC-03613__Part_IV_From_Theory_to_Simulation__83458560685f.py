# Inside a loop iterating through candidate_pairs
a, b = pair
E = EllipticCurve(QQ, [a, b])

# Check for singularity
if E.discriminant() == 0:
   continue

# Compute invariants
rank = E.rank()
tors_order = E.torsion_order()
conductor = E.conductor()
omega = E.period_lattice().real_period()
reg = E.regulator()
tamagawa = prod(E.tamagawa_numbers())

# Verify Weak BSD
L = E.lseries()
analytic_rank = L.analytic_rank()
if rank!= analytic_rank:
   print(f"Weak BSD fails for a={a}, b={b}")
   continue

# Verify Strong BSD
leading_coeff = L.derivative(1, rank) / factorial(rank)
sha_order = 1  # Assume |Sha(E)| = 1 for simplicity
rhs = (omega * reg * sha_order * tamagawa) / (tors_order**2)

if abs(leading_coeff - rhs) > 1e-5:
   print(f"Strong BSD fails for a={a}, b={b}")
   continue
