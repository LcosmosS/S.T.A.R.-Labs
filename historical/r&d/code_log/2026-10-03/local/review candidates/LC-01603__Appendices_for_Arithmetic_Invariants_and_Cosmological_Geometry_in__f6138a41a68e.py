    plt.xlabel("Mass Density Quantile", fontsize=12); plt.ylabel("Redshift Quantile",
fontsize=12)
    plt.savefig(f"{OUTPUT_PLOT_PREFIX}_bayesian_binning.png"); plt.close()

    print("  - Generating KDE L-Function Analogue plot on full dataset...")
    plt.figure(figsize=(12, 7)); sns.kdeplot(data=df, x='K_clipped', fill=True)
    plt.title("KDE L-Function Analogue of Scaling Constant K (Full Dataset)",
fontsize=16)
    plt.xlabel("Value of K (Clipped)", fontsize=12); plt.ylabel("Probability Density",
fontsize=12)
    plt.savefig(f"{OUTPUT_PLOT_PREFIX}_kde_l_function.png"); plt.close()

def run_predictive_modeling(df):
    features = ['discriminant', 'z', 'logmass', 'petrorad_r', 'density_kg_m3']
    target = 'virial_energy_j'

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25,
random_state=42)

    print(f"  - Data split into {len(X_train)} training samples and {len(X_test)} test
