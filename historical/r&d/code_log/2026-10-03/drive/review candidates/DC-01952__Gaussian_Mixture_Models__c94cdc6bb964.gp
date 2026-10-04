mass_parts = select(p -> strstart(p, "mass_part"), parts);
mass = [];
for (part in mass_parts,
  eq_pos = strpos("=", part);
  values_str = substr(part, eq_pos + 1, #part - eq_pos - 2);
  values = strsplit(values_str, ",");
  mass = concat(mass, vector(#values, i, eval(values[i])));
