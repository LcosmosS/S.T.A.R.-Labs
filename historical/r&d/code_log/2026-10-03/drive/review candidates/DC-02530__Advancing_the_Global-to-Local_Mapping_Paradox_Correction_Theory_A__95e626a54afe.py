def satisfies_heegner_hypothesis(E, D):
try:
D_fund = fundamental_discriminant(D)
if D_fund != D or D >= 0:
return False
N = E.conductor()
for p in N.prime_factors():
if kronecker_symbol(D, p) != 1:
return False
return True
except Exception as e:
print(f"Error checking Heegner hypothesis for D={D}: {e}")
return False
