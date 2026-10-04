    print(f"\nProcessing cluster: {cluster_name}")
    try:
        # Predict coefficients using the Virgo-calibrated kappa [cite: 402]
        a_predicted = -VIRGO_CALIBRATED_KAPPA * r
        b_predicted = rho
        
        # Round 'a' as is standard for number-theoretic investigations [cite: 404]
        a = round(a_predicted)
        b = b_predicted
        
        print(f"  Derived curve: y^2 = x^3 + {a}x + {b}")
        
        # Define the curve in SageMath
        E = EllipticCurve(QQ, [a, b])
        
        # Compute algebraic rank and generator
        rank = E.rank()
        
        if rank == 1:
            generator = E.gens()[0]
            print(f"  SUCCESS: Rank 1 curve found.")
            print(f"  Generator: {generator}")
            return {
                'cluster': cluster_name, 'r': r, 'rho': rho,
                'a': a, 'b': b, 'rank': rank, 'generator': generator,
                'curve_obj': E
            }
        else:
            print(f"  SKIPPED: Predicted rank is {rank}, not 1.")
            return None
            
    except Exception as e:
        print(f"  ERROR processing {cluster_name}: {e}")
        return None


# Process all clusters except the holdout case
analysis_results = []
for name, data in cluster_data.items():
    if name != HOLDOUT_CLUSTER:
        result = derive_and_analyze_cluster_curve(name, data['r'], data['rho'])
        if result:
            analysis_results.append(result)


# Process the holdout cluster separately for validation later
holdout_result = derive_and_analyze_cluster_curve(HOLDOUT_CLUSTER,
                                                   cluster_data[HOLDOUT_CLUSTER]['r'],
                                                   cluster_data[HOLDOUT_CLUSTER]['rho'])
