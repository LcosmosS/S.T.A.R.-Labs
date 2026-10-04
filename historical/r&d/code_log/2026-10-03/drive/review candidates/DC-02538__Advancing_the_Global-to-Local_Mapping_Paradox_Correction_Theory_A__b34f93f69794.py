def main():
high_rank_pairs = [(2, 144), (377, 987), (-102, 918), (34, 4181), (17711, 17711), (17711, 46368)]
max_attempts = 10
curves_data = []
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_file = f"interweb_nodes_{timestamp}.csv"
with open(csv_file, 'w', newline='') as csv_f:
csv_writer = csv.writer(csv_f)
csv_writer.writerow(['a', 'b', 'rank', 'leading_coeff', 'omega', 'reg', 'tamagawa', 'weak_bsd_holds', 'selmer3_rank', 'log_delta', 'log_cond', 'longitude', 'latitude', 'elevation', 'size'])
previous_curves = [
