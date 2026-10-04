    # Optionally, attempt generation for small n and append if successful
    phi = (1 + QQ(5).sqrt()) / 2
    for n in range(1, 11):  # Limit to small n=1-10 to avoid large number issues
        seqs = [
            fibonacci(n),  # Fibonacci
            lucas_number2(n, 1, -1),  # Lucas
            floor(phi * n)  # Golden ratio approx
        ]
        for a_base in seqs:
            for b_base in seqs:
                for scalar_a in scalars:
                    for scalar_b in scalars:
                        a = scalar_a * a_base
                        b = scalar_b * b_base
                        try:
                            E = EllipticCurve(QQ, [0, 0, 0, a, b])
                            disc = E.discriminant()
                            if disc != 0:
                                try:
                                    N = E.conductor()
                                    abs_disc = abs(disc)
                                    r = E.rank(only_bounds=True)[0]
                                    curves.append({'label': f'E_{a}_{b}', 'N': N, 'Delta': abs_disc, 'r': r})
                                except Exception:
                                    pass  # Skip if conductor/rank fails
                        except Exception:
                            pass  # Skip invalid curves
    # Deduplicate by Delta
    unique_curves = {c['Delta']: c for c in curves}.values()
    return list(unique_curves)


# Step 2: Project curves to 3D coordinates (phi, theta, z)
def project_curves(curves, alpha=200):
    deltas = [c['Delta'] for c in curves if c['Delta'] > 0]
    ns = [c['N'] for c in curves]
