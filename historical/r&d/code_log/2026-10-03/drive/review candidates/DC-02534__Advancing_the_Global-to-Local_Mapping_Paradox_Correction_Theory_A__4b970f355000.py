rank_info = E.two_descent()
selmer2_rank = E.rank()  # Approximate via descent
except Exception as e:
print(f"SageMath two_descent failed for {E.ainvs()}: {e}")
selmer2_rank = None
try:
pari_E = pari.ellinit(E.ainvs())
pari_data = pari_E.ellrank()
pari_rank = pari_data[0]
except Exception as e:
print(f"PARI/GP ellrank failed for {E.ainvs()}: {e}")
pari_rank = None
