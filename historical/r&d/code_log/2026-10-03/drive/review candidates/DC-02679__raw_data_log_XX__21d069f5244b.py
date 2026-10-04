print("S.T.A.R. INVERSE b PIPELINE RESULTS")
print("="*80)
for name, r, b, mass, v_disp, r_mpc in clusters:
    try:
        P_pred, rho_recovered = predict_star_generator(r, b, mass, v_disp, r_mpc)
        a = -round(31.59259 * r)
        E = EllipticCurve(QQ, [a, b])
        E.two_descent(second_limit=20, verbose=False)
        rank_actual = E.rank(only_use_mwrank=False)
        gens = E.gens()
        P_actual = gens[0] if rank_actual > 0 else None
    except Exception as e:
        print(f"{name}: ERROR - {e}")
        continue
    
    match = (P_actual is not None and P_pred == P_actual)
    
    print(f"{name:10} | r={r:3} | b={b:5} | ρ_rec={rho_recovered:5} | Rank={rank_actual} | Match={'YES' if match else 'NO'}")
    print(f"   Pred: {P_pred}")
    if P_actual:
        print(f"   Actl: {P_actual}")
    print("-"*80)
