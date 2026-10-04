	log_mass = [\n10.234\n11.345\n...]\n;
	lines = readstr(...); log_mass = vector(#lines-2, i, eval(lines[i+1]))
