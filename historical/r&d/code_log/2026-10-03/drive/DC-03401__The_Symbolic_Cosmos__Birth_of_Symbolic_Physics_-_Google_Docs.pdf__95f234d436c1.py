except ValueError as e:
print(f"Failed to compute Heegner point: {e}")
# Compute the 2-Selmer rank using two_descent()
try:
E.two_descent(verbose=False)
selmer_rank = E.selmer_rank() # Use selmer_rank() if
