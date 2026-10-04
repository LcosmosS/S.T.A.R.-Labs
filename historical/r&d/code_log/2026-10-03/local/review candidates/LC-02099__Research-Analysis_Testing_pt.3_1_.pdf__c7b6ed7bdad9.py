        X_data.append(features)

        y_data.append(success)

    if success:

        successful_curves += 1

    attempts += 1



# Analyze original curve

print(f"\nAnalyzing original curve")
success, features = analyze_curve(-1706, 6320, is_original=True)

if features:

    X_data.append(features)

    y_data.append(success)



print(f"\nCompleted: {successful_curves} successful curves analyzed out of {attempts} attempts")

if X_data:

    print("\nFinal classifier data summary:")

    print(f"Total curves analyzed: {len(X_data)}")

    print(f"Success rate: {sum(y_data) / len(y_data):.2%}")
