def add_optimized_topology(df, name, ra_col, de_col, z_col, k=25):
    print(f"Computing {name} topology + persistence entropy...")

    # 1. Coordinate Transformation