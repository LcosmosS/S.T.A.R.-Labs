def analyze_curve(a, b, is_original=False, max_attempts=5, require_3selmer=False,
conductor_limit=1e14, descent_limit=20):

    curve_name = 'Original curve' if is_original else 'Fibonacci curve'

    print(f"\n{curve_name}: y² = x³ + {a}x + {b}")



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



    if conductor > conductor_limit and not is_original:

        print(f"Conductor too large (> {conductor_limit}), skipping curve")

        with open("failed_curves.txt", "a") as f:

            f.write(f"a={a},b={b},conductor={conductor},reason=too_large\n")

        return False, None, None, None, None, None, None, False, None, None



    rank_success = False

    selmer3_success = False

    rank = None

    selmer3_rank = None
    leading_coeff = None

    omega = None

    reg = None

    tamagawa = None

    weak_bsd_holds = False
