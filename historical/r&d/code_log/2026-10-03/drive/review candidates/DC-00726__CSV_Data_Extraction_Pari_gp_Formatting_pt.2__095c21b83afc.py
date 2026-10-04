import csv
with open('MyTable.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    expected = len(header)
    for i, row in enumerate(reader, 2):
        if len(row) != expected:
*             print(f"Row {i} has {len(row)} fields, expected {expected}")
