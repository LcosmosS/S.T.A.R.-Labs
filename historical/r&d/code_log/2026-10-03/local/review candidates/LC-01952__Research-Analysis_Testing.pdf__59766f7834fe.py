# Define the point P = (2, 54)
P = E([2, 54])
# Compute the canonical height with 100 bits of precision
Reg = P.height(precision=100) # Note: 'prec' is often 'precision' in SageMath
# Print the regulator
print(Reg)
