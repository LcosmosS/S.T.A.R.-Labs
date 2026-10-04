    # Predict numerators using the trained linear models
    predicted_x_num = model_x_num.predict(np.array([[r, rho]]))[0]
    predicted_y_num = model_y_num.predict(np.array([[r, rho]]))[0]

    # Calculate denominators using the discovered rule
    # Assuming x_den is step 1 and y_den is step 2
    predicted_x_den = denominator_func(1)
    predicted_y_den = denominator_func(2)

    # Construct the rational coordinates
    predicted_x = QQ(round(predicted_x_num), predicted_x_den)
    predicted_y = QQ(round(predicted_y_num), predicted_y_den)

    return (predicted_x, predicted_y)

# 4.1: Predict the generator for the holdout cluster
holdout_r = holdout_result['r']
holdout_rho = holdout_result['rho']
predicted_gen_coords = predict_generator(holdout_r, holdout_rho)

# 4.2: Get the actual generator for the holdout cluster
actual_gen = holdout_result['generator']
actual_gen_coords = (actual_gen[0], actual_gen[1])

# 4.3: Compare prediction to reality
print(f"\nValidation for Holdout Cluster: {HOLDOUT_CLUSTER}")
print(f"  Physical Inputs: r={holdout_r}, rho={holdout_rho}")
print(f"  Predicted Generator: {predicted_gen_coords}")
print(f"  Actual Generator:    {actual_gen_coords}")
