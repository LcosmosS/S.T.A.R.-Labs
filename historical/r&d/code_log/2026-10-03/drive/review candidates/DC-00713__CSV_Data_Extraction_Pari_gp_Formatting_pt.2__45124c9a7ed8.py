with open('pipe3d_data2.csv', 'r') as f:
    for i, line in enumerate(f, 1):
        if i == 3726:
            print(line)
