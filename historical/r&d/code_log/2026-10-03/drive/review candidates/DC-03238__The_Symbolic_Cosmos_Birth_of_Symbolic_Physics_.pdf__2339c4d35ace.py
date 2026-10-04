best_score = score
best_pair = (a, b)
return best_pair if best_pair else random.sample(valid_fibs, 2)
def analyze_curve(a, b, is_original=False, max_attempts=5):
"""Analyze an elliptic curve, returning success status and features."""
curve_name = 'Original curve' if is_original else 'Fibonacci curve'
print(f"\n{curve_name}: y² = x³ + {a}x + {b}")
try:
E = EllipticCurve(QQ, [0, 0, 0, a, b])
except ValueError as e:
print(f"Error creating curve: {e}")
return False, None
delta = E.discriminant()
conductor = E.conductor()
tors_order = E.torsion_subgroup().order()
print(f"Discriminant: {delta}")
print(f"Conductor: {conductor} = {factor(conductor)}")
print(f"Torsion order: {tors_order} (cyclic nodes in 3-sphere interweb)")
rank_success = False
selmer2_success = False
selmer3_success = False
rank = None
selmer_rank = None
selmer3_rank = None
for attempt in range(max_attempts):
try:
selmer_rank = E.selmer_rank()
selmer2_success = True
two_torsion_rank = 1 if tors_order % 2 == 0 else 0
rank_bound = selmer_rank - two_torsion_rank
rank = E.rank()
try:
E.two_descent(verbose=False)
gens = E.gens()
descent_rank = len(gens)
if rank != descent_rank:
