        E_sage = EllipticCurve(QQ, [a, b])

        try:
            rank = E_sage.rank(algorithm='pari')
        except (RuntimeError, ArithmeticError) as e:
            print(f"  SKIPPED: Rank computation failed: {e}")
            return None

        if rank == 1:
            generator = E_sage.gens()[0]
            print(f"  \033[92mSUCCESS: Rank 1 curve found!\033[0m")
            return {'cluster': cluster_name, 'rank': rank, 'generator':
str(generator)}
        else:
            print(f"  SKIPPED: Predicted rank is {rank}, not 1.")
            return None

    except (SignalError, TypeError, ValueError) as e: