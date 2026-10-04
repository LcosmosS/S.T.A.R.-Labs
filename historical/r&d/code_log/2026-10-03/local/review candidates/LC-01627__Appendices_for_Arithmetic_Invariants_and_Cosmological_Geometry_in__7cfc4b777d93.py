        plt.savefig(f"{OUTPUT_PLOT_PREFIX}_bayesian_binning.png"); plt.close()
    except Exception as e:
        print(f"    - Could not generate Bayesian Binning plot. Error: {e}")

    print("  - Generating KDE L-Function Analogue plot on full dataset...")
    plt.figure(figsize=(12, 7)); sns.kdeplot(data=df, x='K_clipped', fill=True)
    plt.title("KDE L-Function Analogue of Scaling Constant K", fontsize=16)
    plt.xlabel("Value of K (Clipped)", fontsize=12); plt.ylabel("Probability Density",
fontsize=12)
    plt.savefig(f"{OUTPUT_PLOT_PREFIX}_kde_l_function.png"); plt.close()

def run_predictive_modeling(df):
    # --- MODELING IN LOG-STABLE SPACE ---
    features = ['log_abs_discriminant', 'z', 'logmass', 'petrorad_r']
    target = 'log_abs_virial_energy'
