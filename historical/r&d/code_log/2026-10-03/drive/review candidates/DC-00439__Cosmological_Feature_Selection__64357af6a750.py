import zipfile


# Extract the CSV from the zip file
zip_file_name = 'data.zip'  # Replace with your actual zip file name
csv_file_name = 'PhotoObj_pmqr771.csv'  # Replace with your actual CSV file name inside the zip


with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
    zip_ref.extract(csv_file_name)
