import csv
with open('pipe3d_data.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    expected = len(header)
    for i, row in enumerate(reader, 2):
        if len(row) != expected:
