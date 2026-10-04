mass_parts = select(p -> strstart(p, "mass_part"), parts);
mass = [];
for (part in mass_parts,
  /* Find the position of "=" and extract the value string */
  eq_pos = strpos("=", part);
  values_str = substr(part, eq_pos + 1, #part - eq_pos - 2);  /* Remove brackets */
  values = strsplit(values_str, ",");
  /* Convert string values to numbers and append to mass */
  mass = concat(mass, vector(#values, i, eval(values[i])));
