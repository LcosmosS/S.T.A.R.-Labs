compute_selmer_ranks(a, b) = {
    E = ellinit([0, 0, 0, a, b], 1);
    print("\nCurve: y^2 = x^3 + ", a, "x + ", b);
    delta = elldisc(E);
    conductor = ellglobalred(E)[1];
    print("Discriminant: ", delta);
    print("Conductor: ", conductor);
    tors = elltors(E);
    tors_order = tors[1];
    print("Torsion order: ", tors_order);
    if (conductor > 7e9, 
        print("Conductor too large, skipping curve");
        return
    );
    selmer_group = ellselmer(E);
    selmer2_rank = length(selmer_group);
    print("2-Selmer rank: ", selmer2_rank);
    alg_rank = ellrank(E)[1];
    print("Algebraic rank: ", alg_rank);
    est_selmer3_rank = max(alg_rank, selmer2_rank - 1);
    print("Estimated 3-Selmer rank: ", est_selmer3_rank);
    if (est_selmer3_rank >= 3,
        print("Potential 3-Selmer candidate!")
    );
}

curves = [
    [5, 233], [2, 233], [2, 144], [5, 144], [34, 377], [1597, 2], [34, 610], [34, 233],
    [2, 377], [89, 144], [8, 144], [13, 144], [5, 377], [5, 610], [5, 987], [3, 144],
    [13, 377], [55, 144], [21, 144], [8, 610], [8, 21], [2, 13], [3, 233], [377, 13],
    [144, 5], [377, 21], [55, 8], [89, 377], [55, 233], [377, 34], [-1706, 6320]
];

for(i=1, length(curves),
    compute_selmer_ranks(curves[i][1], curves[i][2])
);