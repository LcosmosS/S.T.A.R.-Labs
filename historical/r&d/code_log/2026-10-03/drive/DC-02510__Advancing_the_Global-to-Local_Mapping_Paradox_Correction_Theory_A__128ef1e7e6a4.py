def analyze_curve(a, b):
print(f"\nAnalyzing curve: y^2 = x^3 + {a}x + {b}")
try:
E = EllipticCurve(QQ, [0, 0, 0, a, b])
delta = E.discriminant()
conductor = E.conductor()
tors_order = E.torsion_subgroup().order()
print(f"Discriminant: {delta}")
print(f"Conductor: {conductor} = {factor(conductor)}")
print(f"Torsion order: {tors_order}")
try:
analytic_rank = E.rank(only_use_mwrank=True)
except Exception as e:
print(f"Analytic rank computation failed: {e}")
analytic_rank = None
try:
algebraic_rank = E.rank()
except Exception as e:
print(f"Algebraic rank computation failed: {e}")
algebraic_rank = None
print(f"Analytic rank: {analytic_rank}")
print(f"Algebraic rank: {algebraic_rank}")
selmer2_rank, selmer3_rank = compute_selmer_ranks(E)
print(f"2-Selmer rank (Sage): {selmer2_rank}")
print(f"3-Selmer rank (PARI/GP estimate): {selmer3_rank}")
D, P, twist_d = compute_heegner_point(E)
if D is not None and P is not None:
curve_str = f"twist by d={twist_d}" if twist_d else "original curve"
print(f"Heegner point for D={D} on {curve_str}: {P}")
