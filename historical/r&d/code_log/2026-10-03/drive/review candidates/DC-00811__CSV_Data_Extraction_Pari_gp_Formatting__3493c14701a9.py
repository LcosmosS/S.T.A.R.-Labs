import csv


filename = 'Stellar_Mass2_Table.csv'


with open(filename, 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)
    column_data = {header: [] for header in headers}
    
    for row in reader:
        if all(value != "-9999" for value in row):
            for header, value in zip(headers, row):
                column_data[header].append(value)


output = ""
for header in headers:
    values = ",".join(column_data[header])
    output += f"{header}=[{values}];"


print(output)
