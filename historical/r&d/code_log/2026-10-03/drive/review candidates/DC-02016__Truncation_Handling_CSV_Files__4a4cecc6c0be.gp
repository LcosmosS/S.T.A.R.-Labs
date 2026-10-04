lines = readstr("C:\\temp\\load_vectors.txt");
data = vector(length(lines), i, Strsplit(lines[i], ","));
