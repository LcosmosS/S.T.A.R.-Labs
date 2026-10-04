def hierarchy_evidence(E, name):

   try:

       algebraic_rank = E.rank()

       pari_E = pari(E)

       selmer_2_rank = pari_E.ellrank()[1]  # 2-Selmer

       analytic_rank = E.rank(algorithm='pari')  # Analytic proxy

       conclusion = algebraic_rank == selmer_2_rank == analytic_rank

       print(f"{name}: Algebraic {algebraic_rank}, 2-Selmer {selmer_2_rank}, Analytic
