leading_coeff = L1_deriv2 / 2
else:
analytic_rank = 1
leading_coeff = L1_deriv
else:
analytic_rank = 0
leading_coeff = L1
print(f"Analytic rank: {analytic_rank}")
print(f"Leading coefficient L^{(r)}(E, 1): {leading_coeff}")
# Verify weak BSD
if rank == analytic_rank:
print("Weak BSD holds: Algebraic rank = Analytic rank")
else:
print("Weak BSD fails: Algebraic rank != Analytic rank")
# Use Heegner points to construct rational points (Euler system
