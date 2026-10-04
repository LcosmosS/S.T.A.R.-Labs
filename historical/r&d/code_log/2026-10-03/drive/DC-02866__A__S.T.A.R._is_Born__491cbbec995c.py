import csv


input_file = '2Mass.csv'
output_file = '2Mass_cleaned.csv'


with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    header = next(reader)  # Assuming first row is header
    expected_fields = len(header)
    writer.writerow(header)
    for i, row in enumerate(reader, start=2):  # Start at line 2
        if len(row) != expected_fields:
            print(f"Line {i} has {len(row)} fields, expected {expected_fields}. Adjusting...")
            # Truncate or pad the row as needed (example: truncate extra fields)
            row = row[:expected_fields]
   *         writer.writerow(row)
   * This script ensures all rows match the header’s field count by truncating extra fields. Adjust the logic (e.g., padding with empty strings) based on your data’s needs.
