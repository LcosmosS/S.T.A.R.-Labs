import csv
with open('pipe3d_data2.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    expected = len(header)
    for i, row in enumerate(reader, 2):
        if len(row) != expected:
            print(f"Row {i} has {len(row)} fields, expected {expected}")

with open('pipe3d_data2.csv', 'r') as f:
    for i, line in enumerate(f, 1):
        if i == 3726:
            print(line)
            break