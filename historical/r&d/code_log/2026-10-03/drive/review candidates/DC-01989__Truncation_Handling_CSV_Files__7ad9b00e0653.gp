raw_data = read("C:\\temp\\load_vectors.txt");
data = vector(length(raw_data), i, Str(raw_data[i]));  \\ Convert to strings
data = vector(length(data), i, component(Vec(data[i], ","), 5));  \\ Extract 5th column
