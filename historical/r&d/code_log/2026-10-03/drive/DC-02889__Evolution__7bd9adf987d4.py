import sympy as sp


r, R, Omega, T, alpha = sp.symbols('r R Omega T alpha')


# Regulator as det(height matrix), dimensional ~ h^r
# ψ normalizes by triangular exponent for matrix complexity
psi = r * (r + 1) / 2


# Generalized volume law: V = (Omega * R^(1/r) * alpha^r) / T * sp.exp(-psi)
V = (Omega * R**(1/r) * alpha**r) / T * sp.exp(-psi)


print("Universal ψ(r):", psi)
print("Invariant Volume Law:", V.simplify())
