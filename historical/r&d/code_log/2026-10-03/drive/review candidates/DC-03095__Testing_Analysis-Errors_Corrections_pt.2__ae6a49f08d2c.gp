E = ellinit([0, 0, 0, a, b], 1); \\ 1 indicates working over Q


\\ Compute the discriminant
delta = E.disc;
print("Discriminant: ", delta);
if(delta == 0, print("Not an elliptic curve (singular). Skipping."); next);


\\ Compute the conductor
conductor = ellglobalred(E)[1];
print("Conductor: ", conductor);


\\ Compute the torsion subgroup order
tors = elltors(E);
tors_order = tors[1];
print("Torsion subgroup order: ", tors_order);


\\ Compute the algebraic rank
rank_data = ellrank(E);
alg_rank = rank_data[1];
print("Algebraic rank: ", alg_rank);


\\ Compute the L-function and analytic rank
L = elllseries(E, 1); \\ Evaluate L(E, s) at s=1
if(abs(L) < 1e-10,
    L_deriv = elllseries(E, 1, 1); \\ First derivative L'(E, 1)
    if(abs(L_deriv) < 1e-10,
        L_deriv2 = elllseries(E, 1, 2); \\ Second derivative L''(E, 1)
        if(abs(L_deriv2) < 1e-10,
            analytic_rank = 3; leading_coeff = L_deriv2 / 2;
        ,
            analytic_rank = 2; leading_coeff = L_deriv2 / 2;
        );
    ,
        analytic_rank = 1; leading_coeff = L_deriv;
    );
,
    analytic_rank = 0; leading_coeff = L;
