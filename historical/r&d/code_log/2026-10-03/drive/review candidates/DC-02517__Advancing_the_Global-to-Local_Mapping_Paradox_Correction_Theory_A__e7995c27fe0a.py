import csv
interweb_data = []
with open('interweb_nodes.txt', 'r') as f:
    for line in f:
        data = eval(line.strip())  # Safely parse tuple
        interweb_data.append(data)


with open('interweb_nodes.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['a', 'b', 'rank', 'leading_coeff', 'omega', 'reg', 'tamagawa', 'weak_bsd_holds', 'log_delta', 'log_cond', 'volume'])
                  *     writer.writerows(interweb_data)
