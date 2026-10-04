    if fractional_percentage > 50:
        print("Adopting 'Recursive' denominator rule based on Coma pattern.")
        return lambda n: 3**(2*n + 2)
    else:
        print("Adopting 'Simple' denominator rule based on Perseus pattern.")
        return lambda n: 1

denominator_func = find_denominator_rule(df[['x_den', 'y_den']])
print(f"Selected denominator function: f(1)={denominator_func(1)},
f(2)={denominator_func(2)}")
print("--- Stage 2 Complete ---")

# Stage 3: Modeling Numerators and Exchange Rate
# ===============================================================
print("\n--- Stage 3: Modeling Numerators and Exchange Rate ---")

df['exchange_rate'] = df['y_coord'] / df['r']
df['regulator'] = df['curve_obj'].apply(lambda E: E.regulator() if E.rank() > 0 else
