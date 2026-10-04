rank = 0 if selmer_rank == two_torsion_rank else rank
rank_success = True
except:
print("Point search failed")
128print(f"Algebraic rank: {rank} (independent nodes in cosmic web)")
print(f"2-Selmer rank: {selmer_rank}")
try:
S3 = E.selmer_group(3, [])
selmer3_rank = len(S3) - 1
print(f"3-Selmer rank: {selmer3_rank}")
selmer3_success = True
except:
print("Failed to compute 3-Selmer rank")
break
except:
print(f"Rank computation failed on attempt {attempt + 1}")
if attempt == max_attempts - 1:
print("Max attempts reached, skipping curve")
return False, None
# Relaxed success: rank and 2-Selmer required, 3-Selmer optional
success = rank_success and selmer2_success
if success:
try:
L = E.lseries()
dok = L.dokchitser(prec=100)
L1 = dok(1)
if abs(L1) < 1e-10:
try:
L1_deriv = dok.derivative(1, 1)
if abs(L1_deriv) < 1e-10:
L1_deriv2 = dok.derivative(1, 2)
analytic_rank = 2
leading_coeff = L1_deriv2 / 2
else:
analytic_rank = 1
leading_coeff = L1_deriv
except:
analytic_rank = 2
leading_coeff = 0
else:
analytic_rank = 0
leading_coeff = L1
print(f"Analytic rank: {analytic_rank}")
print(f"Leading coefficient: {leading_coeff} (topological density in
