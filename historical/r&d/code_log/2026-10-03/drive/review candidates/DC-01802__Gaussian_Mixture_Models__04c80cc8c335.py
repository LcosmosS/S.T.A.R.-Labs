for subpop, group in grouped:
    print(f"Subpopulation {subpop}:")
    print(f"  Std z: {group['z'].std():.4f}")
    print(f"  Std sfr: {group['sfr'].std():.4f}")
