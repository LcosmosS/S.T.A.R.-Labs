curves = [[1, 2], [2, 1], [3, 2], [5, 3], [-1706, 6320]];
p = 5;
phi = (1 + sqrt(5))/2;
pi_val = Pi;
for(i = 1, length(curves),
    a = curves[i][1]; b = curves[i][2];
    print("Curve: y^2 = x^3 + ", a, "x + ", b);
    E = ellinit([0, 0, 0, a, b], 1);
    disc = -16*(4*a^3 + 27*b^2);
    print("Discriminant: ", disc);
    conductor = ellglobalred(E)[1];
    print("Conductor: ", conductor);
    tors = elltors(E);
    tors_order = tors[1];
    print("Torsion subgroup order: ", tors_order);
    rank_data = ellrank(E);
    alg_rank = rank_data[1];
    print("Algebraic rank: ", alg_rank);
    L = elllseries(E, 1);
    if(abs(L) < 1e-10,
        analytic_rank = 0;
        L = elllseries(E, 1, alg_rank);
    ,
        L_deriv = elllseries(E, 1, 1);
        if(abs(L_deriv) < 1e-10,
            analytic_rank = 1;
            L = elllseries(E, 1, alg_rank);
        ,
            L_deriv2 = elllseries(E, 1, 2);
            if(abs(L_deriv2) < 1e-10,
                analytic_rank = 2;
                L = elllseries(E, 1, alg_rank);
            ,
                analytic_rank = 3;
                L = elllseries(E, 1, alg_rank);
            );
        );
