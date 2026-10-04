import pandas as pd


# Define the path to the CSV file
file_path = 'Stellar_Mass2_Bigsby.csv'  # Change this if the file is in a different location


try:
    df = pd.read_csv(file_path)
