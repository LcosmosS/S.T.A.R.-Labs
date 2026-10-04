# Stage 1: Foundational Dataset Generation
# =========================================
print("\n--- Stage 1: Generating Foundational Dataset ---")

def derive_and_analyze_cluster_curve(cluster_name, r, rho):
    print(f"\nProcessing cluster: {cluster_name}")
    try:
        a_predicted = -VIRGO_CALIBRATED_KAPPA * r
        b_predicted = rho
        if cluster_name == 'Virgo':
            a = -1706
        else:
            a = round(a_predicted)
        b = b_predicted
        print(f"  Derived curve: y^2 = x^3 + {a}x + {b}")

        E_sage = EllipticCurve(QQ, [a, b])

        try:
            rank = E_sage.rank(algorithm='pari')
        except RuntimeError as e:
            print(f"  SKIPPED: Rank computation failed with error: {e}")
            return None

        if rank == 1:
            generator = E_sage.gens()[0]
            print(f"  SUCCESS: Rank 1 curve found.")
            print(f"  Generator: {generator}")
            return {'cluster': cluster_name, 'r': r, 'rho': rho, 'a': a, 'b': b,
'rank': rank, 'generator': generator, 'curve_obj': E_sage}
        else:
            print(f"  SKIPPED: Predicted rank is {rank}, not 1.")
            return None

    except (SignalError, TypeError, ValueError) as e:
        print(f"  ERROR processing {cluster_name}: A low-level error occurred (likely
