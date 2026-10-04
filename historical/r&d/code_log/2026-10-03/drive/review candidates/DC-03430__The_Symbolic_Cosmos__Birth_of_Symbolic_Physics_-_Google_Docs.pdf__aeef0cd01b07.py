L1_deriv2 = dok.derivative(1, 2)
analytic_rank = 2
leading_coeff = L1_deriv2 / 2
else:
analytic_rank = 1
leading_coeff = L1_deriv
except:
analytic_rank = 2
leading_coeff = 0
else:
analytic_rank = 0
leading_coeff = L1
print(f"Analytic rank: {analytic_rank}")
print(f"Leading coefficient: {leading_coeff} (topological density in
