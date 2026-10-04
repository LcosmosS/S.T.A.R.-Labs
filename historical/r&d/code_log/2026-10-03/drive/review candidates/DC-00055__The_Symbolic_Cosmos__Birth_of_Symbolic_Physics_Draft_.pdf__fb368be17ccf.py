weak_bsd_holds = (rank == analytic_rank)
if weak_bsd_holds:
print("Weak BSD holds: Algebraic rank = Analytic rank")
else:
print("Weak BSD fails: Algebraic rank != Analytic rank")
except:
print("L-function computation failed")
return False, None, None, None, None, None, None, False
try:
omega = E.period_lattice().real_period(prec=100)
reg = E.regulator() if rank > 0 else 1.0
tamagawa = prod(E.tamagawa_numbers())
