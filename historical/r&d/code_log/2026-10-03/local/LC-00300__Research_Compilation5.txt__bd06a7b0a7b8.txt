    print(f"File not found: {file_path}")
    exit(1)


# Define columns of interest
columns = ['log_mass', 'ra', 'sfr', 'z']


# Convert columns to numeric, coercing errors to NaN
for col in columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')


# Drop rows where any of the specified columns are NaN
df = df.dropna(subset=columns)


# Create vector strings for each column
vectors = []
for col in columns:
    vector_str = f"{col}=[" + ",".join(map(str, df[col].tolist())) + "]"
    vectors.append(vector_str)


# Combine into a single line with spaces
output = " ".join(vectors)


# Print the output
print(output)
