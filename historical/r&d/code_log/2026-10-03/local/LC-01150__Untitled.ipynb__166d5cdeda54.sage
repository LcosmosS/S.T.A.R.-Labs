pari.default('realprecision', 60)

E = pari.ellinit([-1706, 6320])

# Torsion
tors = E.elltors()
print("Torsion:", tors)

# Global reduction & Tamagawa product
gr = E.ellglobalred()
print("Conductor N =", gr[0])
print("Tamagawa product =", gr[2])          # this is the reliable way

# Analytic rank and L'(E,1)
ar = E.ellanalyticrank()
print("Analytic rank =", ar[0])
print("L'(E,1)       =", ar[1])

# Real period – two conventions shown
periods = E.ellperiods()
half_period = periods[0]                     # PARI’s default (≈ 0.42236)
full_period = 2 * half_period                # Sage-style real period (≈ 0.84473)
print("PARI half-period Ω =", half_period)
print("Full real period Ω =", full_period)

# Generator and regulator (manual, because ellgenerators needs elldata)
P = [2, 54]
reg = E.ellheight(P)
print("Regulator (height of (2,54)) =", reg)

# 2-Selmer (if available in your PARI build)
try:
    sel = E.ellselmer(2) 
    print("2-Selmer rank =", len(sel))
except Exception as e:
    print("ellselmer not available or failed:", e)
    print("(You already know from Sage two_descent that the 2-Selmer rank is 1)")