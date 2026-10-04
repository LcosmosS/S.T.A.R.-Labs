def compute_symbolic_entropy(curve_data):
entropy = 0
for ap, p in zip(curve_data['ap_list'], curve_data['prime_list']):
if ap != 0:
entropy -= np.log(abs(ap)) / p
return entropy
curve_data = {'ap_list': [1, -1, 0, 2], 'prime_list': [2, 3, 5, 7]}
symbolic_entropy = compute_symbolic_entropy(curve_data)
