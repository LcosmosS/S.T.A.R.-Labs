    try:

        E = EllipticCurve(QQ, [0, 0, 0, a, b])
    except ValueError as e:
        print(f"Error creating curve: {e}")
        return False, None, None, None, None, None, None, False, None, None


    delta = E.discriminant()
    conductor = E.conductor()
    tors_order = E.torsion_subgroup().order()
    print(f"Discriminant: {delta}")
    print(f"Conductor: {conductor} = {factor(conductor)}")

    print(f"Torsion order: {tors_order}")

    if conductor > conductor_limit:
        print(f"Conductor too large (> {conductor_limit}), skipping curve")
        return False, None, None, None, None, None, None, False, None, None


    rank_success = False
    rank = None
    selmer3_rank = None
    leading_coeff = None
    omega = None

    reg = None
    tamagawa = None
    weak_bsd_holds = False

    try:

        L = E.lseries()