# Compute L(1)
l_1 = l_function(1, bin_counts)


# Compute L(1.01)
l_1_01 = l_function(1.01, bin_counts)


# Estimate the derivative at s=1
dl_ds = (l_1_01 - l_1) / 0.01


# Hypothesize the order of the zero based on the derivative
if abs(dl_ds) > 1e-5:
    order = 1  # First-order zero
else:
    order = 2  # Higher-order zero


print(f"Estimated order of zero at s=1: {order}")
