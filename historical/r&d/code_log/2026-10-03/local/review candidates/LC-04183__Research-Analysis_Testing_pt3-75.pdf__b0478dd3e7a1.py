with open("failed_curves.txt", "w") as f:
    f.write("a,b,conductor,reason\n")
with open("rank3_curves.txt", "w") as f:
    f.write("a,b,rank,selmer3,volume\n")
with open("unique_curves.txt", "w") as f:
    f.write("a,b,rank,omega,reg,volume,scaled_reg,leading_coeff,conductor,plot_file\n")

while successful_curves < max_successful_curves and attempts < max_total_attempts:
    force_failure = (attempts % 5 == 0 and attempts > 0 and len(set(y_data)) < 2)
    if attempts % 10 == 0 and len(X_data) >= 10 and len(set(y_data)) >= 2:
        print("\nTraining logistic regression classifier...")
        classifier = LogisticRegression(max_iter=1000, class_weight={1: 50, 0: 1})
        if X_data:
