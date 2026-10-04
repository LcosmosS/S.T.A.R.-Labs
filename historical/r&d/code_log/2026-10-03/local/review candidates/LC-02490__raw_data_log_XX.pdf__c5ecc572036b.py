print("S.T.A.R. INVERSE b PIPELINE RESULTS")
print("="*80)
for name, r, b, mass, v_disp, r_mpc in clusters:
    try:
        P_pred, rho_recovered = predict_star_generator(r, b, mass, v_disp, r_mpc)
        a = -round(31.59259 * r)
        E = EllipticCurve(QQ, [a, b])
        E.two_descent(second_limit=20, verbose=False)
        rank_actual = E.rank(only_use_mwrank=False)