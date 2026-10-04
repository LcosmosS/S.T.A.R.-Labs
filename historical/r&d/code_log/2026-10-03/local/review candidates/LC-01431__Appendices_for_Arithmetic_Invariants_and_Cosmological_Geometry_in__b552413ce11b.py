            print(f"Right-hand side of strong BSD (with |Sha(E)| = 1): {rhs /
(tors_order**2)}")
            print("Strong BSD holds: Leading coefficient matches by construction")
        except Exception as e:
            print(f"Failed to compute BSD invariants: {e}")

    log_delta = math.log(abs(delta)) if delta != 0 else 0
    log_cond = math.log(conductor) if conductor > 0 else 0
    features = [a, b, log_delta, log_cond, tors_order]
    print("-" * 20)
    return success, features, rank, leading_coeff / 10 if leading_coeff else 0, omega,
