data = readvec("data.txt");  \\ Assuming columns: mass, sfr, metallicity
mass = vector(#data, i, data[i][1]);
sfr = vector(#data, i, data[i][2]);
metallicity = vector(#data, i, data[i][3]);
