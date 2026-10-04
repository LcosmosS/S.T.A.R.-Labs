import csv


# Initialize lists to store valid logmass and z values
log_mass = []
z = []
valid_count = 0


# Read the CSV file
with open('Stellar_Mass2_Table.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            logmass = float(row['logmass'])
            z_value = float(row['z'])
            if logmass != -9999:
                log_mass.append(logmass)
                z.append(z_value)
                valid_count += 1
                if valid_count == 1000:
                    break
        except ValueError:
            continue  # Skip rows with non-numeric logmass or z


# Check if we have at least 1000 valid entries
if len(log_mass) < 1000:
    print(f"Warning: Found only {len(log_mass)} valid entries, expected 1000.")


# Write the vectors to data.gp in PARI/GP format
with open(r'C:\temp\data.gp', 'w') as f:
    f.write('log_mass = [\n')
    for value in log_mass:
        f.write(str(value) + ',\n')
    f.write('];\n')
    f.write('z = [\n')
    for value in z:
        f.write(str(value) + ',\n')
    f.write('];\n')
