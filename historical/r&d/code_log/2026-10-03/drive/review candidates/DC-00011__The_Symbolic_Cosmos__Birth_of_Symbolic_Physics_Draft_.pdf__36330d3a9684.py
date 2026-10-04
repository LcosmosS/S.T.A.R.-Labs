print(kappa) # Output: ~31.59, matching sqrt(k) from topological model
a_calculated = -kappa * r_virgo # Applies scaling to distance for tension term
b_calculated = rho_virgo # Direct density mapping for compression term
print(f"Calculated a: {a_calculated}") # Verify matches original -1706
