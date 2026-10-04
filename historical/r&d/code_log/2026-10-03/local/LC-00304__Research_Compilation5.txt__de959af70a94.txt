    print(f"File not found: {file_path}")
    exit(1)Define the columns of interestcolumns = ['log_mass', 'ra', 'sfr', 'z']Convert specified columns to numeric, coercing non-numeric values to NaNfor col in columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')Filter out rows where any of the specified columns contain NaNdf = df.dropna(subset=columns)Create a list to store the formatted vector stringsvectors = []Format each column's data as a vector stringfor col in columns:
    # Convert the column values to a list and then to strings, joining with commas
    vector_str = f"{col}=[" + ",".join(map(str, df[col].tolist())) + "]"
    vectors.append(vector_str)Combine all vector strings into a single line, separated by spacesoutput = " ".join(vectors)Print the resultprint(output)
