    rank = None


    selmer_rank = None


    selmer3_rank = None


    leading_coeff = None


    omega = None


    reg = None





    if conductor > 10**9:  # Skip large conductors


        print("Conductor too large, skipping curve")


        return False, None, None, None, None, None





    for attempt in range(max_attempts):


        try:


            selmer_rank = E.selmer_rank()


            selmer2_success = True


            two_torsion_rank = 1 if tors_order % 2 == 0 else 0


            rank_bound = selmer_rank - two_torsion_rank


            rank = E.rank()


            try: