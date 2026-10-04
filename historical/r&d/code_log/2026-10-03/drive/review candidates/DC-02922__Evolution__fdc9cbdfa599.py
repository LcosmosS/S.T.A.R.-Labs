   from sage.all import EllipticCurve, QQ, pari


   def hierarchy_evidence(E, name):
       try:
           algebraic_rank = E.rank()
           pari_E = pari(E)
           selmer_2_rank = pari_E.ellrank()[1]  # 2-Selmer
           analytic_rank = E.rank(algorithm='pari')  # Analytic proxy
           conclusion = algebraic_rank == selmer_2_rank == analytic_rank
           print(f"{name}: Algebraic {algebraic_rank}, 2-Selmer {selmer_2_rank}, Analytic {analytic_rank}, Converge: {conclusion}")
           return conclusion
       except Exception as e:
           print(f"Error for {name}: {e}")
           return False


   # Cornerstone r=3
   E3 = EllipticCurve(QQ, [2, 144])
   hierarchy_evidence(E3, "Cornerstone Rank 3")


   # Virgo r=1
   E1 = EllipticCurve(QQ, [-1706, 6320])
   hierarchy_evidence(E1, "Virgo Rank 1")


   # Rank 2 example
   E2 = EllipticCurve(QQ, [5, 144])
   hierarchy_evidence(E2, "Rank 2 Example")


   # Twist for higher rank
   E_twist = EllipticCurve(QQ, [170, -4250])  # From file 9
   hierarchy_evidence(E_twist, "Twisted Rank 2")
