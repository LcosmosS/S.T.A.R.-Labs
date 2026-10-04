import csv
with open('pipe3d_data.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
