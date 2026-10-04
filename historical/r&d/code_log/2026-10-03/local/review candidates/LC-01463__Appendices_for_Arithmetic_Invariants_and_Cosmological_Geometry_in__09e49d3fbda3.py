df['y_num'] = df['y_coord'].apply(lambda y: y.numerator())
df['y_den'] = df['y_coord'].apply(lambda y: y.denominator())

print("\n--- Stage 1 Complete: Foundational Dataset ---")
print(df[['cluster', 'r', 'rho', 'generator']])

# Stage 2: Recursive Grammar Analysis (Denominators)
# =================================================

print("\n--- Stage 2: Analyzing Denominator Structure ---")

def find_denominator_rule(denominators):
    """
    Analyzes a list of denominators to find a generating rule.
