import pandas as pd


# Load the mangaHIall.csv file
mangaHIall = pd.read_csv('mangaHIall.csv')


# Rename the 'MANGAID' column to 'mangaid'
mangaHIall = mangaHIall.rename(columns={'MANGAID': 'mangaid'})


# Now, all datasets should have the 'mangaid' column
