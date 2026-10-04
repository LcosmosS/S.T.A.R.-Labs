def compute_heegner_point(E, max_D=-100):
try:
rank = E.rank()
if rank == 1:
for D in range(-3, max_D - 1, -1):
if satisfies_heegner_hypothesis(E, D):
try:
pari_E = pari.ellinit(E.ainvs())
heegner_data = pari_E.ellheegner(D)
x, y = heegner_data[0], heegner_data[1]
P = E([x, y])
return D, P, None
except Exception as e:
print(f"PARI/GP Heegner point failed for D={D}: {e}")
try:
P = E.heegner_point(D).point_exact()
return D, P, None
except Exception as e:
print(f"Sage Heegner point failed for D={D}: {e}")
continue
print(f"No suitable discriminant found for Heegner point on {E.ainvs()}")
return None, None, None
else:
print(f"Curve {E.ainvs()} has rank {rank}, trying quadratic twists")
for d in [2, 3, 5, 7]:
E_twist = quadratic_twist(E, d)
try:
twist_rank = E_twist.rank()
if twist_rank == 1:
print(f"Twist by d={d} has rank 1: {E_twist.ainvs()}")
for D in range(-3, max_D - 1, -1):
if satisfies_heegner_hypothesis(E_twist, D):
try:
pari_E = pari.ellinit(E_twist.ainvs())
heegner_data = pari_E.ellheegner(D)
x, y = heegner_data[0], heegner_data[1]
P = E_twist([x, y])
return D, P, d
except Exception as e:
print(f"PARI/GP Heegner point failed for twist d={d}, D={D}: {e}")
try:
P = E_twist.heegner_point(D).point_exact()
return D, P, d
except Exception as e:
print(f"Sage Heegner point failed for twist d={d}, D={D}: {e}")
continue
except Exception as e:
print(f"Rank computation failed for twist d={d}: {e}")
continue
print(f"No rank 1 twist found for {E.ainvs()}")
return None, None, None
except Exception as e:
print(f"Failed to compute Heegner point for {E.ainvs()}: {e}")
return None, None, None
