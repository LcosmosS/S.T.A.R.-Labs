            print(f"Real period (Omega): {omega} (3-sphere scale factor)")


            print(f"Regulator: {reg} (node interaction strength)")


            print(f"Product of Tamagawa numbers: {tamagawa} (local edge constraints)")


            print(f"Right-hand side of strong BSD (with |Sha(E)| = 1): {rhs}")





            if abs(leading_coeff - rhs) < 1e-10:


                print("Strong BSD holds: Leading coefficient matches with |Sha(E)| = 1")


            else:


                print("Strong BSD fails: Leading coefficient does not match with |Sha(E)| = 1")


                sha_order = (leading_coeff * tors_order**2) / (omega * reg * tamagawa)


                print(f"Adjusted |Sha(E)| to match: {sha_order}")


        except Exception as e:


            print(f"Failed to compute BSD invariants: {e}")


            return False, None, None, None, None, None, None





    log_delta = math.log(abs(delta)) if delta != 0 else 0


    log_cond = math.log(conductor) if conductor > 0 else 0


    features = [a, b, log_delta, log_cond, tors_order]


    normalized_leading_coeff = leading_coeff / 10 if leading_coeff else 0  # Normalize for Virgo height