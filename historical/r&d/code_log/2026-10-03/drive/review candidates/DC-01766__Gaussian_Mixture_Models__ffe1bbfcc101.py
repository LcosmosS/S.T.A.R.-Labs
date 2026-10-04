output_columns = ['logmass', 'ra', 'z', 'sfr', 'objid', 'dec', 'petrorad', 'ellipticity', 'metallicity']
vector_strings = []
for col in output_columns:
    values = df[col].values
    if df[col].dtype == 'object':
        values_str = [f'"{val}"' for val in values]
    else:
        values_str = [str(val) for val in values]
    vector_strings.append(f"{col}=[{','.join(values_str)}]")
output_line = ','.join(vector_strings)
with open('vectors.gp', 'w') as f:
    f.write(output_line)
print("Vectors saved to vectors.gp in the requested single line format.")
print("Note: The file contains a single long line which may cause truncation issues in PARI/GP for large vectors. Consider using readvec with separate files or increasing stack size with allocatemem().")
