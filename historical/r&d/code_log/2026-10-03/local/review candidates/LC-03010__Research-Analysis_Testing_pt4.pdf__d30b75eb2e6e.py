math.log(48766972889600), math.log(12191743222400)),
    (17711, 46368, 3, 90.123456789012 / 10, 0.321456789012345, 46.7890123456789, 2, True,
math.log(193964465342464), math.log(48491116335616)),
    (987, 610, 0, 1.3318189706830563230543242301 / 10, 0.66590948534152816152716211506, 1.0, 2,
True, math.log(61697054592), math.log(253897344)),
    (610, 1597, 0, 1.5375354317386584983301355052 / 10, 0.76876771586932924916506775259, 1.0, 2,
True, math.log(15628560688), math.log(7814280344)),
    (1597, 4181, 2, 34.467712331727546458459266382 / 10, 0.59845828114740869987664084021,
28.797088633850538753730327173, 2, True, math.log(268223891824), math.log(38317698832)),
]

# Updated analyze_curve function (same as before, included for completeness)
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
    selmer2_success = False
    selmer3_success = False
    rank = None
    selmer_rank = None
    selmer3_rank = None
    leading_coeff = None
    omega = None
    reg = None
    tamagawa = None
    weak_bsd_holds = False
