import zipfile
import pandas as pd


# Extract CSV from zip file
with zipfile.ZipFile('data.zip', 'r') as zip_ref:
    zip_ref.extract('PhotoObj_pmqr771.csv')


# Now load the CSV and run the script
df = pd.read_csv("PhotoObj_pmqr771.csv")
# Rest of the script...
