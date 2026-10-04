    # Bin the data 
    bins = {}
    for index, row in data.iterrows():
        key = (row['logmass'], row['z'], row['petrorad_r'])
        if key not in bins:
            bins[key] = 0
        bins[key] += 1

    l_value = 0
    for i, count in enumerate(bins.values()):
        l_value += count * (i + 1)**(-s)  # Using i+1 as n
    return l_value

def estimate_rank(data):
    """
    Estimates the rank of the galaxy distribution.
