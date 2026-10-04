for a, b in previous_curves:
result = analyze_curve(a, b)
if result[0]:
success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size = result
data_tuple = (a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size)
curves_data.append((None, data_tuple))
with open(csv_file, 'a', newline='') as csv_f:
csv_writer = csv.writer(csv_f)
csv_writer.writerow(data_tuple)
if rank and rank >= 3:
training_data.append(features)
training_labels.append(rank)
print(f"Added rank {rank} curve to training data: {features}")
gc.collect()
for _ in range(max_attempts):
a, b = random_fibonacci_pair(fib_numbers, lucas_numbers, high_rank_pairs)
result = analyze_curve(a, b)
if result[0]:
success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size = result
data_tuple = (a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size)
curves_data.append((None, data_tuple))
with open(csv_file, 'a', newline='') as csv_f:
csv_writer = csv.writer(csv_f)
csv_writer.writerow(data_tuple)
if rank and rank >= 3:
training_data.append(features)
training_labels.append(rank)
print(f"Added rank {rank} curve to training data: {features}")
gc.collect()
twist_primes = [2, 3, 5, 7]
for a, b in high_rank_pairs:
try:
E = EllipticCurve(QQ, [0, 0, 0, a, b])
for d in twist_primes:
E_twist = quadratic_twist(E, d)
a_new = E_twist.a4()
b_new = E_twist.a6()
print(f"\nTwisting curve (a={a}, b={b}) with d={d}")
result = analyze_curve(a_new, b_new)
if result[0]:
success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E_twist, selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size = result
data_tuple = (a_new, b_new, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size)
curves_data.append((f"Twist_d{d}", data_tuple))
with open(csv_file, 'a', newline='') as csv_f:
csv_writer = csv.writer(csv_f)
csv_writer.writerow(data_tuple)
if rank and rank >= 3:
training_data.append(features)
training_labels.append(rank)
print(f"Added twisted rank {rank} curve to training data: {features}")
gc.collect()
except Exception as e:
print(f"Error processing curve (a={a}, b={b}) for twisting: {e}")
try:
