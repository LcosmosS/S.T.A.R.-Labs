offset = 10;  \\ Adjust based on max logmass
masses = vector(length(data), i, 10^(data[i] - offset));
