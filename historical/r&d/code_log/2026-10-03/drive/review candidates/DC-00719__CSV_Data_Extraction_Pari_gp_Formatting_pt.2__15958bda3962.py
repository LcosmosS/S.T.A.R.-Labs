import csv


rows_per_file = 2555  # For first three files, last will adjust


with open('pipe3d_data.csv', 'r') as infile:
    reader = csv.reader(infile)
    header = next(reader)


    for i in range(3):  # First three files
        with open(f'pipe3d_data_part{i+1}.csv', 'w', newline='') as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
            writer.writerow(header)
            for _ in range(rows_per_file):
                try:
                    row = next(reader)
                    writer.writerow(row)
                except StopIteration:
                    break


    # Last file, get remaining rows
    with open(f'pipe3d_data_part4.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        for row in reader:
            writer.writerow(row)
