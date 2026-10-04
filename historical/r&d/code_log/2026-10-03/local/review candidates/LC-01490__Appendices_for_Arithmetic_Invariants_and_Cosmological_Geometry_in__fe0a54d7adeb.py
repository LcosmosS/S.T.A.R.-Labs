# Stage 2: Adaptive Denominator Analysis
# =========================================
print("\n--- Stage 2: Adaptive Denominator Analysis ---")

def find_denominator_rule(denominators_df):
    non_one_denominators = (denominators_df != 1).sum().sum()
    total_denominators = denominators_df.size
    fractional_percentage = (non_one_denominators / total_denominators) * 100
    print(f"Analyzing training data denominators: {fractional_percentage:.2f}% are
