    if rank == 1 and 0.01 < regulator < 10.0:
        # "Fine-tuned" zone for stable structure formation
        return 1.0
    elif rank == 0:
        # "Empty" universe, no complexity
        return 0.1
    else:
        # High-rank or high-regulator universes are "unstable" (e.g., too dense, collapses)
        return 1 / (1 + rank + regulator)


# ==============================================================================
# SECTION 3: PIPELINE EXECUTION STAGES
# ==============================================================================


def run_stage_1_stat_mech_test(normalization_data):
    """
    Tests if the empirically validated T_cosmo is consistent with the value
