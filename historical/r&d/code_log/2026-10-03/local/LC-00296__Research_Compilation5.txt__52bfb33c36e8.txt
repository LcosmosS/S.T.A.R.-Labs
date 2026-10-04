vectors = []
for col in columns:
    vector_str = f"{col}=[" + ",".join(map(str, df[col].tolist())) + "]"
    vectors.append(vector_str)
output = " ".join(vectors)
print(output)
