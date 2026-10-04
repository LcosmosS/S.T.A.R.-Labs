import csv
with open('fits_extract_clean.csv', 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    header = next(reader)
    num_fields = len(header)
    for i, row in enumerate(reader, 2):
        if len(row) != num_fields:
            print(f"Row {i} has {len(row)} fields, expected {num_fields}")
