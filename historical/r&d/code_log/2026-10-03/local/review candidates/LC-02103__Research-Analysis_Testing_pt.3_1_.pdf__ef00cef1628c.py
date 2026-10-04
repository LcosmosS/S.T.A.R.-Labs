    try:


        E = EllipticCurve(QQ, [0, 0, 0, a, b])


    except ValueError as e:


        print(f"Error creating curve: {e}")


        return False, None, None





    delta = E.discriminant()


    conductor = E.conductor()


    tors_order = E.torsion_subgroup().order()


    print(f"Discriminant: {delta}")


    print(f"Conductor: {conductor} = {factor(conductor)}")


    print(f"Torsion order: {tors_order} (cyclic nodes in 3-sphere interweb)")





    rank_success = False


    selmer2_success = False


    selmer3_success = False


    rank = None


    selmer_rank = None