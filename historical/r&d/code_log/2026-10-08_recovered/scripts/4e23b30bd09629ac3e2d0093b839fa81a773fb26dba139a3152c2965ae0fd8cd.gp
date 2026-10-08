\\ Set precision to 38 decimal digits for 32-bit compatibility
\p 38

\\ Define the golden ratio
phi = (1 + sqrt(5)) / 2;

\\ Define pi
pi_val = Pi;

\\ Define the list of curves: [a, b] for y^2 = x^3 + a*x + b
curves = [[1, 2], [2, 1], [3, 2], [5, 3], [-1706, 6320]];

\\ Loop over each curve
for(i = 1, length(curves),
    a = curves[i][1]; b = curves[i][2];
    print("Curve: y^2 = x^3 + ", a, "x + ", b);

    \\ Initialize the elliptic curve over Q
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
    );
    print("Analytic rank: ", analytic_rank);
    print("Leading coefficient L^(r)(E, 1): ", leading_coeff);

    \\ Verify weak BSD
    if(alg_rank == analytic_rank,
        print("Weak BSD holds: Algebraic rank = Analytic rank");
    ,
        print("Weak BSD fails: Algebraic rank != Analytic rank");
    );

    \\ Compute the p-adic L-function at p=5
    p = 5;
    try = {
        L_padic = ellpadiclseries(E, p, 10); \\ Compute p-adic L-series up to 10 terms
        L_padic_val = subst(L_padic, 'x, 1); \\ Evaluate at s=1 (x = t^(s-1), so s=1 means x=1)
        print("p-adic L-function at s=1 (p=", p, "): ", L_padic_val);
        if(abs(L_padic_val) < 1e-10,
            print("p-adic L-function suggests higher rank");
        ,
            print("p-adic L-function suggests rank 0");
        );
    };
    iferr(try, err, print("Failed to compute p-adic L-function: ", err));

    \\ Compute BSD invariants
    omega = ellomega(E)[1]; \\ Real period
    omega_scaled = pi_val * omega; \\ Scale by pi
    if(alg_rank == 0,
        reg = 1.0;
    ,
        gens = ellgenerators(E);
        if(length(gens) > 0,
            reg = ellheight(E, gens[1]); \\ Height of the first generator
        ,
            reg = 1.0; \\ Fallback if no generators found
        );
    );
    reg_scaled = phi * reg; \\ Scale by golden ratio
    tamagawa = prod(elllocalred(E, prime)[2] | prime <- factor(conductor)[,1]); \\ Product of Tamagawa numbers

    \\ Use Fibonacci substitution for |Sha(E)|
    sha_order = 5; \\ F_5

    \\ Compute the right-hand side of the strong BSD formula with our modifications
    rhs = (omega_scaled * reg_scaled * sha_order * tamagawa) / (tors_order^2);
    print("Scaled real period (Omega * pi): ", omega_scaled);
    print("Scaled regulator (Reg * phi): ", reg_scaled);
    print("Product of Tamagawa numbers: ", tamagawa);
    print("Right-hand side of modified strong BSD: ", rhs);

    \\ Use Fibonacci substitution for leading coefficient
    modified_leading_coeff = 8; \\ F_6
    print("Modified leading coefficient (F_6): ", modified_leading_coeff);

    \\ Verify modified strong BSD
    if(abs(modified_leading_coeff - rhs) < 1e-5,
        print("Modified strong BSD holds with Fibonacci, pi, and phi substitutions");
    ,
        print("Modified strong BSD fails with Fibonacci, pi, and phi substitutions");
        adjusted_sha = (modified_leading_coeff * tors_order^2) / (omega_scaled * reg_scaled * tamagawa);
        print("Adjusted |Sha(E)| to match: ", adjusted_sha);
    );

    print("");
);