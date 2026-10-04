# Create a DataFrame for easier analysis
df = pd.DataFrame(analysis_results)


print("\n--- Stage 1 Complete: Foundational Dataset ---")
if not df.empty:
    df['x_coord'] = df['generator'].apply(lambda p: p[0])
    df['y_coord'] = df['generator'].apply(lambda p: p[1])
    df['x_num'] = df['x_coord'].apply(lambda x: x.numerator())
    df['x_den'] = df['x_coord'].apply(lambda x: x.denominator())
    df['y_num'] = df['y_coord'].apply(lambda y: y.numerator())
    df['y_den'] = df['y_coord'].apply(lambda y: y.denominator())
    print("Training Dataset:")
    print(df[['cluster', 'r', 'rho', 'generator']])
else:
    print("Training Dataset is empty.")




# --- ADDED VALIDATION BLOCK FROM PREVIOUS RESPONSE ---
if holdout_result is None:
    print(f"\n\033[91mCRITICAL PIPELINE ERROR:\033[0m")
    print(f"The designated holdout cluster, '{HOLDOUT_CLUSTER}', did not produce a valid Rank 1 curve and was skipped.")
    print("The pipeline cannot proceed to the validation stage without a valid holdout case.")
    print("Please select a different holdout cluster from the successful Rank 1 curves or add more clusters to the dataset.")
    exit() 
# --- END OF VALIDATION BLOCK ---


if df.empty:
    print(f"\n\033[91mCRITICAL PIPELINE ERROR:\033[0m")
    print("The training dataset is empty. No Rank 1 curves were found among the non-holdout clusters.")
    print("Cannot proceed to model training.")
    exit()


# Stage 2: Analyzing Denominator Structure
# =========================================


print("\n--- Stage 2: Analyzing Denominator Structure ---")


def find_denominator_rule(denominators):
    """
    Analyzes a list of denominators to find a generating rule.
