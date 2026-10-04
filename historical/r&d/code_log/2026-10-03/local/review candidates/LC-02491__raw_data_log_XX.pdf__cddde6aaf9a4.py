        gens = E.gens()
        P_actual = gens[0] if rank_actual > 0 else None
    except Exception as e:
        print(f"{name}: ERROR - {e}")
        continue

    match = (P_actual is not None and P_pred == P_actual)

    print(f"{name:10} | r={r:3} | b={b:5} | ρ_rec={rho_recovered:5} | Rank={rank_actual} | Match={'YES' if
