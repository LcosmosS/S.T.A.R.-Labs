with open('pipe3d_data.csv', 'r') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader, 1):
        if i == 3726:
            print(f"Row 3726 has {len(row)} fields")
