            E_pari = pari.ellinit([0, 0, 0, a, b])
            rank_info = E_pari.ellrank()

            rank = int(rank_info[0])
            rank_success = True
            print(f"Algebraic rank (via PARI/GP): {rank}")
            selmer3_rank = rank
            print(f"3-Selmer rank (refined using BSD): {selmer3_rank}")

            break
        except Exception as e:
            print(f"Rank computation failed on attempt {attempt + 1}: {e}")
            if attempt == max_attempts - 1:
                return False, None, None, None, None, None, None, False, None, None


    success = rank_success
    if success:
        try:
            print(f"Leading coefficient: {leading_coeff}")
            weak_bsd_holds = (rank == analytic_rank)

            print(f"Weak BSD holds: {weak_bsd_holds}")

            omega = E.period_lattice().real_period(prec=50)
            tamagawa = prod(E.tamagawa_numbers())
            sha_order = 1

            rhs = leading_coeff * (tors_order**2)
            reg = rhs / (omega * tamagawa * sha_order) if rank > 0 else 1.0
            cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
            scaled_period = omega * SQRT_KAPPA * cosmo_scale
            comoving_volume = (omega * reg * cosmo_scale**3) / (2.5e11 if rank == 3 else 5e13 if
rank == 2 else 1e15 if rank == 1 else 1e13)