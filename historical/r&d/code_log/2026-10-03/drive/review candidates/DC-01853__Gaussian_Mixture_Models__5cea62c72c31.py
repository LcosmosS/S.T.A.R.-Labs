    print(f"File not found: {file_path}")
    exit(1)


# Define the correct column names based on the dataset
# Adjust these if the actual column names differ
columns = ['logmass', 'ra', 'sfr', 'z']


# Verify that the specified columns exist in the DataFrame
