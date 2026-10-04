from sage.all import EllipticCurve, QQ, factor, RealField
from sage.schemes.elliptic_curves.sha_tate import Sha

def analyze_curve(a, b, is_original=False):
    print(f"\n{'Original curve' if is_original else 'Fibonacci curve'}: y² = x³ + {a}x + {b}")

    # Define the elliptic curve
    try:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
    except ValueError as e:
        print(f"Error creating curve: {e}")
        return

    # Compute basic invariants
    delta = E.discriminant()
    conductor = factor(E.conductor())
    tors_order = E.torsion_subgroup().order()
    print(f"Discriminant: {delta}")
    print(f"Conductor: {conductor}")
    print(f"Torsion order: {tors_order}")

    # Compute algebraic rank carefully
    try:
        rank = E.rank()
        print(f"Algebraic rank: {rank}")
    except:
        print("Algebraic rank computation failed")
        rank = None

    # Compute analytic rank and leading coefficient
    L = E.lseries()
    dok = L.dokchitser(prec=100)
    L1 = dok(1)
    if abs(L1) < 1e-10:
        try:
            L1_deriv = dok.derivative(1, 1)
            if abs(L1_deriv) < 1e-10:
                L1_deriv2 = dok.derivative(1, 2)
                analytic_rank = 2
                leading_coeff = L1_deriv2 / 2