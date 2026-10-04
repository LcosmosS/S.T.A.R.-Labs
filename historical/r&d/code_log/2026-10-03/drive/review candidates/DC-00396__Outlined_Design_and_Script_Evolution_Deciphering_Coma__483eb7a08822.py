    predicted_x_num_numpy = model_x_num.predict(np.array([[r, rho]]))[0]
    predicted_y_num_numpy = model_y_num.predict(np.array([[r, rho]]))[0]
    
    py_float_x = predicted_x_num_numpy.item()
    py_float_y = predicted_y_num_numpy.item()


    predicted_x_den = denominator_func(1)
    predicted_y_den = denominator_func(2)
    
    # Use Sage's Integer() for robust conversion from a potentially huge float
    sage_int_x = Integer(round(py_float_x))
    sage_int_y = Integer(round(py_float_y))


    predicted_x = QQ(sage_int_x, predicted_x_den)
    predicted_y = QQ(sage_int_y, predicted_y_den)
    
    return (predicted_x, predicted_y)


holdout_r = holdout_result['r']
holdout_rho = holdout_result['rho']
predicted_gen_coords = predict_generator(holdout_r, holdout_rho)


actual_gen = holdout_result['generator']
actual_gen_coords = (actual_gen[0], actual_gen[1])


print(f"\nValidation for Holdout Cluster: {HOLDOUT_CLUSTER}")
print(f"  Physical Inputs: r={holdout_r}, rho={holdout_rho}")
print(f"  Predicted Generator: {predicted_gen_coords}")
print(f"  Actual Generator:    {actual_gen_coords}")


x_match = (predicted_gen_coords[0] == actual_gen_coords[0])
y_match = (predicted_gen_coords[1] == actual_gen_coords[1])


if x_match and y_match:
    print("\nSUCCESS CRITERION MET: Predicted generator matches actual generator.")
else:
    print("\nSUCCESS CRITERION FAILED: Prediction does not match.")
    
print("\n--- Pipeline Finished ---")
