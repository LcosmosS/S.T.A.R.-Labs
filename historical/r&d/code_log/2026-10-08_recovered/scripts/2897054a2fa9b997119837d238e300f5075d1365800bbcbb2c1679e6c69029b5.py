import pandas as pd  # Assuming you're using pandas
import csv          # Add this line to import the csv module

# Read the original CSV file
df = pd.read_csv('pipe3d_data.csv')

# Write to a new CSV file with all fields quoted
df.to_csv('pipe3d_data2.csv', index=False, quoting=csv.QUOTE_ALL)