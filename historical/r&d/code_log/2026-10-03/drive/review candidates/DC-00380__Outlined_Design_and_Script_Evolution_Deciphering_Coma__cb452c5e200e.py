# Create a DataFrame for easier analysis
df = pd.DataFrame(analysis_results)
df['x_coord'] = df['generator'].apply(lambda p: p[0])
df['y_coord'] = df['generator'].apply(lambda p: p[1])
df['x_num'] = df['x_coord'].apply(lambda x: x.numerator())
df['x_den'] = df['x_coord'].apply(lambda x: x.denominator())
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
