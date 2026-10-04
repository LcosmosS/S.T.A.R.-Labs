# Main testing loop (Attempts 87–90)
max_attempts = 90
attempt = 87
current_fib_index = 78
phi_powers = [0, 1, 2]

while attempt <= max_attempts:
    if current_fib_index >= len(fib_numbers):
        fib_numbers.append(fib_numbers[-1] + fib_numbers[-2])
        print(f"Extended Fibonacci numbers to index {current_fib_index}: {fib_numbers[-1]}")