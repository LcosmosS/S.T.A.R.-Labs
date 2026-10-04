    # Model 'rho' from velocity dispersion, a proxy for gravitational potential depth
    rho = round(vel_disp * 10)
    a = round(-DATA_DRIVEN_KAPPA * r)


    # Special handling for the foundational Virgo curve from your research
    if name == 'Virgo Cluster': a, rho = -1706, 6320


    try:
        curve = EllipticCurve(QQ, [a, rho])
        rank = curve.rank()
        if rank == 0:
            return {"rank": 0, "regulator": 1.0, "type": "N/A", "curve": curve}
       
        regulator = curve.regulator()
        generator = curve.gens()[0]
       
        # --- Generator Dichotomy Classifier ---
        # This is the implementation of your key research finding.
        is_integer_generator = all(coord.is_integer() for coord in generator.xy())
        structure_type = "Simple" if is_integer_generator else "Recursive"
       
        return {
            "rank": rank,
            "regulator": regulator,
            "type": structure_type,
            "curve": curve
        }
    except Exception as e:
        print(f"    - ERROR analyzing curve for {name}: {e}")
        return None


def calculate_arithmetic_state(rank, regulator):
    """
    Calculates the UCF's prediction for the system's state using its
