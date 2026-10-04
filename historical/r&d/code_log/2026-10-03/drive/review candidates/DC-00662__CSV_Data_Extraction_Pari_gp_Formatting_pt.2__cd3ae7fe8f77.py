# Load dataset
csv_file = 'Stellar_Mass2_Table_cleaned.csv'
try:
    df = pd.read_csv(csv_file)
    print(f"Loaded '{csv_file}' successfully.")
