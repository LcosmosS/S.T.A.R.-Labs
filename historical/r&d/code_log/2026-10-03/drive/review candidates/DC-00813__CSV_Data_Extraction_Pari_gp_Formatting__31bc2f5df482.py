import csv


filename = 'Stellar_Mass2_Table.csv'


with open(filename, 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)  # Read the header row
    # Exclude 'objid' from processing
    headers_to_process = [h for h in headers if h != 'objid']
    column_data = {header: [] for header in headers_to_process}
    
    for row in reader:
        for header, value in zip(headers, row):
            if header != 'objid' and value != '-9999.0':
                column_data[header].append(value)


# Format output in one unbroken line
output = ""
for header in headers_to_process:
    values = ",".join(column_data[header])
    output += f"{header}=[{values}];"


print(output)
