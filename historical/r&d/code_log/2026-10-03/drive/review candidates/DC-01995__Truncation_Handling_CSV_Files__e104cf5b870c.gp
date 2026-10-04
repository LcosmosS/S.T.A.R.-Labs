data = readvec("C:\\temp\\load_vectors.txt");
print("Min logmass: ", vecmin(data));
print("Max logmass: ", vecmax(data));
masses = vector(length(data), i, 10^data[i]);  \\ Try with higher precision first
