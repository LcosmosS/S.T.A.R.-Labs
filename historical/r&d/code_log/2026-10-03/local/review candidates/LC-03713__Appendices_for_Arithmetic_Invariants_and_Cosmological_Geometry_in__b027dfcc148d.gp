    conductor = ellglobalred(E)[1];
    print("Conductor: ", conductor);

    \\ Torsion subgroup
    tors = elltors(E);
    tors_order = tors[1];
    print("Torsion subgroup order: ", tors_order);

    \\ Algebraic Rank
    rank_data = ellrank(E);
    alg_rank = rank_data[1];
    print("Algebraic rank: ", alg_rank);

    \\ --- Analytic Rank Calculation (BSD) ---
    L0 = elllseries(E, 1);
    if(abs(L0) > 1e-9,
        analytic_rank = 0;
        leading_coeff = L0,
        \\ L(E, 1) is zero, check first derivative
        L1 = elllseries(E, 1, 1);
        if(abs(L1) > 1e-9,
            analytic_rank = 1;
            leading_coeff = L1,
            \\ L'(E, 1) is zero, check second derivative
            L2 = elllseries(E, 1, 2);
            if(abs(L2) > 1e-9,
