import pandas as pd


# Load the mangaHIall.csv file
mangaHIall = pd.read_csv('mangaHIall.csv')


# Rename 'MANGAID' to 'mangaid'
mangaHIall = mangaHIall.rename(columns={'MANGAID': 'mangaid'})
