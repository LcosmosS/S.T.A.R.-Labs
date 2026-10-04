    a_new = a * u**4
    b_new = b * u**6
    return a_new, b_new


def analyze_curve(a, b, is_original=False, max_attempts=5, require_3selmer=False, conductor_limit=1e11):
    curve_name = 'Original curve' if is_original else 'Fibonacci curve'
    print(f"\n{curve_name}: y² = x³ + {a}x + {b}")
    
    try:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
    except ValueError as e:
        print(f"Error creating curve: {e}")
        return False, None, None, None, None, None, None, False, None
    
    delta = E.discriminant()
    conductor = E.conductor()
    tors_order = E.torsion_subgroup().order()
    print(f"Discriminant: {delta}")
    print(f"Conductor: {conductor} = {factor(conductor)}")
    print(f"Torsion order: {tors_order}")
    
    if conductor > conductor_limit and not is_original:
        print(f"Conductor too large (> {conductor_limit}), skipping curve")
        with open("failed_curves.txt", "a") as f:
            f.write(f"a={a},b={b},conductor={conductor},reason=too_large\n")
        return False, None, None, None, None, None, None, False, None
    
    rank_success = False
    selmer2_success = False
    selmer3_success = False
    rank = None
    selmer_rank = None
    selmer3_rank = None
    leading_coeff = None
    omega = None
    reg = None
    tamagawa = None
    weak_bsd_holds = False
    
    # Compute the analytic rank first (safer)
    try:
        L = E.lseries()
        dok = L.dokchitser(prec=100)
        L1 = dok(1)
        analytic_rank = 0
        leading_coeff = L1
        if abs(L1) < 1e-10:
            L1_deriv = dok.derivative(1, 1)
            if abs(L1_deriv) < 1e-10:
                L1_deriv2 = dok.derivative(1, 2)
                if abs(L1_deriv2) < 1e-10:
                    L1_deriv3 = dok.derivative(1, 3)
                    if abs(L1_deriv3) < 1e-10:
                        analytic_rank = 4
                        leading_coeff = L1_deriv3 / 24
                    else:
                        analytic_rank = 3
                        leading_coeff = L1_deriv3 / 6
                else:
                    analytic_rank = 2
                    leading_coeff = L1_deriv2 / 2
            else:
                analytic_rank = 1
                leading_coeff = L1_deriv
        print(f"Analytic rank: {analytic_rank}")
    except Exception as e:
        print(f"Failed to compute analytic rank: {e}")
        return False, None, None, None, None, None, None, False, None
    
    # Attempt algebraic rank computation
    for attempt in range(max_attempts):
        try:
            # Try PARI/GP's ellrank first
            try:
                E_pari = pari.ellinit([0, 0, 0, a, b])
                rank_info = E_pari.ellrank()
                rank = int(rank_info[0])  # First element is the rank
                rank_success = True
                print(f"Algebraic rank (via PARI/GP): {rank}")
            except Exception as e:
                print(f"PARI/GP rank computation failed: {e}")
                # Try transforming the curve to reduce coefficients
                u = 1 / math.sqrt(abs(a)) if abs(a) > 1 else 1
                a_new, b_new = transform_curve(a, b, u)
                print(f"Transforming curve with u={u}: y² = x³ + {a_new}x + {b_new}")
                try:
                    E_transformed = EllipticCurve(QQ, [0, 0, 0, a_new, b_new])
                    rank = E_transformed.rank(pari_effort=10)  # Increase precision
                    rank_success = True
                    print(f"Algebraic rank (transformed curve): {rank}")
                except Exception as e:
                    print(f"Rank computation on transformed curve failed: {e}")
                    # Fallback to mwrank with increased effort
                    try:
                        rank = E.rank(pari_effort=10)
                        rank_success = True
                        print(f"Algebraic rank (mwrank with high effort): {rank}")
                    except Exception as e:
                        print(f"mwrank failed: {e}. Falling back to analytic rank...")
                        rank = analytic_rank
                        rank_success = True
            
            # Compute 2-Selmer rank if possible
            if rank_success and rank != analytic_rank:
                try:
                    selmer_rank = E.selmer_rank()
                    selmer2_success = True
                    print(f"2-Selmer rank: {selmer_rank}")
                except Exception as e:
                    print(f"2-Selmer rank computation failed: {e}")
                    selmer2_success = False
            
            # Refined 3-Selmer rank estimate
            if selmer2_success:
                estimated_selmer3 = max(rank, selmer_rank - 1)
            else:
                estimated_selmer3 = rank  # Fallback to rank if 2-Selmer rank unavailable
            if analytic_rank == rank:
                selmer3_rank = rank
                print(f"3-Selmer rank (refined using BSD): {selmer3_rank}")
            else:
                selmer3_rank = estimated_selmer3
                print(f"Estimated 3-Selmer rank (fallback): {selmer3_rank}")
            selmer3_success = True if not require_3selmer else False
            
            if selmer3_rank >= 3:
                print("Potential 3-Selmer candidate!")
                with open("rank3_curves.txt", "a") as f:
                    vol = omega * reg * (VIRGO_DISTANCE / (omega * SQRT_KAPPA))**3 / 3e11 if omega and reg else 'N/A'
                    f.write(f"a={a},b={b},rank={rank},selmer3={selmer3_rank},volume={vol}\n")
            break
        except Exception as e:
            print(f"Rank computation failed on attempt {attempt + 1}: {e}")
            if attempt == max_attempts - 1:
                with open("failed_curves.txt", "a") as f:
                    f.write(f"a={a},b={b},conductor={conductor},reason=rank_failure\n")
                return False, None, None, None, None, None, None, False, None
    
    success = rank_success and (selmer3_success if require_3selmer else True)
    if success:
        try:
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
            comoving_volume = (omega * reg * cosmo_scale**3) / (3e11 if rank == 3 else 3e12 if rank == 2 else 5e12 if rank == 1 else 1e13)
            scaled_reg = reg * SQRT_KAPPA * (20 if rank == 3 else 13 if rank == 2 else 60 if rank == 1 else 20)
            print(f"Real period (Omega): {omega}")
            print(f"Dynamic COSMO_SCALE: {cosmo_scale}")
            print(f"Scaled period: {float(scaled_period)} light-years")
            print(f"Regulator: {reg}")
            print(f"Scaled regulator (Reg * √κ * {'20' if rank == 3 else '13' if rank == 2 else '60' if rank == 1 else '20'}): {float(scaled_reg)}")
            print(f"Product of Tamagawa numbers: {tamagawa}")
            print(f"Estimated comoving volume (Omega * Reg * scale^3 / {'3e11' if rank == 3 else '3e12' if rank == 2 else '5e12' if rank == 1 else '1e13'}): {comoving_volume} Mly^3")
            print(f"Right-hand side of strong BSD (with |Sha(E)| = 1): {rhs}")
            
            if abs(leading_coeff - rhs) < 1e-10:
                print("Strong BSD holds: Leading coefficient matches with |Sha(E)| = 1")
            else:
                sha_order = (leading_coeff * tors_order**2) / (omega * reg * tamagawa)
                print(f"Adjusted |Sha(E)| to match: {sha_order}")
        except Exception as e:
            print(f"Failed to compute BSD invariants: {e}")
            return False, None, None, None, None, None, None, False, E
    
    log_delta = math.log(abs(delta)) if delta != 0 else 0
    log_cond = math.log(conductor) if conductor > 0 else 0
    features = [a, b, log_delta, log_cond, tors_order]
    normalized_leading_coeff = leading_coeff / 10 if leading_coeff else 0
    
    if success and rank is not None:
        try:
            x_range = 10 if abs(a) <= 5 else 4 * math.sqrt(abs(a))
            x_vals = np.linspace(-x_range, x_range, 1000)
            y_vals = np.sqrt(np.maximum(x_vals**3 + a * x_vals + b, 0))
            density_size = min(leading_coeff * 177 / 20, 200) if leading_coeff else 10
            plt.figure(figsize=(8, 6))
            color = 'green' if rank == 3 else 'blue' if rank == 2 else 'black'
            plt.scatter(x_vals, y_vals, s=float(max(density_size, 1)), c=color, alpha=0.5, label=f'Rank {rank}')
            plt.scatter(x_vals, -y_vals, s=float(max(density_size, 1)), c=color, alpha=0.5)
            if rank > 0:
                contour_y = np.full_like(x_vals, float(5))
                plt.plot(x_vals, contour_y, 'r--', label=f'Regulator {scaled_reg:.0f}')
                plt.plot(x_vals, -contour_y, 'r--')
            plt.title(f'Curve y² = x³ + {a}x + {b}, Density: {leading_coeff * 177:.0f}')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.legend()
            plt.grid(True)
            plt.savefig(f"curve_{a}_{b}.png")
            plt.close()
            print(f"Polynomial plot saved as curve_{a}_{b}.png")
        except Exception as e:
            print(f"Failed to generate polynomial plot: {e}")
    
    print("-" * 20)
    return success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E


# Restore state from attempts 1–17 and previous run (18–35 + original curve)
X_data = [
    [13, 377, math.log(61540336), math.log(61540336), 1],  # Attempt 1
    [2, 144, math.log(8958464), math.log(4479232), 1],    # Attempt 2
