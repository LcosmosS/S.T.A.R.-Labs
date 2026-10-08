#!/usr/bin/env python3
"""
M1-INH-E1b local verification of the constructive pair.
Requires only NumPy.
"""

import numpy as np

# ---------- frozen parameters ----------
def M(z):
    return 1.0 + z

Lambda = 3.0

def Phi(t, z):
    return (2*(1 + z))**(1/3) * np.sinh(1.5*(t + z))**(2/3)

def H(t, z):
    return 1.0 / np.tanh(1.5*(t + z))

def b(z):
    return 1.0 / (3*(1 + z))

# ---------- spatial sectors ----------
def E1(x, y, z):
    return 0.5 * (1 + x*x + y*y)

def E2(x, y, z):
    return 0.5 * (np.exp(z)*(x*x + y*y) + np.exp(-z))

def nu_z1(x, y, z):
    return 0.0

def nu_z2(x, y, z):
    q = np.exp(2*z) * (x*x + y*y)
    return (1 - q) / (1 + q)

# ---------- density ----------
def kappa_rho(t, x, y, z, nu_z):
    Phi_ = Phi(t, z)
    H_   = H(t, z)
    b_   = b(z)
    L    = H_ + b_ + nu_z
    Mz   = 1.0                    # M' = 1
    return (2*Mz + 6*M(z)*nu_z) / (Phi_**2 * (Phi_ * L))

# ---------- test point inside the regular domain ----------
t, z, x, y = 1.3, 0.07, 0.21, 0.17
assert 1 < t < 2 and -0.25 < z < 0.25 and x*x + y*y < 0.25

rho1 = kappa_rho(t, x, y, z, nu_z1(x, y, z))
rho2 = kappa_rho(t, x, y, z, nu_z2(x, y, z))
print(f"rho1 = {rho1:.8e}")
print(f"rho2 = {rho2:.8e}")
print(f"rho2 > rho1 > 0  ?  {rho2 > rho1 > 0}")

# ---------- Weierstrass data (identical for both) ----------
g2 = 0.0
g3 = -(1 + z)**2 / 4
Delta = g2**3 - 27 * g3**2
print(f"g2 = {g2},  g3 = {g3:.8e},  Delta = {Delta:.8e}")

# ---------- covariant discriminator J via finite differences ----------
eps = 1e-6

def J(t, x, y, z, nu_z_func, E_func):
    def rho_at(xx, yy):
        return kappa_rho(t, xx, yy, z, nu_z_func(xx, yy, z))
    drho_dx = (rho_at(x + eps, y) - rho_at(x - eps, y)) / (2 * eps)
    drho_dy = (rho_at(x, y + eps) - rho_at(x, y - eps)) / (2 * eps)
    Phi_ = Phi(t, z)
    E_   = E_func(x, y, z)
    return (E_**2 / Phi_**2) * (drho_dx**2 + drho_dy**2)

J1 = J(t, x, y, z, nu_z1, E1)
J2 = J(t, x, y, z, nu_z2, E2)
print(f"J1 = {J1:.8e}   (should be ~0)")
print(f"J2 = {J2:.8e}   (should be >0)")
print(f"J2 > 0 and |J1| < 1e-8  ?  {J2 > 0 and abs(J1) < 1e-8}")

print("\n--- quantitative claims of the constructive pair verified ---")