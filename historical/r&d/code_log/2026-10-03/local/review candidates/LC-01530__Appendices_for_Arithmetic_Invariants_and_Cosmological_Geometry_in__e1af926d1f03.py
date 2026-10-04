        results["fundamental_plane_corr"] = float(corr)
    else:
        print("  > Testing Fundamental Plane (Ellipticals)...")
        print("    - Not enough data points to calculate correlation.")
        results["fundamental_plane_corr"] = None

    return results

def run_stage_3_math_physics_context():
    """
    This stage is conceptual, outlining the context for deeper research.
