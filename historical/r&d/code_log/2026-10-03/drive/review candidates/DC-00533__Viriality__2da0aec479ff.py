    return mcxc_sample


def fetch_hiflugcs_data():
    """Fetch and parse HIFLUGCS data from arXiv PDF summary (30+)."""
    # Simulated parse; z mostly N/A, use medians or skip incomplete.
    hiflugcs_sample = [  # From tool summary, first 10 as demo
