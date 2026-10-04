# Find the generator(s) of the free part of the Mordell-Weil group
generators = E.gens()
print(generators)

# Compute the L-series associated with E
L = E.lseries()

# Compute the value of L(E,s) at s=1
L_value_at_1 = L(1)
print(L_value_at_1)

# Compute the value of the first derivative L'(E,s) at s=1
L_derivative_at_1 = L.dokchitser().derivative(1, 1)
print(L_derivative_at_1)

# Re-compute L'(E,1) with higher precision
L_derivative_high_precision = E.lseries().dokchitser(prec=100).derivative(1, 1)
print(L_derivative_high_precision)

# Compute the real period with higher precision
omega_high_precision = E.period_lattice().real_period(prec=100)
print(omega_high_precision)

# Compute the regulator with higher precision
P = E.gens()[0]
regulator_high_precision = P.height(precision=100)
print(regulator_high_precision)

# Compute the product of the Tamagawa numbers
tamagawa_product = prod(E.tamagawa_numbers())
print(tamagawa_product)

# Perform a verbose 2-descent to analyze the 2-Selmer group
E.two_descent(verbose=True)
