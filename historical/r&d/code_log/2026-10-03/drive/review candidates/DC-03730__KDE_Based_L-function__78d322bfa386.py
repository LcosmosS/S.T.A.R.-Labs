def custom_log1p(x):
    if x > 0:
        return np.log1p(x)
    elif x < 0:
        return np.tanh(x)  # Or use any other transformation you find suitable
    else:
        return 0  # Handle the zero case
