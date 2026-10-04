# Retry Attempt 18 with a higher descent_second_limit
print(f"\nRetrying Attempt 18 with descent_second_limit=100: Testing Fibonacci curve with a=2584,
b=144")
success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E = analyze_curve(
    2584, 144, require_3selmer=False, conductor_limit=1e11, descent_limit=100
)

# Update interweb_data if successful
if success and rank is not None and omega is not None and reg is not None:
    interweb_data.append((2584, 144, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
