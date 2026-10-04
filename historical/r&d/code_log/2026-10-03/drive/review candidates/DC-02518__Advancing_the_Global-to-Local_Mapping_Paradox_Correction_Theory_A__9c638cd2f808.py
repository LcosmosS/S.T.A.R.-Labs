import unreal
import csv
import os


def load_interweb_data():
    csv_path = "C:/path/to/interweb_nodes.csv"  # Update path
    nodes = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            node = {
                'log_delta': float(row['log_delta']),
                'log_cond': float(row['log_cond']),
                'rank': float(row['rank']),
                'volume': float(row['volume']),
                'reg': float(row['reg'])
            }
            nodes.append(node)
                     *     return nodes
