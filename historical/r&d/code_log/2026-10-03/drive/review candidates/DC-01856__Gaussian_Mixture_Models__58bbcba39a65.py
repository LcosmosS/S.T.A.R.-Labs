if missing_cols:
    print(f"Error: The following columns are missing from the dataset: {', '.join(missing_cols)}")
    print(f"Available columns are: {', '.join(df.columns)}")
    exit(1)


# Convert specified columns to numeric, coercing non-numeric values to NaN
for col in columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')


# Filter out rows with NaN in any of the specified columns
df = df.dropna(subset=columns)


# Format the output as vectors
vectors = []
for col in columns:
    vector_str = f"{col}=[" + ",".join(map(str, df[col].tolist())) + "]"
    vectors.append(vector_str)


# Combine vectors into a single line
output = " ".join(vectors)


# Print the result
print(output)
