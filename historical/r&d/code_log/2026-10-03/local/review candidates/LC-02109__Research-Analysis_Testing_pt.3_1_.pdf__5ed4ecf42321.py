                print("Strong BSD holds: Leading coefficient matches with |Sha(E)| = 1")


            else:


                print("Strong BSD fails: Leading coefficient does not match with |Sha(E)| = 1")


                sha_order = (leading_coeff * tors_order**2) / (omega * reg * tamagawa)


                print(f"Adjusted |Sha(E)| to match: {sha_order}")


        except Exception as e:


            print(f"Failed to compute BSD invariants: {e}")


            return False, None, None





    log_delta = math.log(abs(delta)) if delta != 0 else 0


    log_cond = math.log(conductor) if conductor > 0 else 0


    features = [a, b, log_delta, log_cond, tors_order]


    print("-" * 20)


    return success, features, rank





# Initialize data


X_data = []


y_data = []


classifier = None