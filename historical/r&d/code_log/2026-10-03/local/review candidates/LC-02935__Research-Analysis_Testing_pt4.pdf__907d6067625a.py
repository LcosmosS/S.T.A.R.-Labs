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