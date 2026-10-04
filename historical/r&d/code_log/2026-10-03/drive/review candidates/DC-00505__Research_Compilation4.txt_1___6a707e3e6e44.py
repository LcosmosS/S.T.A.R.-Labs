import csv


# Initialize lists to store valid logmass and z values
log_mass = []
z = []


# Read the CSV file
with open('Stellar_Mass2_Table.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        logmass = float(row['logmass'])
        if logmass != -9999:  # Skip invalid entries
            log_mass.append(logmass)
            z.append(float(row['z']))


# Print the vectors in PARI/GP format
print("log_mass = [", end="")
print(", ".join(map(str, log_mass)), end="];")
print("\nz = [", end="")
print(", ".join(map(str, z)), end="];")


# Print the number of valid entries
print(f"\nNumber of valid galaxies: {len(log_mass)}")
