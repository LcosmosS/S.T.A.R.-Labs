print(f"Discriminant: {delta}")
print(f"Conductor: {conductor} = {factor(conductor)}")
print(f"Torsion order: {tors_order} (cyclic nodes in 3-sphere interweb)")
if conductor > 2e8 and not is_original:
print("Conductor too large, skipping curve")
return False, None, None, None, None, None, None, False
rank_success = False
selmer2_success = False
selmer3_success = False
rank = None
selmer_rank = None
selmer3_rank = None
leading_coeff = None
omega = None
reg = None
tamagawa = None
weak_bsd_holds = False
for attempt in range(max_attempts):
try:
selmer_rank = E.selmer_rank()
selmer2_success = True
two_torsion_rank = 1 if tors_order % 2 == 0 else 0
rank = E.rank()
try:
E.two_descent(verbose=False)
gens = E.gens()
descent_rank = len(gens)
if rank != descent_rank:
