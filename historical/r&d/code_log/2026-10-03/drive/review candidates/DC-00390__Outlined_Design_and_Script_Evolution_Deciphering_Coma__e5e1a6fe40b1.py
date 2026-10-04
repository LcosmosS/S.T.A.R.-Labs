    # Calculate the percentage of denominators that are not 1
    non_one_denominators = (denominators_df != 1).sum().sum()
    total_denominators = denominators_df.size
    fractional_percentage = (non_one_denominators / total_denominators) * 100
    
    print(f"Analyzing training data denominators: {fractional_percentage:.2f}% are fractional.")


    # If more than 50% of denominators are fractional, assume the Coma-like rule applies.
    # Otherwise, assume the Perseus-like (integer) rule applies.
    if fractional_percentage > 50:
        print("Adopting 'Recursive' denominator rule based on Coma pattern.")
        # Rule from your exploratory script
        return lambda n: 3**(2*n + 2)
    else:
        print("Adopting 'Simple' denominator rule based on Perseus pattern.")
        return lambda n: 1


denominator_func = find_denominator_rule(df[['x_den', 'y_den']])
print(f"Selected denominator function: f(1)={denominator_func(1)}, f(2)={denominator_func(2)}")
print("--- Stage 2 Complete ---")




# Stage 3: Modeling Numerators and Exchange Rate
# ===============================================================
# (No changes in this stage)
print("\n--- Stage 3: Modeling Numerators and Exchange Rate ---")


df['exchange_rate'] = df['y_coord'] / df['r']
df['regulator'] = df['curve_obj'].apply(lambda E: E.regulator() if E.rank() > 0 else 1.0)
print("\nExchange Rate Analysis:")
print(df[['cluster', 'r', 'y_coord', 'exchange_rate', 'regulator']])


X_train = df[['r', 'rho']]
y_train_x_num = df['x_num']
y_train_y_num = df['y_num']
model_x_num = LinearRegression().fit(X_train, y_train_x_num)
model_y_num = LinearRegression().fit(X_train, y_train_y_num)


print("\nNumerator Model Coefficients (Linear):")
print(f"  x_num = {model_x_num.coef_[0]:.2f}*r + {model_x_num.coef_[1]:.2f}*rho + {model_x_num.intercept_:.2f}")
print(f"  y_num = {model_y_num.coef_[0]:.2f}*r + {model_y_num.coef_[1]:.2f}*rho + {model_y_num.intercept_:.2f}")
print("--- Stage 3 Complete ---")




# Stage 4: Synthesis and Predictive Validation
# ============================================


print("\n--- Stage 4: Synthesizing and Validating the Model ---")


# --- INCORPORATED THE NotImplementedError FIX IN THIS FUNCTION ---
def predict_generator(r, rho):
    """
    Synthesized model to predict a generator from physical inputs.
