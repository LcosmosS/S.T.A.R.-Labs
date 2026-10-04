# 4.4: Success Criterion Check
x_match = (predicted_gen_coords[0] == actual_gen_coords[0])
y_match = (predicted_gen_coords[1] == actual_gen_coords[1])

if x_match and y_match:
    print("\nSUCCESS CRITERION MET: Predicted generator matches actual generator.")
else:
    print("\nSUCCESS CRITERION FAILED: Prediction does not match.")

print("\n--- Pipeline Finished ---")
