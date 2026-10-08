import csv

# Initialize lists to store valid logmass and z values
log_mass = []
z = []

# Read the CSV file
with open('Stellar_Mass2_Table.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            logmass = float(row['logmass'])
            if logmass != -9999:
                log_mass.append(logmass)
                z.append(float(row['z']))
        except ValueError:
            continue  # Skip rows with non-numeric logmass or z

# Ensure we have exactly 1148 valid entries
if len(log_mass) != 1148:
    print(f"Warning: Found {len(log_mass)} valid entries, expected 1148.")

# Output the vectors in PARI/GP format
print("log_mass = [", end="")
print(", ".join(map(str, log_mass)), end="];")
print("\nz = [", end="")
print(", ".join(map(str, z)), end="];")