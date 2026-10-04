rank = 0 if selmer_rank == two_torsion_rank else rank
rank_success = True
print(f"Algebraic rank: {rank} (independent nodes in cosmic web)")
print(f"2-Selmer rank: {selmer_rank}")
try:
S3 = E.selmer_group(3, [])
selmer3_rank = len(S3) - 1
print(f"3-Selmer rank: {selmer3_rank}")
selmer3_success = True
if selmer3_rank >= 3:
print("Found potential 3-salmer candidate!")
except Exception as e:
print(f"Failed to compute 3-Selmer rank: {e}")
break
except:
135print(f"Rank computation failed on attempt {attempt + 1}")
if attempt == max_attempts - 1:
print("Max attempts reached, skipping curve")
return False, None, None, None, None, None, None, False
success = rank_success and selmer2_success and (selmer3_success if require_3selmer
else True)
if success:
try:
L = E.lseries()
dok = L.dokchitser(prec=100)
L1 = dok(1)
analytic_rank = 0
leading_coeff = L1
if abs(L1) < 1e-10:
try:
L1_deriv = dok.derivative(1, 1)
if abs(L1_deriv) < 1e-10:
L1_deriv2 = dok.derivative(1, 2)
if abs(L1_deriv2) < 1e-10 and rank >= 3:
L1_deriv3 = dok.derivative(1, 3)
analytic_rank = 3
leading_coeff = L1_deriv3 / 6
else:
analytic_rank = 2
leading_coeff = L1_deriv2 / 2
else:
analytic_rank = 1
leading_coeff = L1_deriv
except:
analytic_rank = max(2, rank)
leading_coeff = 0
print(f"Analytic rank: {analytic_rank}")
print(f"Leading coefficient: {leading_coeff} (topological density in
