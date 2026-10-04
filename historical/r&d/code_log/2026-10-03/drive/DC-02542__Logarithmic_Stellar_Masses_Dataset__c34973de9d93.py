import pandas as pd


# Specify the CSV filename
filename = 'Stellar_Mass2_Table.csv'


try:
    # Read the CSV file
    df = pd.read_csv(filename)
    
    # Filter rows where logmass and z are not -9999
    valid_df = df[(df['logmass'] != -9999) & (df['z'] != -9999)]
    
    # Select the first 1000 valid rows
    first_1000 = valid_df.head(1000)
    
    # Extract logmass and z values
    logmass = first_1000['logmass'].tolist()
    z = first_1000['z'].tolist()
    
    # Create a list of tuples (logmass, z)
    data = list(zip(logmass, z))
    
    # Print the first 5 entries for verification
    print("First 5 entries:", data[:5])
    
    # Write the full list to a file
    with open('output.txt', 'w') as f:
        f.write(str(data))
    
    print("Full data has been written to output.txt")
