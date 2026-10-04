import zipfile
import pandas as pd


# Extract CSV from zip file
with zipfile.ZipFile('data.zip', 'r') as zip_ref:
    zip_ref.extract('PhotoObj_pmqr771.csv')


# Load the dataset
df = pd.read_csv("PhotoObj_pmqr771.csv")
# Continue with the rest of the script...
