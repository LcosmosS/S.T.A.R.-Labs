for subpop, group in grouped:
    print(f"Subpopulation {subpop}:")
    print(f"  Mean z: {group['z'].mean():.4f}")
    print(f"  Mean sfr: {group['sfr'].mean():.4f}")
