import csv


rows_per_file = 3407  # Hardcoding since total_rows is 10221


with open('pipe3d_data.csv', 'r') as infile:
    reader = csv.reader(infile)
    header = next(reader)


    for i in range(3):
        with open(f'pipe3d_data_part{i+1}.csv', 'w', newline='') as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
            writer.writerow(header)
            for _ in range(rows_per_file):
                try:
                    row = next(reader)
                    writer.writerow(row)
                except StopIteration:
                    break
