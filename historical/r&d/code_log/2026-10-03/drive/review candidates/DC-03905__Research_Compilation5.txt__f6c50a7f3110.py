import numpy as npDefine the file pathfile_path = 'Stellar_Mass2_Table.csv'Load the CSV file into a DataFrametry:
    df = pd.read_csv(file_path)
    print("Columns in the DataFrame:", df.columns)  # Print column names for debugging
