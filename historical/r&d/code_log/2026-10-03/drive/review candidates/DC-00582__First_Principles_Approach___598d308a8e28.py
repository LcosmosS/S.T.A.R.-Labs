    print("\n--- STAGE 1: Statistical Mechanics Validation ---")
    N = normalization_data['N']
    t_empirical = normalization_data['T_cosmo_empirical']
    t_theoretical = model_t_cosmo_from_stat_mech(N)
    
    percent_diff = 100 * abs(t_empirical - t_theoretical) / t_empirical
    
    print(f"  > Empirical T_cosmo (from N=978 data): {t_empirical:.2f}")
    print(f"  > Theoretical T_cosmo (from StatMech, ~C*sqrt(N)): {t_theoretical:.2f}")
    print(f"  > Percent Difference: {percent_diff:.2f}%")
    
    is_consistent = percent_diff < 10.0 # Set a 10% tolerance for consistency
    print(f"  > Result: The values are {'CONSISTENT' if is_consistent else 'INCONSISTENT'}.")
    return {"empirical_T": t_empirical, "theoretical_T": t_theoretical, "consistent": is_consistent}


def run_stage_2_scaling_law_test(ucf_data):
    """
    Tests if the UCF's arithmetic invariants can reproduce established
