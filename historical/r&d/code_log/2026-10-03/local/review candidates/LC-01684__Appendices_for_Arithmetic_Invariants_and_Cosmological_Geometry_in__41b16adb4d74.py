    X_tf = df[feature_cols]
    y_tf = df['petrorad_r']
    valid_idx = y_tf.notna()
    X_tf = X_tf[valid_idx]
    y_tf = y_tf[valid_idx]
    print(f"Tully-Fisher: Dropped {len(df) - len(X_tf)} rows due to NaN in
