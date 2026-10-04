if non_torsion:
print(f"Found non-torsion points: {non_torsion}")
rank = max(1, len(non_torsion))
else:
print("No non-torsion points found, rank likely 0 if Selmer
