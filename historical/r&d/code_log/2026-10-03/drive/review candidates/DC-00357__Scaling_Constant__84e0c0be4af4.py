    try:
        curve = EllipticCurve(QQ, [a, rho])
        rank = curve.rank()
        if rank == 0: return {"rank": 0, "regulator": 1.0}
        regulator = curve.regulator()
        return {"rank": rank, "regulator": regulator}
    except Exception as e:
        print(f"    - ERROR analyzing curve for {name}: {e}")
        return None


def calculate_informational_potential(rank, regulator, upsilon):
    """
    Calculates the Informational Potential, I(A) = ϒ * f(Rank, Regulator).
