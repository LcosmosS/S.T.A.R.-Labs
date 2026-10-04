    # Predict numerators using the trained linear models
    predicted_x_num_float = model_x_num.predict(np.array([[r, rho]]))[0]
    predicted_y_num_float = model_y_num.predict(np.array([[r, rho]]))[0]
    
    # Calculate denominators using the adaptively selected rule from Stage 2
    predicted_x_den = denominator_func(1)
    predicted_y_den = denominator_func(2)
    
    # Convert the float to a standard integer BEFORE passing to QQ()
    predicted_x = QQ(int(round(predicted_x_num_float)), predicted_x_den)
    predicted_y = QQ(int(round(predicted_y_num_float)), predicted_y_den)
    
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
