for (i=1, #parts,
  part = parts[i];
  if (part == "", continue);  \ skip empty parts
  eq_pos = strpos("=", part);
  name = substr(part, 1, eq_pos-1);
  values_str = substr(part, eq_pos+1, #part - eq_pos - 1);
  if (substr(values_str, 1, 1) == "[", values_str = substr(values_str, 2, #values_str - 2));
  values = strsplit(values_str, ",");
  vec = vector(#values, j, eval(values[j]));
  if (name == "log_mass", log_mass = vec);
  if (name == "ra", ra = vec);
  if (name == "sfr", sfr = vec);
  if (name == "z", z = vec);
