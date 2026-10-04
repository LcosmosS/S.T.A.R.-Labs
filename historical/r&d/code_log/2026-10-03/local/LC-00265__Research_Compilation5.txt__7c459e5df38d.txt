rank = sum(1 for K in K_values.values() if abs(K - 1) < 0.1)
print(f"Rank: {rank}")
