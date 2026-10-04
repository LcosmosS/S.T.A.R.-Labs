prec = 200

Omega  = E.period_lattice().omega()
Reg    = E.gens()[0].height(precision=prec)
prod_c = E.tamagawa_product()

# Correct way to get analytic rank + leading term
ar_data = E.pari_curve().ellanalyticrank()
ar      = ar_data[0]
lead    = ar_data[1]          # this is L'(E,1) for rank 1

print("=== Final high-precision Strong BSD check ===")
print(f"Ω              = {Omega}")
print(f"Reg            = {Reg}")
print(f"∏ c_p          = {prod_c}")
print(f"Analytic rank  = {ar}")
print(f"L'(E,1)        = {lead}")
print(f"RHS (|Sha|=1)  = {Omega * Reg * prod_c}")
print(f"Implied |Sha|  = {lead / (Omega * Reg * prod_c)}")