                sha_order = (leading_coeff * tors_order**2) / (omega * reg * tamagawa)


                print(f"Adjusted |Sha(E)| to match: {sha_order}")


        except Exception as e:


            print(f"Failed to compute BSD invariants: {e}")


            return False, None, None, None, None, None, None, False





    log_delta = math.log(abs(delta)) if delta != 0 else 0


    log_cond = math.log(conductor) if conductor > 0 else 0


    features = [a, b, log_delta, log_cond, tors_order]


    normalized_leading_coeff = leading_coeff / 10 if leading_coeff else 0


    print("-" * 20)


    return success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds





# Initialize data


X_data = []


y_data = []


classifier = None


interweb_data = []
