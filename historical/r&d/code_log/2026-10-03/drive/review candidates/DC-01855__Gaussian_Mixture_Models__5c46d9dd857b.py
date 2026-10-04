    print(f"File not found: {file_path}")
    exit(1)


# Define the expected column names
# Adjust these based on your actual dataset
columns = ['logmass', 'ra', 'sfr', 'z']


# Check if all specified columns exist in the DataFrame
