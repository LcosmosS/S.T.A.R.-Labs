        print("Strong BSD holds: Leading coefficient matches with |Sha(E)| = 1")
    else:
        print("Strong BSD fails: Leading coefficient does not match with |Sha(E)| = 1")
        sha_order = (leading_coeff * tors_order^2) / (omega * reg * tamagawa)
        print(f"Adjusted |Sha(E)| to match: {sha_order}")
