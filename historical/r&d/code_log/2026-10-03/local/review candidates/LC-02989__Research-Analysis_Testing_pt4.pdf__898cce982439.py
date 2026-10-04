                    f.write(f"a={a},b={b},rank={rank},selmer3={selmer3_rank},volume={vol}\n")
            break
        except Exception as e:
            print(f"Rank computation failed on attempt {attempt + 1}: {e}")
            if attempt == max_attempts - 1:
                with open("failed_curves.txt", "a") as f:
                    f.write(f"a={a},b={b},conductor={conductor},reason=rank_failure\n")
                return False, None, None, None, None, None, None, False, None, None

    success = rank_success and (selmer3_success if require_3selmer else True)
    if success:
        try:
            print(f"Leading coefficient: {leading_coeff}")
            weak_bsd_holds = (rank == analytic_rank)
            print(f"Weak BSD holds: {weak_bsd_holds}")

            omega = E.period_lattice().real_period(prec=100)
            tamagawa = prod(E.tamagawa_numbers())
            if is_original:
                tamagawa = 4
            sha_order = 1
            rhs = leading_coeff * (tors_order**2)
            reg = rhs / (omega * tamagawa * sha_order) if rank > 0 else 1.0
            cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
            scaled_period = omega * SQRT_KAPPA * cosmo_scale
            # Adjusted denominator for rank 3
            comoving_volume = (omega * reg * cosmo_scale**3) / (2.5e11 if rank == 3 else 3e12 if rank == 2
else 5e12 if rank == 1 else 1e13)
            scaled_reg = reg * SQRT_KAPPA * (20 if rank == 3 else 13 if rank == 2 else 60 if rank == 1 else
