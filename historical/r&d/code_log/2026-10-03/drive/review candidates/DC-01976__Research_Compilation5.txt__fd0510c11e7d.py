for col in columns:
    if col in df.columns:
        vector_str = f"{col}=[" + ",".join(map(str, df[col].tolist())) + "]"
        vectors.append(vector_str)
    else:
        print(f"Column '{col}' not found, skipping.")
