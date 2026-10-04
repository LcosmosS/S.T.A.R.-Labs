if missing_cols:
    print(f"Error: The following columns are missing in the DataFrame: {missing_cols}")
    exit(1)


# Convert specified columns to numeric, coercing non-numeric values to NaN
for col in columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')


# Filter out rows where any of the specified columns contain NaN
df = df.dropna(subset=columns)


# Create a list to store the formatted vector strings
vectors = []


# Format each column's data as a vector string
for col in columns:
    vector_str = f"{col}=[" + ",".join(map(str, df[col].tolist())) + "]"
    vectors.append(vector_str)


# Combine all vector strings into a single line, separated by spaces
output = " ".join(vectors)


# Print the result
print(output)
