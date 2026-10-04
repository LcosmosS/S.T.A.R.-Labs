            analytic_rank = 0
            leading_coeff = L1
            if abs(L1) < 1e-10:
                L1_deriv = dok.derivative(1, 1)
                if abs(L1_deriv) < 1e-10:
                    L1_deriv2 = dok.derivative(1, 2)
                    if abs(L1_deriv2) < 1e-10 and rank >= 3:
                        L1_deriv3 = dok.derivative(1, 3)
                        analytic_rank = 3
                        leading_coeff = L1_deriv3 / 6
                    else:
                        analytic_rank = 2
                        leading_coeff = L1_deriv2 / 2
                else:
                    analytic_rank = 1
                    leading_coeff = L1_deriv
            print(f"Analytic rank: {analytic_rank}")
            print(f"Leading coefficient: {leading_coeff}")
            weak_bsd_holds = (rank == analytic_rank)
            print(f"Weak BSD holds: {weak_bsd_holds}")

            omega = E.period_lattice().real_period(prec=100)
            reg = E.regulator() if rank > 0 else 1.0
            tamagawa = prod(E.tamagawa_numbers())
            if is_original:
                tamagawa = 4
            sha_order = 1
            rhs = (omega * reg * sha_order * tamagawa) / (tors_order**2)
            cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
            scaled_period = omega * SQRT_KAPPA * cosmo_scale
            comoving_volume = (omega * reg * cosmo_scale**3) / (1.5e13 if rank == 3 else 5e13 if rank == 2
else 8e13 if rank == 1 else 1e14)
            scaled_reg = reg * SQRT_KAPPA * (20 if rank == 3 else 13 if rank == 2 else 10 if rank == 1 else
